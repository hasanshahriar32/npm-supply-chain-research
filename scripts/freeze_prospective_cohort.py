#!/usr/bin/env python3
"""Freeze a seeded prospective cohort using official npm metadata only.

Selection is saved before requests. Metadata responses are allowlisted into
features: no email addresses, package payloads, install-script text, or tokens are
retained. All outcome fields are explicitly pending, never zero/benign labels.
This is data collection for a future study, not a completed forecast experiment.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import random
import re
import shutil
import sqlite3
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / 'manuscript/results/prospective_cohort'
MAX_BYTES = 1048576
LOCAL_ZONE = timezone(timedelta(hours=6))


def stamp():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')


def repo_key(value):
    if isinstance(value, dict):
        value = value.get('url')
    if not isinstance(value, str):
        return None
    value = value.replace('git+', '', 1)
    if value.startswith('github:'):
        value='https://github.com/'+value[len('github:'):]
    match = re.search(r'(?:^|[/@])github\.com[:/]([^/#?]+)/([^/#?]+)', value, re.I)
    if match:
        owner,repo=match.groups()
        if repo.endswith('.git'):
            repo=repo[:-4]
        return owner.casefold()+'/'+repo.casefold()
    return None


def features(data):
    dist = data.get('dist') if isinstance(data.get('dist'), dict) else {}
    scripts = data.get('scripts') if isinstance(data.get('scripts'), dict) else {}
    maintainers=data.get('maintainers') if isinstance(data.get('maintainers'), list) else []
    publisher=data.get('_npmUser') if isinstance(data.get('_npmUser'),dict) else {}
    attestations=dist.get('attestations') if isinstance(dist.get('attestations'),dict) else {}
    return {
        'observed_name':data.get('name'),'observed_version':data.get('version'),
        'github_repository_key':repo_key(data.get('repository')),
        'maintainer_count':len(maintainers),
        'maintainer_usernames':sorted({m['name'] for m in maintainers if isinstance(m,dict) and isinstance(m.get('name'),str)}),
        'version_publisher_username':publisher.get('name'),
        'runtime_dependency_count':len(data.get('dependencies',{})) if isinstance(data.get('dependencies',{}),dict) else None,
        'optional_dependency_count':len(data.get('optionalDependencies',{})) if isinstance(data.get('optionalDependencies',{}),dict) else None,
        'peer_dependency_count':len(data.get('peerDependencies',{})) if isinstance(data.get('peerDependencies',{}),dict) else None,
        'development_dependency_count':len(data.get('devDependencies',{})) if isinstance(data.get('devDependencies',{}),dict) else None,
        'has_install_lifecycle_script':any(key in scripts for key in ['preinstall','install','postinstall']),
        'has_deprecation_notice':bool(data.get('deprecated')),
        'dist_integrity':dist.get('integrity'),'dist_file_count':dist.get('fileCount'),
        'dist_unpacked_size':dist.get('unpackedSize'),
        'dist_signature_count':len(dist.get('signatures',[])) if isinstance(dist.get('signatures',[]),list) else None,
        'has_attestation_metadata':bool(attestations),
        'provenance_predicate_type':attestations.get('provenance',{}).get('predicateType') if isinstance(attestations.get('provenance'),dict) else None,
    }


def fetch(package):
    url='https://registry.npmjs.org/'+urllib.parse.quote(package,safe='')+'/latest'
    result={'package_name':package,'url':url,'method':'GET','request_started_at_utc':stamp(),
            'outcome_status':'pending','documented_publisher_compromise':None,
            'outcome_event_time_utc':None,'outcome_source':None}
    attempts=[]
    for attempt in range(2):
        request=urllib.request.Request(url,headers={'User-Agent':'npm-supply-chain-prospective-research/1.0','Accept':'application/json'})
        try:
            with urllib.request.urlopen(request,timeout=15) as response:
                body=response.read(MAX_BYTES+1)
                entry={'http_status':response.status,'response_bytes':len(body),
                       'response_sha256':hashlib.sha256(body).hexdigest(),
                       'server_date':response.headers.get('Date'),'response_finished_at_utc':stamp()}
                attempts.append(entry)
                result.update(entry)
                if len(body)>MAX_BYTES:
                    result['capture_status']='response_exceeded_bound'
                else:
                    data=json.loads(body)
                    if data.get('name')!=package:
                        result['capture_status']='response_package_name_mismatch'
                    else:
                        result['capture_status']='metadata_captured'
                        result['features']=features(data)
                break
        except urllib.error.HTTPError as error:
            entry={'http_status':error.code,'response_finished_at_utc':stamp(),'error':type(error).__name__}
            attempts.append(entry)
            result.update(entry)
            result['capture_status']='metadata_unavailable'
            if error.code not in [429,500,502,503,504] or attempt:
                break
            time.sleep(1)
        except Exception as error:
            entry={'http_status':None,'response_finished_at_utc':stamp(),'error':type(error).__name__,'reason':str(error)}
            attempts.append(entry)
            result.update(entry)
            result['capture_status']='request_failed'
            if attempt:
                break
            time.sleep(1)
    result['attempts']=attempts
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--size',type=int,default=100)
    parser.add_argument('--seed',type=int,default=20261020)
    parser.add_argument('--output',type=Path,default=DEFAULT_OUT)
    parser.add_argument('--delay',type=float,default=.2)
    args=parser.parse_args()
    if args.size<1 or args.delay<.2:
        parser.error('size must be positive and request delay at least 0.2 seconds')
    args.output.mkdir(parents=True,exist_ok=True)
    manifest_path=args.output/'selection_manifest.json'
    if manifest_path.exists():
        raise SystemExit('Selection manifest already exists; the frozen collection will not be overwritten. Choose another output folder for a new wave.')
    archive=ROOT/'data/npm_ecosystem.db.zip'
    with tempfile.TemporaryDirectory(prefix='npm-prospective-selection-') as temp:
        database=Path(temp)/'snapshot.db'
        with zipfile.ZipFile(archive) as z,z.open('npm_ecosystem.db') as source,database.open('wb') as dest:
            shutil.copyfileobj(source,dest)
        connection=sqlite3.connect(f'file:{database}?mode=ro&immutable=1',uri=True)
        population=[r[0] for r in connection.execute('SELECT name FROM packages ORDER BY name')]
        connection.close()
    if args.size>len(population):
        raise SystemExit('Requested cohort is larger than the source population')
    selected=sorted(random.Random(args.seed).sample(population,args.size))
    manifest={'study':'prospective-current-metadata-feasibility-cohort',
              'selection_frozen_at_utc':stamp(),'selection_frozen_at_asia_dhaka':datetime.now(LOCAL_ZONE).isoformat(),
              'source_archive':'data/npm_ecosystem.db.zip','source_archive_sha256':digest(archive),
              'sampling_population':'All package names in the immutable original snapshot, including unavailable metadata rows.',
              'population_size':len(population),'population_order':'SQLite ORDER BY name, binary collation',
              'sampling_method':'Uniform sampling without replacement using Python random.Random(seed).sample; selected names sorted before fetching.',
              'python_random_seed':args.seed,'sample_size':args.size,'selected_package_names':selected,
              'selection_before_first_network_request':True,
              'sampling_inclusion_probability':args.size/len(population),
              'capture_endpoint':'https://registry.npmjs.org/<percent-encoded-name>/latest',
              'target_outcome':'A publicly documented unauthorized publication or release-pipeline compromise affecting the sampled established package during the follow-up interval; ordinary accidental vulnerabilities and unrelated typosquats do not satisfy this target.',
              'outcome_horizon_days':90,'all_outcomes_initially_pending':True,
              'label_semantics':'Future absence of a report means no documented event under the registered source/surveillance procedure, not certified benignness. Unknown or incomplete coverage remains unknown.',
              'surveillance_design_status':'Feasibility cohort frozen; final source freeze, event adjudication protocol and analysis plan remain to be finalized before outcomes are examined.',
              'no_model_has_been_trained_or_evaluated':True,
              'source_manifest_sha256':digest(Path(__file__))}
    dump(manifest_path,manifest)
    records=[]
    with (args.output/'capture_records.jsonl').open('w') as handle:
        for index,package in enumerate(selected):
            row=fetch(package)
            handle.write(json.dumps(row,sort_keys=True)+'\n')
            handle.flush()
            records.append(row)
            if (index+1)%10==0:
                print(f'Captured {index+1}/{len(selected)} package responses',flush=True)
            if index+1<len(selected):
                time.sleep(args.delay)
    finished=datetime.fromisoformat(max(r['response_finished_at_utc'] for r in records))
    end=finished+timedelta(days=90)
    report={'study':manifest['study'],'selection_manifest_sha256':digest(manifest_path),
            'capture_records_sha256':digest(args.output/'capture_records.jsonl'),
            'feature_cutoff_utc':finished.isoformat(),'feature_cutoff_asia_dhaka':finished.astimezone(LOCAL_ZONE).isoformat(),
            'outcome_interval':'(feature_cutoff, feature_cutoff + 90 days]',
            'outcome_horizon_end_utc':end.isoformat(),'outcome_horizon_end_asia_dhaka':end.astimezone(LOCAL_ZONE).isoformat(),
            'source_population_size':len(population),'cohort_size':len(records),
            'capture_status_counts':dict(Counter(r['capture_status'] for r in records)),
            'http_status_counts':dict(Counter(str(r['http_status']) for r in records)),
            'successful_metadata_rows':sum(r['capture_status']=='metadata_captured' for r in records),
            'pending_outcomes':len(records),'positive_outcomes_assigned':0,'negative_outcomes_assigned':0,
            'probabilities_predicted':0,'models_fit':0,'forecast_performance_computed':False,
            'raw_metadata_bodies_retained':False,'email_addresses_retained':False,
            'package_payloads_downloaded_or_executed':0,
            'limitations':['Small feasibility sample; no power claim or expected event yield.',
                           'The sampling frame is the existing historical high-impact-seeded expansion, not all npm packages today.',
                           'Archive features, if later joined, are stale structural measurements first available to this study at the freeze cutoff; their original observation dates are not inferred.',
                           'The latest endpoint provides retained version metadata, not the complete historical account or workflow state.',
                           'Outcome surveillance sources and censoring rules must be fixed before future outcomes are examined.',
                           'No currently missing record is labeled safe, benign, or uncompromised.']}
    dump(args.output/'cohort_status.json',report)
    (args.output/'README.md').write_text(
        '# Prospective cohort feasibility freeze\n\n'
        f'A uniform seeded sample of {len(records)} package names was selected before metadata requests. '
        f'Official npm metadata was captured for {report["successful_metadata_rows"]} packages. '
        'The other request outcomes are retained as missingness, without replacement or relabeling.\n\n'
        f'Feature cutoff: **{report["feature_cutoff_asia_dhaka"]}** (Asia/Dhaka). '
        f'The 90-day interval ends **{report["outcome_horizon_end_asia_dhaka"]}**. '
        'All outcomes are pending. No model was fitted and no forecasting performance exists.\n\n'
        '`selection_manifest.json` fixes the sampling frame, seed and selected names before requests. '
        '`capture_records.jsonl` contains status, capture times, response hashes and allowlisted metadata features. '
        '`cohort_status.json` fixes the exact collection cutoff and follow-up interval. Raw responses, emails, '
        'tarballs and install-script bodies are not retained.\n\n'
        'This is a completed data-acquisition feasibility step. It is not a preregistered powered benchmark: '
        'final surveillance sources, censoring rules and analysis plan still require freezing before follow-up '
        'outcomes are examined. Absence from an advisory feed never certifies a package benign.\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
