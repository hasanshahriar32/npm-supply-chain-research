#!/usr/bin/env python3
"""Portable alternative to the connected GitHub tool bridge for future GET captures.

Existing observations are never overwritten. Credentials stay in memory and are
sent only to api.github.com; they are never written into evidence records.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.parse
import urllib.request
import urllib.error

from journal_revision_common import dump, stamp


def main():
    ap=argparse.ArgumentParser();ap.add_argument('requests',type=Path);args=ap.parse_args()
    requests=json.loads(args.requests.read_text());folder=args.requests.parent/'github_responses'
    folder.mkdir(exist_ok=True)
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        result=subprocess.run(['gh','auth','token'],text=True,capture_output=True)
        token=result.stdout.strip() if result.returncode==0 else None
    def capture(req):
        key=req['key']
        if not re.fullmatch(r'[AR]\d{3}__(?:commit|root|workflows|file_[0-9a-f]{16})',key):
            raise ValueError('Invalid generated evidence key')
        target=folder/(key+'.json')
        if target.exists():return 'cached'
        url=req['url'];parts=urllib.parse.urlsplit(url)
        if parts.scheme!='https' or parts.hostname not in ['api.github.com','github.com','raw.githubusercontent.com']:
            raise ValueError('Only public GitHub HTTPS resource hosts are supported')
        headers={'User-Agent':'npm-research-evidence/1'}
        if parts.hostname=='api.github.com' and token:headers['Authorization']='Bearer '+token
        record={'request':req,'observed_at_utc':stamp(),'content':None,'is_error':True}
        for attempt in range(2):
            record['attempts']=attempt+1
            try:
                with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=25) as response:
                    raw=response.read(8000000);record['http_status']=response.status
                body=raw.decode('utf-8');record['source_response_sha256']=hashlib.sha256(raw).hexdigest()
                if key.endswith('__commit'):
                    obj=json.loads(body)
                    if isinstance(obj,list):
                        body=json.dumps([{'sha':x.get('sha'),'html_url':x.get('html_url'),
                            'commit':{'tree':x.get('commit',{}).get('tree'),
                            'committed_at':x.get('commit',{}).get('committer',{}).get('date')}} for x in obj])
                record.update(content=body,is_error=False)
                break
            except urllib.error.HTTPError as error:
                record['http_status']=error.code
                if error.code not in [429,500,502,503,504]:break
            except (urllib.error.URLError,TimeoutError,UnicodeError,ValueError) as error:
                record['error_type']=type(error).__name__
        dump(target,record)
        return 'captured' if not record['is_error'] else 'unresolved'
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs=[pool.submit(capture,req) for req in requests]
        for i,future in enumerate(as_completed(jobs),1):
            future.result()
            if i%20==0:print('Processed',i,'of',len(jobs),flush=True)
    print('Completed; unresolved requests retained and no selected units replaced.')


if __name__=='__main__':main()
