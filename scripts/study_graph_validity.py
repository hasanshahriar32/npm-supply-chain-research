#!/usr/bin/env python3
"""Reproduce graph-fidelity and observation-unit analyses without changing data.

The version graph is the UNION of retained deps.dev resolutions. Enforcing node
version continuity removes package-projection paths, but does not reconstruct an
installation, a historic cutoff, or a jointly satisfiable dependency resolution.
Only Python's standard library is required. All extraction is temporary and the
SQLite connection is read-only. Package payloads are neither fetched nor run.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil
import sqlite3
import statistics
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'manuscript/results/graph_validity'
ARCHIVE = ROOT / 'data/npm_ecosystem.db.zip'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path, rows):
    if not rows:
        return
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def summary(values):
    values = sorted(values)
    if not values:
        return {'n': 0}
    return {'n': len(values), 'min': values[0], 'median': statistics.median(values),
            'mean': statistics.mean(values), 'p90': values[math.ceil(.9 * len(values))-1],
            'max': values[-1], 'sum': sum(values)}


def walk(seeds, adjacency):
    seen = set(seeds)
    pending = list(seen)
    while pending:
        for neighbor in adjacency.get(pending.pop(), ()):
            if neighbor not in seen:
                seen.add(neighbor)
                pending.append(neighbor)
    return seen


def scc(nodes, adjacency):
    """Iterative Kosaraju avoids recursion-depth dependence on real graphs."""
    visited, order = set(), []
    for root in sorted(nodes):
        if root in visited:
            continue
        visited.add(root)
        stack = [(root, iter(adjacency.get(root, ())))]
        while stack:
            node, neighbors = stack[-1]
            neighbor = next(neighbors, None)
            if neighbor is None:
                stack.pop()
                order.append(node)
            elif neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, iter(adjacency.get(neighbor, ()))))
    transpose = defaultdict(set)
    for source, destinations in adjacency.items():
        for destination in destinations:
            transpose[destination].add(source)
    visited, components = set(), []
    for root in reversed(order):
        if root in visited:
            continue
        component = set()
        pending = [root]
        visited.add(root)
        while pending:
            node = pending.pop()
            component.add(node)
            for neighbor in transpose[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    pending.append(neighbor)
        components.append(component)
    nontrivial = [c for c in components if len(c)>1]
    return {'nodes': len(nodes), 'edges': sum(map(len, adjacency.values())),
            'components': len(components), 'nontrivial_components': len(nontrivial),
            'nodes_in_nontrivial_components': sum(map(len, nontrivial)),
            'largest_component': max(map(len, components), default=0),
            'self_loops': sum(node in adjacency.get(node, ()) for node in nodes)}, nontrivial


def parse_repo(url):
    """Lexical GitHub URL parsing only; no remote identity/redirect validation."""
    if not isinstance(url, str):
        return None
    candidate = url.strip().replace('git+', '', 1)
    if candidate.startswith('github:'):
        candidate = 'https://github.com/' + candidate[len('github:'):]
    match = re.search(r'(?:^|[/@])github\.com[:/]([^/#?]+)/([^/#?]+)', candidate, re.I)
    if not match:
        return None
    owner, repo = match.groups()
    if repo.endswith('.git'):
        repo = repo[:-4]
    return (owner.casefold(), repo.casefold()) if owner and repo else None


def queue(rows, field, k):
    return {r['package_name'] for r in sorted(rows, key=lambda r: (-r[field], r['package_name']))[:k]}


def probe_public_sources():
    """Optional bounded access checks; does not download or execute package code."""
    target = OUT / 'source_access'
    target.mkdir(parents=True, exist_ok=True)
    requests = [
        ('npm_metadata_is_number','https://registry.npmjs.org/is-number',None),
        ('deps_dev_is_number','https://api.deps.dev/v3/systems/npm/packages/is-number/versions/7.0.0:dependencies',None),
        ('osv_keyv_reported_outcomes','https://api.osv.dev/v1/query',{'package':{'name':'keyv','ecosystem':'npm'}}),
        ('npm_follower_population_portal','https://dependencies.science/',None),
        ('chrono_resolution_release_metadata','https://zenodo.org/api/records/17576373',None),
        ('openssf_malicious_packages_contract','https://raw.githubusercontent.com/ossf/malicious-packages/main/README.md',None),
    ]
    def get(item):
        name,url,payload=item
        record={'name':name,'url':url,'method':'POST' if payload else 'GET',
                'payload':payload,'attempted_at_utc':datetime.now(timezone.utc).isoformat(),
                'timeout_seconds':15,'max_response_bytes':1048576}
        request=urllib.request.Request(url,data=json.dumps(payload).encode() if payload else None,
                                       headers={'User-Agent':'npm-supply-chain-empirical-study/1.0',
                                                'Content-Type':'application/json'} if payload else
                                       {'User-Agent':'npm-supply-chain-empirical-study/1.0'})
        try:
            with urllib.request.urlopen(request,timeout=15) as response:
                body=response.read(1048577)
                record.update(status=response.status,content_type=response.headers.get('Content-Type'),
                              body_bytes=len(body),complete=len(body)<=1048576,
                              final_url=response.url)
                if len(body)<=1048576:
                    filename=name+('.json' if 'json' in response.headers.get('Content-Type','') else '.txt')
                    retained=body
                    if name=='npm_metadata_is_number':
                        parsed=json.loads(body)
                        retained=json.dumps({'name':parsed.get('name'),'time':parsed.get('time'),
                                             'dist-tags':parsed.get('dist-tags'),
                                             'versions':{version:{field:value for field,value in metadata.items()
                                                                  if field in ['name','version','dependencies','optionalDependencies','peerDependencies']}
                                                         for version,metadata in parsed.get('versions',{}).items()}},indent=2).encode()
                    (target/filename).write_bytes(retained)
                    record.update(retained_file=filename,response_sha256=hashlib.sha256(body).hexdigest(),
                                  retained_file_sha256=hashlib.sha256(retained).hexdigest(),
                                  retained_body_is_raw=(retained==body))
                    try:
                        data=json.loads(body)
                        if name=='npm_metadata_is_number':
                            record['parsed_summary']={'name':data.get('name'),'retained_versions':len(data.get('versions',{})),
                                                      'retained_time_map_keys':len(data.get('time',{})),
                                                      'latest_dist_tag':data.get('dist-tags',{}).get('latest')}
                        elif name=='deps_dev_is_number':
                            record['parsed_summary']={'nodes':len(data.get('nodes',[])),'edges':len(data.get('edges',[])),
                                                      'graph_error':data.get('error')}
                        elif name=='osv_keyv_reported_outcomes':
                            record['parsed_summary']={'returned_reports':len(data.get('vulns',[])),
                                                      'reports':[{'id':r.get('id'),'published':r.get('published'),
                                                                  'withdrawn':r.get('withdrawn'),'summary':r.get('summary')}
                                                                 for r in data.get('vulns',[])],
                                                      'next_page_token_present':bool(data.get('next_page_token'))}
                        elif name=='chrono_resolution_release_metadata':
                            record['parsed_summary']={'doi':data.get('doi'),'files':[
                                {'key':f.get('key'),'size':f.get('size'),'checksum':f.get('checksum')}
                                for f in data.get('files',[])]}
                    except (ValueError,TypeError):
                        pass
        except urllib.error.HTTPError as error:
            record.update(status=error.code,error=type(error).__name__,reason=str(error.reason))
        except Exception as error:
            record.update(status=None,error=type(error).__name__,reason=str(error))
        return record
    with ThreadPoolExecutor(max_workers=6) as pool:
        records=list(pool.map(get,requests))
    result={'purpose':'Bounded primary-source access feasibility, not model training or label certification.',
            'attempt_date':'2026-10-20','requests':records,'package_payloads_downloaded':0,
            'observation':'Current registry metadata can supply retained publication times and source manifests, but does not establish historical authority or workflow states. Public advisory absence is unlabeled and cannot certify benignness.'}
    (target/'access_attempts.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    input_sha = sha(ARCHIVE)
    with tempfile.TemporaryDirectory(prefix='npm-graph-validity-') as temporary:
        database = Path(temporary) / 'ecosystem.db'
        with zipfile.ZipFile(ARCHIVE) as archive, archive.open('npm_ecosystem.db') as source, database.open('wb') as dest:
            shutil.copyfileobj(source, dest)
        connection = sqlite3.connect(f'file:{database}?mode=ro&immutable=1', uri=True)
        connection.row_factory = sqlite3.Row
        packages = {row[0] for row in connection.execute('SELECT name FROM packages')}
        versions = [dict(r) for r in connection.execute('SELECT * FROM package_versions')]
        dependencies = [dict(r) for r in connection.execute('SELECT * FROM dependencies')]
        package_states = [dict(r) for r in connection.execute('SELECT * FROM packages')]
        metrics = {r['package_name']: dict(r) for r in connection.execute('SELECT * FROM package_metrics')}
        schema = {r['name']: r['sql'] for r in connection.execute("SELECT name,sql FROM sqlite_master WHERE type='table'")}
        connection.close()

    package_reverse, version_reverse = defaultdict(set), defaultdict(set)
    versions_by_name, pair_versions = defaultdict(set), defaultdict(set)
    direct_label_reverse = defaultdict(set)
    for row in dependencies:
        a, b = (row['from_package'], row['from_version']), (row['to_package'], row['to_version'])
        package_reverse[b[0]].add(a[0])
        version_reverse[b].add(a)
        versions_by_name[a[0]].add(a)
        versions_by_name[b[0]].add(b)
        pair_versions[(b[0], a[0])].add((b[1], a[1]))
        if row['relation'] == 'DIRECT':
            direct_label_reverse[b[0]].add(a[0])
    metadata_versions = {(row['package_name'], row['version']) for row in versions}
    version_nodes = set(versions_by_name_node for nodes in versions_by_name.values() for versions_by_name_node in nodes)
    for node in metadata_versions:
        versions_by_name[node[0]].add(node)
    version_nodes.update(metadata_versions)
    package_nodes = packages | set(versions_by_name)
    package_scc, package_components = scc(package_nodes, package_reverse)
    version_scc, version_components = scc(version_nodes, version_reverse)
    write_csv(OUT/'nontrivial_components.csv',
              [{'graph':'package_name','size':len(c),'members':'|'.join(sorted(c))} for c in sorted(package_components,key=lambda x:-len(x))] +
              [{'graph':'package_version','size':len(c),'members':'|'.join(f'{p}@{v}' for p,v in sorted(c))} for c in sorted(version_components,key=lambda x:-len(x))])

    workflow_yes, workflow_no, workflow_unknown, linked = set(), set(), set(), set()
    package_repos, corrected_package_repos, repo_rows = defaultdict(set), defaultdict(set), defaultdict(list)
    mismatch_rows, unparsed_stored_rows = [], []
    for row in versions:
        package = row['package_name']
        state = row['has_github_workflows']
        (workflow_yes if state == 1 else workflow_no if state == 0 else workflow_unknown).add(package)
        observed = (row['github_owner'].casefold(), row['github_repo'].casefold()) if row['github_owner'] and row['github_repo'] else None
        corrected = parse_repo(row['repository_url'])
        if observed:
            linked.add(package)
            package_repos[package].add(observed)
            repo_rows[observed].append(row)
        if corrected:
            corrected_package_repos[package].add(corrected)
        if corrected and observed != corrected:
            mismatch_rows.append({'package_name':package,'version':row['version'], 'repository_url':row['repository_url'],
                                  'stored_repository':'/'.join(observed) if observed else '',
                                  'lexically_parsed_repository':'/'.join(corrected), 'workflow_flag':state})
        if observed and not corrected:
            unparsed_stored_rows.append(row)
    write_csv(OUT/'repository_parser_disagreements.csv', mismatch_rows)
    repo_summary = []
    for repo, records in sorted(repo_rows.items()):
        states = {r['has_github_workflows'] for r in records}
        repo_summary.append({'repository':'/'.join(repo), 'packages':len({r['package_name'] for r in records}),
                             'version_rows':len(records), 'workflow_positive_packages':len({r['package_name'] for r in records if r['has_github_workflows']==1}),
                             'conflicting_positive_negative':int(0 in states and 1 in states),
                             'unknown_present':int(None in states)})
    write_csv(OUT/'repository_units.csv', repo_summary)

    rows = []
    for index, package in enumerate(sorted(packages)):
        projected = walk([package], package_reverse) - {package}
        continuous_versions = walk(versions_by_name.get(package, ()), version_reverse)
        continuous = {p for p,v in continuous_versions} - {package}
        assert continuous <= projected, package
        projected_positive = projected & workflow_yes
        continuous_positive = continuous & workflow_yes
        repos = {repo for p in projected_positive for repo in package_repos[p]}
        continuous_repos = {repo for p in continuous_positive for repo in package_repos[p]}
        # Unknown means no observed yes/no record, or no retained registry row.
        unknown = {p for p in projected if p not in workflow_yes and p not in workflow_no}
        projected_direct_label = walk([package], direct_label_reverse) - {package}
        rows.append({'package_name':package, 'package_projected_reach':len(projected),
                     'version_continuous_name_reach':len(continuous), 'version_projection_excess':len(projected-continuous),
                     'workflow_package_reach':len(projected_positive), 'workflow_repository_reach':len(repos),
                     'version_continuous_workflow_package_reach':len(continuous_positive),
                     'version_continuous_workflow_repository_reach':len(continuous_repos),
                     'workflow_package_repository_excess':len(projected_positive)-len(repos),
                     'unknown_workflow_dependents':len(unknown),
                     'workflow_reach_upper_with_unknown':len(projected_positive)+len(unknown),
                     'direct_label_only_reach_diagnostic':len(projected_direct_label),
                     'maintainer_max_portfolio':metrics[package]['wormability_max']})
        assert len(projected_positive)==metrics[package]['blast_radius'], package
        assert len(projected)==metrics[package]['transitive_dependents'], package
        if index and index%5000==0:
            print(f'Completed {index}/{len(packages)} rooted version-continuity comparisons', flush=True)
    write_csv(OUT/'per_package.csv', rows)
    k = math.ceil(.01*len(packages))
    queue_fields = ['package_projected_reach','version_continuous_name_reach','workflow_package_reach',
                    'workflow_repository_reach','version_continuous_workflow_repository_reach','workflow_reach_upper_with_unknown']
    queues = {field:queue(rows,field,k) for field in queue_fields}
    queue_comparisons = []
    for first,second in [('package_projected_reach','version_continuous_name_reach'),
                         ('workflow_package_reach','workflow_repository_reach'),
                         ('workflow_package_reach','version_continuous_workflow_repository_reach'),
                         ('workflow_package_reach','workflow_reach_upper_with_unknown')]:
        a,b=queues[first],queues[second]
        queue_comparisons.append({'first':first,'second':second,'budget':k,'intersection':len(a&b),
                                  'jaccard':len(a&b)/len(a|b)})

    # Combined structural score sensitivity retains the same default equal weight
    # and only changes which observation units contribute to the reach term.
    max_m=max(r['maintainer_max_portfolio'] for r in rows) or 1
    for field in ['workflow_package_reach','workflow_repository_reach','version_continuous_workflow_repository_reach']:
        max_reach=max(r[field] for r in rows) or 1
        score_field='equal_weight_'+field
        for row in rows:
            row[score_field]=.5*row['maintainer_max_portfolio']/max_m+.5*row[field]/max_reach
        queues[score_field]=queue(rows,score_field,k)
    base='equal_weight_workflow_package_reach'
    for field in ['equal_weight_workflow_repository_reach','equal_weight_version_continuous_workflow_repository_reach']:
        a,b=queues[base],queues[field]
        queue_comparisons.append({'first':base,'second':field,'budget':k,'intersection':len(a&b),'jaccard':len(a&b)/len(a|b)})
    write_csv(OUT/'queue_membership.csv',[{'definition':field,'package_name':package} for field,names in queues.items() for package in sorted(names)])
    write_csv(OUT/'per_package.csv',rows)

    witnesses=[]
    for row in sorted(rows,key=lambda r:(-r['version_projection_excess'],r['package_name']))[:5]:
        if row['version_projection_excess']==0:
            continue
        package=row['package_name']
        projected=walk([package],package_reverse)-{package}
        continuous={p for p,v in walk(versions_by_name[package],version_reverse)}-{package}
        absent=projected-continuous
        target=None
        pending=deque([package]); parent={package:None}
        while pending and target is None:
            source=pending.popleft()
            for neighbor in sorted(package_reverse[source]):
                if neighbor not in parent:
                    parent[neighbor]=source;pending.append(neighbor)
                    if neighbor in absent:
                        target=neighbor
                        break
        path=[target]
        while path[-1]!=package:
            path.append(parent[path[-1]])
        path.reverse()
        witnesses.append({'source_dependency':package,'spurious_reachable_name':target,
                          'reverse_package_path':path,
                          'version_options_per_edge':[
                              {'dependency':a,'dependent':b,
                               'dependency_version_dependent_version_pairs':[list(x) for x in sorted(pair_versions[a,b])]}
                              for a,b in zip(path,path[1:])],
                          'checked_absent_from_all_version_continuous_paths':True})
    (OUT/'version_projection_witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n')

    from_nodes={(r['from_package'],r['from_version']) for r in dependencies}
    to_nodes={(r['to_package'],r['to_version']) for r in dependencies}
    row_match=sum((r['from_package'],r['from_version']) in metadata_versions and
                  (r['to_package'],r['to_version']) in metadata_versions for r in dependencies)
    retained_positive_repo_keys={repo for p in workflow_yes for repo in package_repos[p]}
    direct_pairs={(r['from_package'],r['to_package']) for r in dependencies if r['relation']=='DIRECT'}
    indirect_pairs={(r['from_package'],r['to_package']) for r in dependencies if r['relation']=='INDIRECT'}
    label_contradictions=direct_pairs&indirect_pairs
    output = {
        'analysis':'observed-union-graph-fidelity-and-observation-units',
        'audit_date':'2026-10-20','generated_at_utc':datetime.now(timezone.utc).isoformat(),
        'python':sys.version.split()[0],
        'sources_sha256':{str(ARCHIVE.relative_to(ROOT)):input_sha,str(Path(__file__).relative_to(ROOT)):sha(Path(__file__)),
                          'scripts/collect_data.py':sha(ROOT/'scripts/collect_data.py')},
        'definitions':{
            'package_projected_reach':'Distinct reverse-reachable package names in the union of retained explicit dependency edges; root excluded.',
            'version_continuous_name_reach':'Start at every observed version of the root package, traverse exact matching version nodes in the union graph, then count distinct package names, root name excluded. This is a representation sensitivity diagnostic, not an installed-tree or historical resolution.',
            'workflow_repository_reach':'Deduplicate normalized retained GitHub owner/repository keys of workflow-positive reverse-reachable package names. Repository equivalence is lexical, not validated through remote redirects or commit identities.',
            'workflow_unknown':'No positive or negative workflow flag for a reachable package, including packages without a registry row. Unknown flags are not interpreted as absence.',
            'workflow_reach_upper_with_unknown':'Observed workflow-positive packages plus packages with only NULL/absent flags. This bound is conditional on zero flags indicating true absence. Collector zero flags conflate missing directories with unavailable repositories; a bound allowing that uncertainty is package_projected_reach.',
            'queue_ties':'Descending numeric score then Unicode code-point ascending package name; exact cardinality, observational rankings only.',
            'relation':'Stored from deps.dev target node relation to extraction root. All edges[] entries are declaring-to-resolving adjacencies; filtering by node relation is not a valid global direct-edge recovery.'},
        'population':{'queued_packages':len(packages),'metadata_packages':len({r['package_name'] for r in versions}),
                      'metadata_versions':len(metadata_versions),'dependency_rows':len(dependencies),
                      'dependency_source_versions':len(from_nodes),'dependency_target_versions':len(to_nodes),
                      'dependency_source_versions_with_metadata':len(from_nodes&metadata_versions),
                      'dependency_target_versions_with_metadata':len(to_nodes&metadata_versions),
                      'dependency_rows_both_endpoint_versions_have_metadata':row_match,
                      'metadata_versions_with_outgoing_edges':len(metadata_versions&from_nodes),
                      'dependency_package_names_outside_queue':len(set(versions_by_name)-packages),
                      'registry_state_counts':dict(Counter(str(r['fetched_registry']) for r in package_states)),
                      'packages_created_min':min(r['created_at'] for r in package_states),
                      'packages_created_max':max(r['created_at'] for r in package_states)},
        'scc':{'package_projection':package_scc,'exact_version_union':version_scc},
        'workflow_observation':{'positive_packages':len(workflow_yes),'packages_with_zero_flags_only':len(workflow_no-workflow_yes),
                                'unknown_only_metadata_packages':len(workflow_unknown-workflow_yes-workflow_no),
                                'no_metadata_packages':len(packages-{r['package_name'] for r in versions}),
                                'unknown_all_queued_packages':len(packages-workflow_yes-workflow_no),
                                'github_linked_packages':len(linked),'github_linked_repositories':len(repo_rows),
                                'workflow_positive_repositories':len(retained_positive_repo_keys),
                                'positive_packages_without_github_key':len(workflow_yes-linked),
                                'repositories_with_multiple_packages':sum(r['packages']>1 for r in repo_summary),
                                'repositories_with_disagreeing_yes_no_flags':sum(r['conflicting_positive_negative'] for r in repo_summary),
                                'packages_with_multiple_repo_keys':sum(len(repos)>1 for repos in package_repos.values()),
                                'repository_parser_disagreement_version_rows':len(mismatch_rows),
                                'repository_parser_disagreement_packages':len({r['package_name'] for r in mismatch_rows}),
                                'repository_parser_disagreement_positive_version_rows':sum(r['workflow_flag']==1 for r in mismatch_rows),
                                'stored_repo_rows_not_lexically_parsed':len(unparsed_stored_rows),
                                'packages_per_repository':summary([r['packages'] for r in repo_summary]),
                                'largest_repository_groups':sorted(repo_summary,key=lambda r:(-r['packages'],r['repository']))[:10]},
        'relation_diagnostic':{'direct_rows':sum(r['relation']=='DIRECT' for r in dependencies),
                               'indirect_rows':sum(r['relation']=='INDIRECT' for r in dependencies),
                               'package_pairs_having_both_labels_across_versions':len(label_contradictions),
                               'all_projected_package_pairs':sum(map(len,package_reverse.values())),
                               'direct_label_projected_package_pairs':len(direct_pairs),
                               'roots_changed_if_incorrect_direct_label_filter':sum(r['direct_label_only_reach_diagnostic']!=r['package_projected_reach'] for r in rows)},
        'sensitivity':{'projection_changed_packages':sum(r['version_projection_excess']>0 for r in rows),
                       'projection_excess_all_packages':summary([r['version_projection_excess'] for r in rows]),
                       'projection_excess_changed_packages':summary([r['version_projection_excess'] for r in rows if r['version_projection_excess']]),
                       'repository_dedup_changed_packages':sum(r['workflow_package_repository_excess']!=0 for r in rows),
                       'repository_excess_all_packages':summary([r['workflow_package_repository_excess'] for r in rows]),
                       'roots_with_unknown_reachable_flags':sum(r['unknown_workflow_dependents']>0 for r in rows),
                       'queue_comparisons':queue_comparisons,
                       'most_version_projection_excess':sorted(rows,key=lambda r:(-r['version_projection_excess'],r['package_name']))[:10],
                       'most_workflow_package_reach':sorted(rows,key=lambda r:(-r['workflow_package_reach'],r['package_name']))[:10]},
        'validation':{'all_version_continuous_sets_subset_of_package_projected_sets':True,
                      'all_package_projected_reach_reproduces_database':True,
                      'all_workflow_package_reach_reproduces_database':True,
                      'input_archive_unchanged':sha(ARCHIVE)==input_sha,
                      'historical_installed_tree_claim':False,'forecast_metrics_computed':False,
                      'malicious_or_benign_labels_created':False},
        'schema_missing_evidence':['dependency extraction root','edge acquisition timestamp','raw deps.dev response or resolution error retention',
                                   'registry retrieval timestamp','workflow commit SHA or acquisition timestamp','workflow contents or permissions',
                                   'publisher identity','token scopes','2FA state','trusted publisher configuration history']}
    (OUT/'summary.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'output':str(OUT.relative_to(ROOT)), 'scc':output['scc'],
                      'projection_changed_packages':output['sensitivity']['projection_changed_packages'],
                      'workflow_observation':{k:v for k,v in output['workflow_observation'].items() if not isinstance(v,(list,dict))},
                      'queue_comparisons':queue_comparisons},indent=2))


if __name__ == '__main__':
    if sys.argv[1:]==['--probe-public-sources']:
        probe_public_sources()
    elif not sys.argv[1:]:
        main()
    else:
        raise SystemExit('usage: study_graph_validity.py [--probe-public-sources]')
