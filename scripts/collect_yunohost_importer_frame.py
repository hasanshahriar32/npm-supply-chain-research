#!/usr/bin/env python3
"""Read frozen YunoHost packaging recipe files at public catalog revisions."""
import base64
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys

from collect_yunohost_observations import fetch, now, sha256
from collect_yunohost_packaging import url_for

FILES = ("manifest.toml", "manifest.json", "scripts/install", "scripts/upgrade", "scripts/_common.sh",
         "conf/systemd.service")


def observe(row):
    files = {}
    for path in FILES:
        receipt, body = fetch(url_for(row, path), 512_000)
        if body is not None:
            receipt["body_base64"] = base64.b64encode(body).decode()
        files[path] = receipt
    return {**row, "files": files}


if __name__ == "__main__":
    payload = Path(sys.argv[1]).read_bytes()
    rows = json.loads(payload)["projects"]
    if len(rows) != 99 or len({r["upstream"] for r in rows}) != len(rows):
        raise ValueError("Unexpected frozen sample")
    with ThreadPoolExecutor(max_workers=8) as pool:
        observations = list(pool.map(observe, rows))
    print(json.dumps({"queue_sha256": sha256(payload).hexdigest(), "finished_utc": now(),
                      "observations": observations}, separators=(",", ":")))
