#!/usr/bin/env python3
"""
collect_data.py
Resumable, rate-limited data collection script for NPM Supply Chain Research.
Fuses npm metadata, deps.dev dependency topology, GitHub workflows, and OSV advisories.
"""

import os
import sys
import re
import json
import time
import sqlite3
import hashlib
import zipfile
import tempfile
import argparse
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

# Configurations
DB_FILE = "data/npm_ecosystem.db"
DEFAULT_DELAY = 0.2  # Seconds between requests
LONG_BREAK_INTERVAL = 100  # Number of requests before a long break
LONG_BREAK_DURATION = 5.0  # Duration of the long break in seconds
MAX_RETRIES = 5
BACKOFF_FACTOR = 2  # Exponential backoff multiplier
USER_AGENT = "npm-supply-chain-researcher/1.0 (Academic Research; contact: paper-auth@gmail.com)"

# Initialize SQL Database
def init_db(conn):
    cursor = conn.cursor()
    
    # 1. Packages Queue
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS packages (
        name TEXT PRIMARY KEY,
        fetched_registry INTEGER DEFAULT 0,
        fetched_dependencies INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # 2. Package Versions metadata
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS package_versions (
        package_name TEXT,
        version TEXT,
        repository_url TEXT,
        github_owner TEXT,
        github_repo TEXT,
        has_github_workflows INTEGER, -- NULL = not checked, 0 = no, 1 = yes
        fetched_workflows INTEGER DEFAULT 0,
        PRIMARY KEY (package_name, version)
    )""")
    
    # 3. Maintainers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS maintainers (
        username TEXT PRIMARY KEY,
        email_hash TEXT
    )""")
    
    # 4. Package Maintainers Mapping
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS package_maintainers (
        package_name TEXT,
        maintainer_username TEXT,
        PRIMARY KEY (package_name, maintainer_username)
    )""")
    
    # 5. Dependency Graph Edges
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dependencies (
        from_package TEXT,
        from_version TEXT,
        to_package TEXT,
        to_version TEXT,
        requirement TEXT,
        relation TEXT, -- DIRECT or INDIRECT
        PRIMARY KEY (from_package, from_version, to_package, to_version)
    )""")
    
    # 6. Historical compromised packages (Ground Truth labels)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS advisories (
        id TEXT PRIMARY KEY,
        package_name TEXT,
        summary TEXT,
        details TEXT,
        severity TEXT,
        published_at TIMESTAMP,
        classification TEXT -- account_takeover, malicious_code, etc.
    )""")
    
    # Indexes for speed
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pkg_versions ON package_versions(package_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pkg_maintainers ON package_maintainers(package_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dep_from ON dependencies(from_package)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dep_to ON dependencies(to_package)")
    
    conn.commit()
    print("[+] Database initialized successfully.")

# Safe API Request with Retries & Exponential Backoff
def make_request(url, headers=None):
    if headers is None:
        headers = {}
    headers["User-Agent"] = USER_AGENT
    
    retries = 0
    sleep_time = 2.0
    
    while retries < MAX_RETRIES:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                return response.read(), response.status
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None, 404
            elif e.code in [429, 500, 502, 503, 504]:
                print(f"\n[!] HTTP {e.code} for {url}. Retrying in {sleep_time:.1f}s... (Attempt {retries+1}/{MAX_RETRIES})")
                time.sleep(sleep_time)
                retries += 1
                sleep_time *= BACKOFF_FACTOR
            else:
                print(f"\n[!] HTTP Error {e.code} for {url}. Skipping.")
                return None, e.code
        except urllib.error.URLError as e:
            print(f"\n[!] Connection error for {url}: {e.reason}. Retrying in {sleep_time:.1f}s...")
            time.sleep(sleep_time)
            retries += 1
            sleep_time *= BACKOFF_FACTOR
        except Exception as e:
            print(f"\n[!] Unexpected error: {str(e)}")
            return None, 999
            
    print(f"\n[X] Max retries reached. Failed to fetch: {url}")
    return None, 503

# Helper: Parse GitHub owner & repo from repo URL
def parse_github_url(repo_url):
    if not repo_url:
        return None, None
    if isinstance(repo_url, dict):
        repo_url = repo_url.get("url", "")
    if not isinstance(repo_url, str):
        return None, None
    
    # Clean prefixes
    repo_url = repo_url.replace("git+", "")
    repo_url = repo_url.replace("git://", "https://")
    repo_url = repo_url.replace("ssh://git@", "https://")
    
    # Suffixes
    repo_url = repo_url.split(".git")[0]
    repo_url = repo_url.split("#")[0]
    
    shorthands = ["github:", "github.com:", "git@github.com:"]
    for sh in shorthands:
        if repo_url.startswith(sh):
            repo_url = "https://github.com/" + repo_url[len(sh):]
            
    # Find match
    match = re.search(r"github\.com/([^/]+)/([^/.]+)", repo_url, re.IGNORECASE)
    if match:
        owner = match.group(1)
        repo = match.group(2)
        return owner, repo
    return None, None

# Command: --init (Seeds from high-impact list)
def seed_packages(conn):
    print("[*] Fetching seed package list from wooorm/npm-high-impact...")
    url = "https://raw.githubusercontent.com/wooorm/npm-high-impact/main/lib/top.js"
    content, code = make_request(url)
    if not content:
        print("[X] Failed to fetch seed packages list.")
        return
        
    js_text = content.decode("utf-8")
    packages = re.findall(r"'([^']+)'", js_text)
    if not packages:
        packages = re.findall(r'"([^"]+)"', js_text)
        
    if not packages:
        print("[X] Could not parse package names from javascript file.")
        return
        
    print(f"[+] Found {len(packages)} seed packages. Inserting into database...")
    cursor = conn.cursor()
    inserted = 0
    for name in packages:
        try:
            cursor.execute("INSERT OR IGNORE INTO packages (name) VALUES (?)", (name,))
            inserted += cursor.rowcount
        except Exception as e:
            pass
            
    conn.commit()
    print(f"[+] Seed complete. Added {inserted} new root packages. Total in queue: {get_total_packages(conn)}")

def get_total_packages(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM packages")
    return cursor.fetchone()[0]

# Command: --run (Main scraper loop)
def run_scraper(conn, batch_size=1000):
    cursor = conn.cursor()
    
    # Query packages that need fetching
    cursor.execute("""
        SELECT name FROM packages 
        WHERE fetched_registry = 0 OR fetched_dependencies = 0 
        LIMIT ?
    """, (batch_size,))
    
    pkgs = [row[0] for row in cursor.fetchall()]
    if not pkgs:
        print("[+] No pending packages in queue. All resolved!")
        return
        
    print(f"[*] Starting collection loop for {len(pkgs)} packages...")
    
    req_count = 0
    start_time = time.time()
    
    for idx, pkg_name in enumerate(pkgs):
        print(f"\r[{idx+1}/{len(pkgs)}] Scraping: {pkg_name:<50}", end="", flush=True)
        
        # Safe URL encoding for npm package name (handles scoped packages like @types/node)
        encoded_pkg = urllib.parse.quote(pkg_name, safe="")
        
        # ----------------------------------------------------
        # 1. NPM Registry metadata (Version, Maintainers, Repo URL)
        # ----------------------------------------------------
        npm_url = f"https://registry.npmjs.org/{encoded_pkg}/latest"
        registry_fetched = 0
        latest_version = None
        repo_url = None
        owner = None
        repo = None
        
        raw_npm, code = make_request(npm_url)
        req_count += 1
        
        if code in [400, 403, 404, 405]:
            # Package might be deleted, unpublished, or has an invalid/restricted name
            cursor.execute("UPDATE packages SET fetched_registry = -1, fetched_dependencies = -1 WHERE name = ?", (pkg_name,))
            conn.commit()
            continue
            
        if raw_npm:
            try:
                npm_data = json.loads(raw_npm.decode("utf-8"))
                latest_version = npm_data.get("version")
                repo_info = npm_data.get("repository", {})
                
                if isinstance(repo_info, dict):
                    repo_url = repo_info.get("url")
                else:
                    repo_url = str(repo_info)
                    
                owner, repo = parse_github_url(repo_url)
                
                # Insert package version
                cursor.execute("""
                    INSERT OR REPLACE INTO package_versions 
                    (package_name, version, repository_url, github_owner, github_repo) 
                    VALUES (?, ?, ?, ?, ?)
                """, (pkg_name, latest_version, repo_url, owner, repo))
                
                # Insert maintainers
                maintainers = npm_data.get("maintainers", [])
                if isinstance(maintainers, list):
                    for m in maintainers:
                        m_name = m.get("name")
                        m_email = m.get("email", "")
                        if m_name:
                            # Hash email for privacy
                            email_hash = hashlib.sha256(m_email.encode("utf-8")).hexdigest() if m_email else None
                            cursor.execute("INSERT OR IGNORE INTO maintainers (username, email_hash) VALUES (?, ?)", (m_name, email_hash))
                            cursor.execute("INSERT OR IGNORE INTO package_maintainers (package_name, maintainer_username) VALUES (?, ?)", (pkg_name, m_name))
                
                registry_fetched = 1
                cursor.execute("UPDATE packages SET fetched_registry = 1 WHERE name = ?", (pkg_name,))
            except Exception as e:
                print(f"\n[!] Error parsing npm data for {pkg_name}: {e}")
                
        # Time throttle
        time.sleep(DEFAULT_DELAY)
        
        # ----------------------------------------------------
        # 2. Deps.dev API (Dependency Topology)
        # ----------------------------------------------------
        dependencies_fetched = 0
        if registry_fetched and latest_version:
            deps_url = f"https://api.deps.dev/v3/systems/npm/packages/{encoded_pkg}/versions/{latest_version}:dependencies"
            raw_deps, code = make_request(deps_url)
            req_count += 1
            
            if code == 404:
                # Fallback: query deps.dev package endpoint to get all available versions
                pkg_url = f"https://api.deps.dev/v3/systems/npm/packages/{encoded_pkg}"
                raw_pkg_data, pkg_code = make_request(pkg_url)
                req_count += 1
                if raw_pkg_data:
                    try:
                        pkg_json = json.loads(raw_pkg_data.decode("utf-8"))
                        versions_list = pkg_json.get("versions", [])
                        
                        # Extract version strings (ignoring pre-releases)
                        ver_candidates = []
                        for v in versions_list:
                            ver_str = v.get("versionKey", {}).get("version")
                            if ver_str and "-" not in ver_str and ver_str != latest_version:
                                ver_candidates.append(ver_str)
                                
                        # Sort by semver descending
                        def semver_key(version_str):
                            s = version_str.lstrip('v')
                            parts = s.split('-')[0].split('.')
                            digits = []
                            for x in parts:
                                try:
                                    digits.append(int(x))
                                except ValueError:
                                    digits.append(x)
                            while len(digits) < 3:
                                digits.append(0)
                            return digits
                            
                        ver_candidates.sort(key=semver_key, reverse=True)
                        
                        # Try fallback versions
                        for fb_ver in ver_candidates[:5]:
                            deps_url = f"https://api.deps.dev/v3/systems/npm/packages/{encoded_pkg}/versions/{fb_ver}:dependencies"
                            raw_deps, code = make_request(deps_url)
                            req_count += 1
                            if raw_deps:
                                latest_version = fb_ver # update latest_version so parsing uses it
                                break
                    except Exception as e:
                        print(f"\n[!] Error finding fallback version for {pkg_name}: {e}")
            
            if raw_deps:
                try:
                    deps_data = json.loads(raw_deps.decode("utf-8"))
                    nodes = deps_data.get("nodes", [])
                    edges = deps_data.get("edges", [])
                    
                    # 2a. Insert all transitive packages found in the tree into packages queue
                    for node in nodes:
                        node_key = node.get("versionKey", {})
                        node_name = node.get("versionKey", {}).get("name")
                        if node_name and node_name != pkg_name:
                            # Insert into queue as unfetched
                            cursor.execute("INSERT OR IGNORE INTO packages (name) VALUES (?)", (node_name,))
                            
                    # 2b. Insert dependency edges
                    for edge in edges:
                        from_idx = edge.get("fromNode")
                        to_idx = edge.get("toNode")
                        req_str = edge.get("requirement", "")
                        
                        if from_idx is not None and to_idx is not None and from_idx < len(nodes) and to_idx < len(nodes):
                            from_node = nodes[from_idx].get("versionKey", {})
                            to_node = nodes[to_idx].get("versionKey", {})
                            
                            from_pkg = from_node.get("name")
                            from_ver = from_node.get("version")
                            to_pkg = to_node.get("name")
                            to_ver = to_node.get("version")
                            relation = nodes[to_idx].get("relation", "INDIRECT")
                            
                            if from_pkg and to_pkg:
                                cursor.execute("""
                                    INSERT OR REPLACE INTO dependencies 
                                    (from_package, from_version, to_package, to_version, requirement, relation) 
                                    VALUES (?, ?, ?, ?, ?, ?)
                                """, (from_pkg, from_ver, to_pkg, to_ver, req_str, relation))
                                
                    dependencies_fetched = 1
                    cursor.execute("UPDATE packages SET fetched_dependencies = 1 WHERE name = ?", (pkg_name,))
                except Exception as e:
                    print(f"\n[!] Error parsing deps.dev data for {pkg_name}: {e}")
            elif code == 404:
                # If we tried everything (or there were no fallbacks) and got 404,
                # mark as fetched to prevent getting stuck since the resource permanently doesn't exist on deps.dev
                cursor.execute("UPDATE packages SET fetched_dependencies = 1 WHERE name = ?", (pkg_name,))
                    
        # Commit transaction every package to save progress
        conn.commit()
        
        # Long break logic to satisfy API servers
        if req_count > 0 and req_count % LONG_BREAK_INTERVAL == 0:
            print(f"\n[*] Request block complete ({req_count} requests). Pausing for {LONG_BREAK_DURATION}s to prevent rate limits...")
            time.sleep(LONG_BREAK_DURATION)
        else:
            time.sleep(DEFAULT_DELAY)

    elapsed = time.time() - start_time
    print(f"\n[+] Batch complete. Scraped in {elapsed:.1f}s.")

# Command: --fetch-github (Checks workflow presence using GraphQL to avoid strict rate limits)
def fetch_github_workflows(conn, token=None):
    if not token:
        print("[!] Error: GITHUB_TOKEN environment variable is required for GraphQL API.")
        return
        
    cursor = conn.cursor()
    cursor.execute("""
        SELECT package_name, version, github_owner, github_repo 
        FROM package_versions 
        WHERE github_owner IS NOT NULL 
          AND github_repo IS NOT NULL 
          AND fetched_workflows = 0
    """)
    
    rows = cursor.fetchall()
    if not rows:
        print("[+] No pending github workflow checks.")
        return
        
    print(f"[*] Checking GitHub workflow directories for {len(rows)} packages via GraphQL...")
    headers = {
        "Authorization": f"bearer {token}",
        "Content-Type": "application/json"
    }
    
    for idx, (pkg_name, ver, owner, repo) in enumerate(rows):
        print(f"\r[{idx+1}/{len(rows)}] GraphQL check: {owner}/{repo:<40}", end="", flush=True)
        
        # Verify workflows folder existence using GitHub GraphQL API
        query = """
        query {
          repository(owner: "%s", name: "%s") {
            object(expression: "HEAD:.github/workflows") {
              ... on Tree {
                entries {
                  name
                }
              }
            }
          }
        }
        """ % (owner, repo)
        
        payload = json.dumps({"query": query}).encode("utf-8")
        req = urllib.request.Request("https://api.github.com/graphql", data=payload, headers=headers)
        
        has_workflows = 0
        try:
            with urllib.request.urlopen(req) as response:
                resp_data = json.loads(response.read().decode("utf-8"))
                
                # Check for rate limit errors in GraphQL response
                if "errors" in resp_data:
                    for err in resp_data["errors"]:
                        if err.get("type") == "RATE_LIMITED":
                            print("\n[X] GitHub GraphQL API rate limit exceeded.")
                            return
                
                repo_data = resp_data.get("data", {}).get("repository", {})
                if repo_data and repo_data.get("object"):
                    # If the object is not null, the directory exists
                    has_workflows = 1
                    
            cursor.execute("""
                UPDATE package_versions 
                SET has_github_workflows = ?, fetched_workflows = 1 
                WHERE package_name = ? AND version = ?
            """, (has_workflows, pkg_name, ver))
            conn.commit()
        except urllib.error.HTTPError as e:
            if e.code == 401:
                print("\n[X] Unauthorized. Check your GITHUB_TOKEN.")
                break
            elif e.code == 403:
                print("\n[X] GitHub API rate limit exceeded or forbidden.")
                break
            elif e.code == 404:
                # Repository might be deleted or private
                cursor.execute("""
                    UPDATE package_versions 
                    SET has_github_workflows = 0, fetched_workflows = 1 
                    WHERE package_name = ? AND version = ?
                """, (pkg_name, ver))
                conn.commit()
        except Exception as e:
            pass # Network issues, ignore and retry next run
        
        # Sleep to be polite to Github API
        time.sleep(0.5)
        
    print("\n[+] GitHub workflow checks complete.")

# Command: --fetch-advisories (Downloads OSV dataset and imports npm security targets)
def fetch_osv_advisories(conn):
    print("[*] Downloading OSV npm vulnerabilities archive...")
    url = "https://osv-vulnerabilities.storage.googleapis.com/npm/all.zip"
    
    # Use temporary file to download zip
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_file:
        tmp_path = tmp_file.name
        
    try:
        urllib.request.urlretrieve(url, tmp_path)
        print("[*] Extraction and import in progress...")
        
        cursor = conn.cursor()
        imported = 0
        
        # Keywords suggesting compromised entry points rather than typical code bugs
        compromise_keywords = [
            "account takeover", "malicious", "compromise", "backdoor", 
            "dependency confusion", "token", "credential", "steal"
        ]
        
        with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith('.json'):
                    with zip_ref.open(file_name) as f:
                        data = json.loads(f.read().decode('utf-8'))
                        
                        advisory_id = data.get("id")
                        summary = data.get("summary", "")
                        details = data.get("details", "")
                        published = data.get("published", "")
                        
                        # Date filter: September 2025 to April 2026
                        # Format is usually: 2025-09-15T12:00:00Z
                        pub_date = None
                        if published:
                            try:
                                # Simple prefix check is fast
                                pub_year_month = published[:7] # e.g. "2025-09"
                                if pub_year_month >= "2025-09" and pub_year_month <= "2026-04":
                                    pub_date = published
                            except:
                                pass
                                
                        if not pub_date:
                            continue
                            
                        # Keyword matching
                        text_to_search = (summary + " " + details).lower()
                        is_compromise = any(kw in text_to_search for kw in compromise_keywords)
                        if not is_compromise:
                            continue
                            
                        # Find affected packages
                        affected = data.get("affected", [])
                        for item in affected:
                            pkg_info = item.get("package", {})
                            pkg_name = pkg_info.get("name")
                            
                            if pkg_name:
                                severity = "UNKNOWN"
                                database_specific = data.get("database_specific", {})
                                if database_specific:
                                    severity = database_specific.get("severity", "UNKNOWN")
                                    
                                classification = "compromise"
                                if "dependency confusion" in text_to_search:
                                    classification = "dependency_confusion"
                                elif "account takeover" in text_to_search:
                                    classification = "account_takeover"
                                    
                                cursor.execute("""
                                    INSERT OR REPLACE INTO advisories 
                                    (id, package_name, summary, details, severity, published_at, classification) 
                                    VALUES (?, ?, ?, ?, ?, ?, ?)
                                """, (advisory_id, pkg_name, summary, details, severity, published, classification))
                                imported += 1
                                
        conn.commit()
        print(f"[+] OSV import complete. Added {imported} historical compromised package advisories.")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

# Command: --stats
def print_stats(conn):
    cursor = conn.cursor()
    
    # Queued packages stats
    cursor.execute("SELECT COUNT(*) FROM packages")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM packages WHERE fetched_registry = 1 AND fetched_dependencies = 1")
    fetched = cursor.fetchone()[0]
    
    # Versions
    cursor.execute("SELECT COUNT(*) FROM package_versions")
    versions = cursor.fetchone()[0]
    
    # Maintainers
    cursor.execute("SELECT COUNT(*) FROM maintainers")
    maintainers = cursor.fetchone()[0]
    
    # Edges (Dependencies)
    cursor.execute("SELECT COUNT(*) FROM dependencies")
    dependencies = cursor.fetchone()[0]
    
    # GitHub Workflow presence
    cursor.execute("SELECT COUNT(*) FROM package_versions WHERE github_owner IS NOT NULL")
    github_mapped = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM package_versions WHERE fetched_workflows = 1")
    github_checked = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM package_versions WHERE has_github_workflows = 1")
    github_actions = cursor.fetchone()[0]
    
    # Advisories
    cursor.execute("SELECT COUNT(*) FROM advisories")
    advisories = cursor.fetchone()[0]
    
    print("="*50)
    print("        NPM ECOSYSTEM GRAPH STATS SUMMARY        ")
    print("="*50)
    print(f"Total Packages in DB (Seed + Transitive): {total}")
    print(f"Completed Scrapes (npm + deps.dev):       {fetched} ({fetched/total*100:.2f}% complete)")
    print(f"Unique Package Versions:                   {versions}")
    print(f"Unique Developer Maintainers:             {maintainers}")
    print(f"Total Dependency Edges:                    {dependencies}")
    print("-"*50)
    print(f"Packages with GitHub Repositories Mapped:  {github_mapped}")
    print(f"GitHub Workflows Checked:                  {github_checked}")
    print(f"Workflows (CI/CD) Found:                   {github_actions}")
    print("-"*50)
    print(f"OSV Compromise Advisories (Labels):        {advisories}")
    print("="*50)

def main():
    parser = argparse.ArgumentParser(description="Collect cross-domain metadata from npm registry, deps.dev, and GitHub.")
    parser.add_argument("--init", action="store_true", help="Initialize database and seed with high-impact packages")
    parser.add_argument("--run", action="store_true", help="Run the registry and dependency graph scraper")
    parser.add_argument("--fetch-github", action="store_true", help="Perform GitHub workflow directory check")
    parser.add_argument("--fetch-advisories", action="store_true", help="Download and parse historical ground truth advisories")
    parser.add_argument("--stats", action="store_true", help="Print database statistics summary")
    parser.add_argument("--batch", type=int, default=1000, help="Batch size of packages to scrape in this run")
    parser.add_argument("--loop", action="store_true", help="Run the scraper continuously in batches until queue is empty")
    parser.add_argument("--break-time", type=int, default=60, help="Sleep duration in seconds between batches in loop mode")
    
    args = parser.parse_args()
    
    if not (args.init or args.run or args.fetch_github or args.fetch_advisories or args.stats):
        parser.print_help()
        sys.exit(0)
        
    conn = sqlite3.connect(DB_FILE)
    
    if args.init:
        init_db(conn)
        seed_packages(conn)
        
    if args.run:
        # Check if database is empty, seed if it is
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM packages")
        if cursor.fetchone()[0] == 0:
            print("[!] Database packages queue is empty. Initializing first...")
            init_db(conn)
            seed_packages(conn)
            
        if args.loop:
            print(f"[*] Starting loop mode. Batch size: {args.batch}, Break time: {args.break_time}s")
            while True:
                # Count remaining packages that need scraping
                cursor.execute("SELECT COUNT(*) FROM packages WHERE fetched_registry = 0 OR fetched_dependencies = 0")
                remaining = cursor.fetchone()[0]
                if remaining == 0:
                    print("[+] All packages scraped successfully!")
                    break
                
                print(f"\n[*] {remaining} packages remaining in the queue. Scrapes in this batch: {min(args.batch, remaining)}")
                run_scraper(conn, batch_size=args.batch)
                
                # Check again to avoid sleeping if we just finished
                cursor.execute("SELECT COUNT(*) FROM packages WHERE fetched_registry = 0 OR fetched_dependencies = 0")
                remaining = cursor.fetchone()[0]
                if remaining == 0:
                    print("[+] All packages scraped successfully!")
                    break
                    
                print(f"[*] Batch complete. Sleeping for {args.break_time} seconds before next batch...")
                time.sleep(args.break_time)
        else:
            run_scraper(conn, batch_size=args.batch)
        
    if args.fetch_github:
        token = os.environ.get("GITHUB_TOKEN")
        fetch_github_workflows(conn, token=token)
        
    if args.fetch_advisories:
        fetch_osv_advisories(conn)
        
    if args.stats:
        print_stats(conn)
        
    conn.close()

if __name__ == "__main__":
    main()
