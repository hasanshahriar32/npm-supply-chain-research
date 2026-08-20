#!/usr/bin/env python3
"""Profile the repository's compressed SQLite source archive without retaining it in the web project."""

from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: profile_ecosystem_archive.py <npm_ecosystem.db.zip> <output.json>")

    archive_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve()

    with tempfile.TemporaryDirectory(prefix="npm-ecosystem-profile-") as temporary_directory:
        temporary_path = Path(temporary_directory)
        with zipfile.ZipFile(archive_path) as archive:
            database_entry = next((entry for entry in archive.namelist() if entry.endswith(".db")), None)
            if database_entry is None:
                raise RuntimeError("No SQLite database entry found in the archive")
            database_path = temporary_path / Path(database_entry).name
            with archive.open(database_entry) as source, database_path.open("wb") as destination:
                shutil.copyfileobj(source, destination)

        connection = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()

        table_profile = []
        for table_row in tables:
            table_name = table_row["name"]
            escaped_name = table_name.replace('"', '""')
            columns = connection.execute(f'PRAGMA table_info("{escaped_name}")').fetchall()
            count = connection.execute(f'SELECT COUNT(*) AS count FROM "{escaped_name}"').fetchone()["count"]
            table_profile.append(
                {
                    "name": table_name,
                    "rowCount": count,
                    "columns": [
                        {
                            "name": column["name"],
                            "type": column["type"],
                            "notNull": bool(column["notnull"]),
                            "primaryKey": bool(column["pk"]),
                        }
                        for column in columns
                    ],
                }
            )
        connection.close()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    profile = {
        "analysisName": "ecosystem_archive_schema_profile",
        "archiveName": archive_path.name,
        "archiveSha256": sha256_file(archive_path),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "tables": table_profile,
        "notes": [
            "This profile records only schema and aggregate row counts.",
            "The SQLite source archive is not copied into the deployable web project.",
            "Any historical feature claim still requires a dated source and a feature-availability rule.",
        ],
    }
    output_path.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"tableCount": len(table_profile), "archiveSha256": profile["archiveSha256"]}, indent=2))


if __name__ == "__main__":
    main()
