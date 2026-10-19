# NPM Supply Chain Research

This repository contains the codebase and methodology for the academic thesis: **Predicting the Blast Radius: Forecasting High-ROI Attack Entry Points in Software Supply Chains via Graph Neural Networks**.

## Overview
This project builds a cross-domain heterogeneous graph fusing npm software dependency topologies with GitHub infrastructure CI/CD exposure data. The goal is to probabilistically forecast optimal entry points for an attacker to maximize their credential-harvesting Return on Investment (ROI).

## Project Structure

The IEEE-style paper project is in **[`manuscript/`](manuscript/README.md)**, with a compiled PDF, modular LaTeX sections, bibliography, figures, novelty assessment, and a reproducible audit. Its audit identifies inconsistencies between the supplied CSV and SQLite metrics; consult that report before combining those exports or interpreting the legacy score as a predictive result.

The repository is organized into the following directories:

- **`scripts/`**: Contains the Python scripts used for data collection and analysis.
  - `collect_data.py`: The core scraper that aggregates data from the npm registry, deps.dev API, GitHub API, and OSV vulnerabilities.
  - `check_progress.py`: A utility script for monitoring the status and completion of the data scraping queue.
  - `calculate_metrics.py`: Computes the *Wormability*, *Blast Radius*, and *Attacker ROI* metrics for the constructed supply chain graph.
- **`data/`**: (Git-ignored) Directory intended for storing datasets. 
  - The SQLite database (`npm_ecosystem.db`) containing raw nodes and edges.
  - Output metrics summaries (e.g., `metrics_summary.csv`).
- **`docs/`**: Documentation and methodology papers detailing the research background and data collection strategies.

## Execution Workflow
1. **Initialize and Seed Database:**
   ```bash
   python3 scripts/collect_data.py --init
   ```
2. **Run the Scraper (NPM Metadata & Dependencies):**
   ```bash
   python3 scripts/collect_data.py --run --loop
   ```
3. **Fetch GitHub Workflows (Requires GitHub CLI Token):**
   This uses the GraphQL API to avoid strict rate limits.
   ```bash
   export GITHUB_TOKEN=$(gh auth token)
   python3 scripts/collect_data.py --fetch-github
   ```
4. **Import OSV Advisories:**
   ```bash
   python3 scripts/collect_data.py --fetch-advisories
   ```
5. **Calculate Attacker ROI Metrics:**
   ```bash
   python3 scripts/calculate_metrics.py --top-k 100
   ```

## Metrics Formulation
- **Wormability:** The lateral propagation potential, computed as the out-degree of package maintainers.
- **Blast Radius:** The downstream infrastructure exposure, calculated as the count of transitive dependents possessing active CI/CD workflows.
- **Attacker ROI:** $\alpha \cdot \text{Wormability}_{\text{norm}} + \beta \cdot \text{BlastRadius}_{\text{norm}}$

*(Note: Data files and databases are excluded from version control due to file size constraints.)*
