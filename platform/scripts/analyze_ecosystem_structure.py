#!/usr/bin/env python3
"""Produce aggregate structural and observability findings from the compressed source SQLite archive."""

from __future__ import annotations

import csv
import hashlib
import json
import math
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


def rank(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda index: values[index])
    result = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start
        while end + 1 < len(order) and values[order[end + 1]] == values[order[start]]:
            end += 1
        average = (start + 1 + end + 1) / 2
        for cursor in range(start, end + 1):
            result[order[cursor]] = average
        start = end + 1
    return result


def pearson(left: list[float], right: list[float]) -> float | None:
    if not left or len(left) != len(right):
        return None
    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)
    numerator = sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right))
    left_sum = sum((a - left_mean) ** 2 for a in left)
    right_sum = sum((b - right_mean) ** 2 for b in right)
    if left_sum == 0 or right_sum == 0:
        return None
    return numerator / math.sqrt(left_sum * right_sum)


def spearman(left: list[float], right: list[float]) -> float | None:
    return pearson(rank(left), rank(right))


def query_scalar(connection: sqlite3.Connection, query: str) -> int:
    return int(connection.execute(query).fetchone()[0])


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(
            "Usage: analyze_ecosystem_structure.py <npm_ecosystem.db.zip> <output.json> <top-maintainers.csv>"
        )

    archive_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve()
    top_maintainers_path = Path(sys.argv[3]).resolve()

    with tempfile.TemporaryDirectory(prefix="npm-ecosystem-analysis-") as temporary_directory:
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
        package_count = query_scalar(connection, "SELECT COUNT(*) FROM packages")
        metric_count = query_scalar(connection, "SELECT COUNT(*) FROM package_metrics")
        version_count = query_scalar(connection, "SELECT COUNT(*) FROM package_versions")
        advisory_count = query_scalar(connection, "SELECT COUNT(*) FROM advisories")
        dependency_count = query_scalar(connection, "SELECT COUNT(*) FROM dependencies")
        maintainer_relationship_count = query_scalar(connection, "SELECT COUNT(*) FROM package_maintainers")
        maintainer_count = query_scalar(connection, "SELECT COUNT(*) FROM maintainers")

        advisory_time_range = connection.execute(
            "SELECT MIN(published_at) AS first_published_at, MAX(published_at) AS last_published_at, COUNT(DISTINCT package_name) AS distinct_packages FROM advisories"
        ).fetchone()
        advisory_classifications = connection.execute(
            """
            SELECT COALESCE(NULLIF(TRIM(classification), ''), '(missing)') AS classification, COUNT(*) AS row_count
            FROM advisories
            GROUP BY COALESCE(NULLIF(TRIM(classification), ''), '(missing)')
            ORDER BY row_count DESC, classification ASC
            """
        ).fetchall()
        advisory_metric_overlap = query_scalar(
            connection,
            "SELECT COUNT(DISTINCT advisories.package_name) FROM advisories JOIN package_metrics ON package_metrics.package_name = advisories.package_name",
        )

        workflow_rows = connection.execute(
            """
            SELECT
              COALESCE(has_github_workflows, -1) AS has_github_workflows,
              COALESCE(fetched_workflows, -1) AS fetched_workflows,
              COUNT(*) AS row_count
            FROM package_versions
            GROUP BY COALESCE(has_github_workflows, -1), COALESCE(fetched_workflows, -1)
            ORDER BY has_github_workflows, fetched_workflows
            """
        ).fetchall()
        repository_coverage = connection.execute(
            """
            SELECT
              SUM(CASE WHEN repository_url IS NOT NULL AND TRIM(repository_url) != '' THEN 1 ELSE 0 END) AS repository_url_present,
              SUM(CASE WHEN github_owner IS NOT NULL AND TRIM(github_owner) != '' AND github_repo IS NOT NULL AND TRIM(github_repo) != '' THEN 1 ELSE 0 END) AS github_link_present
            FROM package_versions
            """
        ).fetchone()

        maintainer_rows = connection.execute(
            """
            SELECT maintainer_username AS username, COUNT(*) AS package_count
            FROM package_maintainers
            GROUP BY maintainer_username
            ORDER BY package_count DESC, maintainer_username ASC
            """
        ).fetchall()
        top_one_percent_maintainers = math.ceil(len(maintainer_rows) * 0.01)
        top_one_percent_relationships = sum(row["package_count"] for row in maintainer_rows[:top_one_percent_maintainers])

        joined_rows = connection.execute(
            """
            WITH package_maintainer_counts AS (
              SELECT package_name, COUNT(*) AS maintainer_count
              FROM package_maintainers
              GROUP BY package_name
            ), maintainer_portfolios AS (
              SELECT maintainer_username, COUNT(*) AS portfolio_size
              FROM package_maintainers
              GROUP BY maintainer_username
            ), package_max_portfolio AS (
              SELECT pm.package_name, MAX(mp.portfolio_size) AS max_maintainer_portfolio
              FROM package_maintainers pm
              JOIN maintainer_portfolios mp ON mp.maintainer_username = pm.maintainer_username
              GROUP BY pm.package_name
            )
            SELECT
              metrics.package_name,
              metrics.transitive_dependents,
              metrics.direct_dependents,
              COALESCE(counts.maintainer_count, 0) AS maintainer_count,
              COALESCE(portfolio.max_maintainer_portfolio, 0) AS max_maintainer_portfolio
            FROM package_metrics metrics
            LEFT JOIN package_maintainer_counts counts ON counts.package_name = metrics.package_name
            LEFT JOIN package_max_portfolio portfolio ON portfolio.package_name = metrics.package_name
            """
        ).fetchall()
        connection.close()

    transitive = [float(row["transitive_dependents"]) for row in joined_rows]
    direct = [float(row["direct_dependents"]) for row in joined_rows]
    package_maintainer_counts = [float(row["maintainer_count"]) for row in joined_rows]
    max_portfolios = [float(row["max_maintainer_portfolio"]) for row in joined_rows]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    top_maintainers_path.parent.mkdir(parents=True, exist_ok=True)
    with top_maintainers_path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=["rank", "maintainer_username", "package_count"])
        writer.writeheader()
        for rank_value, row in enumerate(maintainer_rows[:50], start=1):
            writer.writerow({"rank": rank_value, "maintainer_username": row["username"], "package_count": row["package_count"]})

    workflow_rows_json = [
        {
            "hasGithubWorkflows": row["has_github_workflows"],
            "fetchedWorkflows": row["fetched_workflows"],
            "rowCount": row["row_count"],
        }
        for row in workflow_rows
    ]
    profile = {
        "analysisName": "current_snapshot_ecosystem_structure_and_observability",
        "archiveName": archive_path.name,
        "archiveSha256": sha256_file(archive_path),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "Current-snapshot aggregate analysis only; package versions lack publication timestamps and therefore cannot support a strict temporal prediction evaluation by themselves.",
        "rowCounts": {
            "packages": package_count,
            "packageMetrics": metric_count,
            "packageVersions": version_count,
            "dependencies": dependency_count,
            "maintainers": maintainer_count,
            "packageMaintainerRelationships": maintainer_relationship_count,
            "advisories": advisory_count,
        },
        "repositoryObservability": {
            "packageVersionRowsWithRepositoryUrl": repository_coverage["repository_url_present"],
            "packageVersionRowsWithGitHubLink": repository_coverage["github_link_present"],
            "workflowFetchStates": workflow_rows_json,
        },
        "advisoryLabelReadiness": {
            "distinctAdvisoryPackages": advisory_time_range["distinct_packages"],
            "metricPackageOverlap": advisory_metric_overlap,
            "firstPublishedAt": advisory_time_range["first_published_at"],
            "lastPublishedAt": advisory_time_range["last_published_at"],
            "classificationCounts": [
                {"classification": row["classification"], "rowCount": row["row_count"]}
                for row in advisory_classifications
            ],
        },
        "maintainerConcentration": {
            "topMaintainerPackageCount": maintainer_rows[0]["package_count"] if maintainer_rows else 0,
            "topOnePercentMaintainerCount": top_one_percent_maintainers,
            "topOnePercentRelationshipCount": top_one_percent_relationships,
            "topOnePercentRelationshipShare": top_one_percent_relationships / maintainer_relationship_count if maintainer_relationship_count else None,
        },
        "structuralAssociations": {
            "spearman_transitive_dependents_vs_maintainer_count": spearman(transitive, package_maintainer_counts),
            "spearman_transitive_dependents_vs_max_maintainer_portfolio": spearman(transitive, max_portfolios),
            "spearman_direct_dependents_vs_maintainer_count": spearman(direct, package_maintainer_counts),
        },
        "limitations": [
            "The advisory table has no affected-version relation in this archive and is unsuitable as a primary compromise-label source without external adjudication.",
            "The package_versions table has no publication timestamp, so observed repository and workflow fields are current-snapshot observability, not cutoff-valid historical features.",
            "Maintainer usernames are registry identities and may not map one-to-one to repository, publisher, or organization authority.",
        ],
    }
    output_path.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"archiveSha256": profile["archiveSha256"], "topMaintainerPackageCount": profile["maintainerConcentration"]["topMaintainerPackageCount"]}, indent=2))


if __name__ == "__main__":
    main()
