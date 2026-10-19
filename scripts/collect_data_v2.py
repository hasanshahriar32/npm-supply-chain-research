#!/usr/bin/env python3
"""Future collection with corrected URLs and dated workflow observations.

Keeps the original collector intact for historical reproducibility. Use the same
CLI flags as collect_data.py, preferably against a fresh collection database.
No historical flag is reinterpreted or silently copied to a corrected URL.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
import time
import urllib.error
import urllib.request

import collect_data as legacy
from research_observations import classify_workflow_response, parse_github_repository


def fetch_github_workflows(connection, token=None):
    token = token or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required for explicit public-workflow collection.")
    connection.execute("""CREATE TABLE IF NOT EXISTS workflow_observation_log (
        id INTEGER PRIMARY KEY, package_name TEXT, version TEXT, github_owner TEXT,
        github_repo TEXT, observed_at_utc TEXT, observation_state TEXT,
        http_status INTEGER, response_sha256 TEXT, detail TEXT)""")
    pending = list(connection.execute("""SELECT package_name,version,github_owner,github_repo
        FROM package_versions WHERE github_owner IS NOT NULL AND github_repo IS NOT NULL
        AND fetched_workflows=0 ORDER BY package_name,version"""))
    query = """query($owner:String!,$name:String!){repository(owner:$owner,name:$name){
        nameWithOwner object(expression:"HEAD:.github/workflows"){
        __typename ... on Tree {entries{name}}}}}"""
    for package, version, owner, repository in pending:
        request = urllib.request.Request("https://api.github.com/graphql",
            data=json.dumps({"query": query, "variables": {"owner": owner, "name": repository}}).encode(),
            headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "npm-research-workflow-observation/2"})
        response_bytes, status, payload = b"", 0, None
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                status, response_bytes = response.status, response.read()
            payload = json.loads(response_bytes)
        except urllib.error.HTTPError as error:
            status, response_bytes = error.code, error.read()
        except (urllib.error.URLError, TimeoutError, ValueError):
            pass
        state, flag, detail = classify_workflow_response(status, payload)
        connection.execute("INSERT INTO workflow_observation_log (package_name,version,github_owner,github_repo,observed_at_utc,observation_state,http_status,response_sha256,detail) VALUES (?,?,?,?,?,?,?,?,?)",
            (package, version, owner, repository, datetime.now(timezone.utc).isoformat(), state, status,
             hashlib.sha256(response_bytes).hexdigest() if response_bytes else None, detail))
        connection.execute("UPDATE package_versions SET has_github_workflows=?,fetched_workflows=? WHERE package_name=? AND version=?",
            (flag, int(flag is not None), package, version))
        connection.commit()
        if status in {401, 403} or (isinstance(payload, dict) and any(e.get("type") == "RATE_LIMITED" for e in payload.get("errors", []) if isinstance(e, dict))):
            break
        time.sleep(.5)
    print("Dated public-workflow observations recorded; unavailable/error observations remain unknown.")


if __name__ == "__main__":
    legacy.parse_github_url = parse_github_repository
    legacy.fetch_github_workflows = fetch_github_workflows
    legacy.main()
