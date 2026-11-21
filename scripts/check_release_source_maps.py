#!/usr/bin/env python3
"""Classify source-map text in checksummed release bundles using a static JS parse."""
import gzip
import io
import json
from pathlib import PurePosixPath
import subprocess
import tarfile

from study_release_module_evidence import CAPTURE, MANIFEST, RUN, UNPACKED_CAP, archives, digest, read, sha, write
from verify_yunohost_deployment_archives import ByteLimit

PARSE = r"""
const fs = require('node:fs');
const acorn = require('internal/deps/acorn/acorn/dist/acorn');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const rows = [];
for (const [path, code] of Object.entries(input)) {
    const comments = [];
    const tokens = [];
    const onComment = (_block, text) => {
        if (text.includes('sourceMappingURL')) comments.push(text);
    };
    const onToken = token => {
        if (code.slice(token.start, token.end).includes('sourceMappingURL'))
            tokens.push(token.type.label);
    };
    acorn.parse(code, {ecmaVersion: 'latest', sourceType: 'script', onComment, onToken});
    rows.push({
        file: path,
        annotation_comments: comments.filter(text => /^[#@]\s*sourceMappingURL\s*=/.test(text.trim())).length,
        other_comments: comments.filter(text => !/^[#@]\s*sourceMappingURL\s*=/.test(text.trim())).length,
        token_classes: tokens,
    });
}
console.log(JSON.stringify({parser: acorn.version, node: process.version, rows}));
"""


def check():
    inputs, _, _ = archives()
    manifest = read(MANIFEST)
    assert manifest["archive_receipts_sha256"] == sha(CAPTURE)
    expected = {row["file"]: row for row in manifest["panel"]["assets"]}
    buffers = {}
    with gzip.GzipFile(fileobj=io.BytesIO(inputs["D095"])) as stream:
        with tarfile.open(fileobj=ByteLimit(stream, UNPACKED_CAP), mode="r|") as archive:
            for item in archive:
                key = str(PurePosixPath(item.name))
                if key not in expected:
                    continue
                assert item.isreg() and key not in buffers
                with archive.extractfile(item) as source:
                    body = source.read()
                assert digest(body) == expected[key]["sha256"]
                buffers[key] = body.decode()
    assert buffers.keys() == expected.keys()
    process = subprocess.run(["node", "--expose-internals", "-e", PARSE], input=json.dumps(buffers), text=True,
                             capture_output=True, check=True, timeout=60)
    output = json.loads(process.stdout)
    for row in output["rows"]:
        counted = row["annotation_comments"] + row["other_comments"] + len(row["token_classes"])
        if counted != expected[row["file"]]["source_mapping_url_markers"]:
            raise ValueError(f"Source-map marker count disagrees with the parser in {row}")
    write(RUN / "static_bundle_parser.json", {"module_inputs_sha256": sha(MANIFEST), **output})
    print("Parsed", len(output["rows"]), "files")
    print("Source map directives", sum(row["annotation_comments"] for row in output["rows"]))
    print("Marker token classes", [token for row in output["rows"] for token in row["token_classes"]])


if __name__ == "__main__":
    check()
