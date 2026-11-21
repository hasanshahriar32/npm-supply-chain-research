#!/usr/bin/env python3
"""Reacquire the two checksum-pinned release archives for offline module inspection."""
import argparse
import base64
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from urllib.request import Request, build_opener

from collect_yunohost_observations import fetch, now
from collect_yunohost_release_archive_evidence import CAP, ReleaseRedirect

PANEL = "pterodactyl/panel"
GIT_SHA = re.compile(r"[a-f0-9]{40}")


def collect(row):
    url = urlsplit(row["url"])
    if (url.scheme != "https" or url.netloc != "github.com" or "/releases/download/" not in url.path
            or url.query or url.fragment):
        raise ValueError("Unexpected archive URL")
    ordered_at = now()
    with build_opener(ReleaseRedirect()).open(Request(row["url"], headers={"User-Agent": "npm-consumer-study/1"}),
                                              timeout=35) as response:
        body = response.read(CAP + 1)
    digest = sha256(body).hexdigest()
    if len(body) > CAP or digest != row["recipe_sha256"]:
        raise ValueError("Archive cap or recipe checksum check failed")
    return {"request": row, "observed_at_utc": ordered_at, "sha256": digest, "size": len(body),
            "body": base64.b64encode(body).decode()}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("queue", type=Path)
    args = cli.parse_args()
    raw = args.queue.read_bytes()
    queue = json.loads(raw)
    if len(queue["requests"]) != 2 or not GIT_SHA.fullmatch(queue["panel_commit"]):
        raise ValueError("Unexpected release input scope")
    rows = [collect(row) for row in queue["requests"]]
    path = f"https://raw.githubusercontent.com/{PANEL}/{queue['panel_commit']}/webpack.config.js"
    config, content = fetch(path, 512_000)
    if content is not None:
        config["body"] = base64.b64encode(content).decode()
    print(json.dumps({"queue_sha256": sha256(raw).hexdigest(), "finished_utc": now(), "archives": rows,
                      "webpack_config": config}, separators=(",", ":")))
