#!/usr/bin/env python3
"""Verify frozen research inputs, numeric results, cohort timing and TeX links."""
from collections import defaultdict
from datetime import datetime
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import sys
import zipfile

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
RESULTS = PAPER / 'results'
failures = []
checked_hashes = 0


def check(condition, message):
    if not condition:
        failures.append(message)


def read_json(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_hash(path, expected):
    global checked_hashes
    check(path.is_file(), f'Missing evidence: {path}')
    if path.is_file():
        check(digest(path) == expected, f'Changed evidence: {path.relative_to(ROOT)}')
        checked_hashes += 1


def close(a, b):
    return math.isclose(float(a), float(b), rel_tol=1e-10, abs_tol=1e-10)


def one(rows, **conditions):
    matches = [r for r in rows if all(r.get(k) == v for k, v in conditions.items())]
    if len(matches) != 1:
        raise ValueError(f'Expected one result for {conditions}; got {len(matches)}')
    return matches[0]


# Historical cross-export audit remains supporting quality-control evidence.
audit = read_json(RESULTS / 'artifact_audit.json')
for name, expected in audit['sources_sha256'].items():
    check_hash(ROOT / name, expected)
check(not any(audit['database_recomputation_mismatches'].values()), 'Historical database metrics do not reproduce')

study_dir = RESULTS / 'structural_interventions'
manifest = read_json(study_dir / 'manifest.json')
study = read_json(study_dir / 'results.json')
for name, expected in manifest['source_sha256'].items():
    if name != 'uncompressed_sqlite':
        check_hash(ROOT / name, expected)
for name, expected in manifest['outputs_sha256'].items():
    check_hash(study_dir / name, expected)
with zipfile.ZipFile(ROOT / 'data/npm_ecosystem.db.zip') as archive:
    names = [n for n in archive.namelist() if n.endswith('.db')]
    check(len(names) == 1, 'Ambiguous SQLite source archive')
    with archive.open(names[0]) as source:
        hasher = hashlib.sha256()
        for block in iter(lambda: source.read(4 * 1024 * 1024), b''):
            hasher.update(block)
    check(hasher.hexdigest() == manifest['source_sha256']['uncompressed_sqlite'], 'Uncompressed SQLite hash changed')

budgets = (1, 5, 10, 25, 50, 100)
methods = ('portfolio', 'sum_package_reach', 'max_package_reach', 'exact_union', 'greedy_coverage')
endpoints = ('all_packages', 'workflow_packages', 'workflow_repositories', 'linked_repositories', 'workflow_checked_packages')
rows = study['deterministic_curves']
check(len(rows) == 150, 'Deterministic grid is incomplete')
for endpoint in endpoints:
    for method in methods:
        previous = (0, 0, 0)
        for budget in budgets:
            r = one(rows, endpoint=endpoint, method=method, budget=budget)
            c, p = r['covered_endpoints'], r['fully_protected_endpoints']
            pairs = study['diagnostics'][endpoint]['total_identity_endpoint_pairs']
            reachable = study['diagnostics'][endpoint]['reachable_endpoints']
            check(0 <= p <= c <= reachable, f'Invalid endpoint counts: {endpoint}/{method}/{budget}')
            check(close(r['scenario_exposure_reduction_fraction'], r['removed_identity_endpoint_pairs']/pairs), 'Scenario fraction mismatch')
            check(r['covered_but_residually_exposed_endpoints'] == c-p, 'Coverage/exclusion mismatch')
            check(r['residual_possible_endpoints'] == reachable-p, 'Residual endpoint mismatch')
            current = (c, p, r['removed_identity_endpoint_pairs'])
            check(all(a >= b for a, b in zip(current, previous)), 'Nonmonotone nested selection')
            previous = current
            best = one(rows, endpoint=endpoint, method='exact_union', budget=budget)
            check(best['removed_identity_endpoint_pairs'] >= r['removed_identity_endpoint_pairs'], 'Exact-union modular optimum violated')
    for budget in budgets:
        analytic = one(study['random_analytic_expectations'], endpoint=endpoint, budget=budget)
        check(close(analytic['expected_scenario_exposure_reduction_fraction'], budget/study['population']['identities']), 'Analytic random H differs from k/M')

with (study_dir / 'random_trials.csv').open() as source:
    random_rows = list(csv.DictReader(source))
check(len(random_rows) == 6000, 'Random trial grid incomplete')
random_groups = defaultdict(list)
keys = set()
for r in random_rows:
    seed_field = 'seed' if 'seed' in r else 'trial_seed'
    key = (r['endpoint'], int(r['budget']), int(r[seed_field]))
    check(key not in keys, 'Duplicate random budget row')
    keys.add(key)
    random_groups[key[:2]].append(r)
for endpoint in endpoints:
    for budget in budgets:
        rs = random_groups[endpoint, budget]
        check(len(rs) == 200, 'Missing random orders')
        summary = one(study['random_summary'], endpoint=endpoint, budget=budget)
        for field in ('covered_endpoints', 'fully_protected_endpoints', 'scenario_exposure_reduction_fraction'):
            check(close(statistics.mean(float(r[field]) for r in rs), summary[field+'_mean']), f'Random mean mismatch: {endpoint}/{budget}/{field}')

validity = read_json(RESULTS / 'graph_validity/summary.json')
for name, expected in validity['sources_sha256'].items():
    check_hash(ROOT / name, expected)
check(validity['sensitivity']['projection_changed_packages'] == 8587, 'Changed graph sensitivity count')
check(validity['validation']['all_version_continuous_sets_subset_of_package_projected_sets'], 'Version continuity subset check failed')
scope = read_json(RESULTS / 'graph_validity/identifier_scope.json')
for name, expected in scope['source_sha256'].items():
    check_hash(ROOT / name, expected)
check(scope['graph_identifier_count'] == 25228 and scope['context_marker_identifier_count'] == 2745,
      'Identifier-scope counts changed')
check(scope['primary_workflow_repository_incidence_identical_after_context_removal'],
      'Context-removal repository incidence result changed')
profile_path = study_dir / 'performance_profile.json'
if profile_path.exists():
    profile = read_json(profile_path)
    for name, expected in profile['source_sha256'].items():
        check_hash(ROOT / name, expected)
    check(profile['reference_results_sha256'] == digest(study_dir / 'results.json'), 'Profile measured different scientific results')
    check(len(profile['repetitions']) == 3 and all(r['scientific_results_equal_frozen'] for r in profile['repetitions']),
          'Incomplete replicated resource profile')
independent = read_json(study_dir / 'independent_validation.json')
check(independent['random_graph_trials'] == 60 and independent['independently_checked_graph_roots'] == 675, 'Independent graph checks incomplete')

# Frozen acquisition is not a labeled prediction benchmark.
cohort_dir = RESULTS / 'prospective_cohort'
cohort = read_json(cohort_dir / 'cohort_status.json')
selection = read_json(cohort_dir / 'selection_manifest.json')
check_hash(cohort_dir / 'capture_records.jsonl', cohort['capture_records_sha256'])
check_hash(cohort_dir / 'selection_manifest.json', cohort['selection_manifest_sha256'])
captures = [json.loads(line) for line in (cohort_dir / 'capture_records.jsonl').read_text().splitlines()]
check(len(captures) == 100 and len(set(selection['selected_package_names'])) == 100, 'Frozen cohort size changed')
check({r['package_name'] for r in captures} == set(selection['selected_package_names']), 'Cohort membership changed')
check(all(r['outcome_status'] == 'pending' and r['documented_publisher_compromise'] is None for r in captures), 'Acquisition assigned outcome labels')
parse_time = datetime.fromisoformat
check(parse_time(selection['selection_frozen_at_utc']) < min(parse_time(r['request_started_at_utc']) for r in captures), 'Selection did not precede acquisition')
check(parse_time(cohort['feature_cutoff_utc']) == max(parse_time(r['response_finished_at_utc']) for r in captures), 'Cutoff differs from final capture')
check((parse_time(cohort['outcome_horizon_end_utc'])-parse_time(cohort['feature_cutoff_utc'])).days == 90, 'Incorrect prospective horizon')
check(cohort['successful_metadata_rows'] == 90 and cohort['models_fit'] == 0 and cohort['pending_outcomes'] == 100, 'Prospective status mismatch')

# Check generated numbers against the scientific results, not manually typed prose.
greedy = one(rows, endpoint='workflow_repositories', method='greedy_coverage', budget=100)
exact = one(rows, endpoint='workflow_repositories', method='exact_union', budget=100)
pop = study['population']
pairs = study['diagnostics']['workflow_repositories']['total_identity_endpoint_pairs']
vpairs = study['version_representation']['workflow_repositories']['total_identity_endpoint_pairs']
expected_macros = {
    'StudyPackages': f"{pop['packages']:,}", 'StudyMaintainers': f"{pop['identities']:,}",
    'StudyWorkflowPackages': f"{pop['workflow_positive_packages']:,}", 'StudyWorkflowRepos': f"{pop['workflow_positive_repositories']:,}",
    'GreedyCovered': f"{greedy['covered_endpoints']:,}", 'GreedyCoveragePercent': f"{100*greedy['coverage_fraction_observed']:.1f}",
    'GreedyExposurePercent': f"{100*greedy['scenario_exposure_reduction_fraction']:.2f}",
    'UnionCovered': f"{exact['covered_endpoints']:,}", 'UnionExposurePercent': f"{100*exact['scenario_exposure_reduction_fraction']:.2f}",
    'GreedyExcluded': f"{greedy['fully_protected_endpoints']:,}", 'VersionPairsDecreasePercent': f"{100*(1-vpairs/pairs):.2f}",
    'ChangedRoots': f"{study['version_representation']['package_roots_with_changed_reach']:,}"}
macros = (RESULTS / 'research_numbers.tex').read_text()
for name, value in expected_macros.items():
    check('\\newcommand{\\'+name+'}{'+value+'}' in macros, f'Stale generated macro: {name}')
tex_rows = (RESULTS / 'research_method_rows.tex').read_text()
for method in methods:
    r = one(rows, endpoint='workflow_repositories', method=method, budget=100)
    values = f"& {r['covered_endpoints']:,} & {100*r['coverage_fraction_observed']:.1f} & {100*r['scenario_exposure_reduction_fraction']:.2f} & {r['fully_protected_endpoints']:,}"
    check(values in tex_rows, f'Stale method table: {method}')

# Task 15: residual increments and strict thresholds have different definitions.
modern = read_json(RESULTS / 'conference_modernization.json')
for relative, expected in modern['source_sha256'].items():
    check_hash(ROOT / relative, expected)
check(modern['T2_empty'] == 1716 and modern['P2_strict_empty'] == 0, 'Threshold baselines conflated')
for prefix, expected in [('Greedy', (2112,396,1145)), ('Exact', (2137,421,793)), ('Pareto', (2153,437,961))]:
    row = next(row for row in modern['budget100'] if row['strategy'].startswith(prefix))
    check((row['T2'],row['delta_T2'],row['P2_strict']) == expected, f'Task 15 threshold mismatch: {prefix}')
    check(close(row['H_eta_090_pct'], 0.9*row['H_pct']), 'Efficacy scaling mismatch')

visited = set()

def tex_tree(relative):
    if relative in visited:
        return ''
    visited.add(relative)
    path = PAPER / (relative + '.tex')
    check(path.is_file(), f'Missing active TeX input: {relative}')
    if not path.is_file():
        return ''
    content = path.read_text()
    return content + '\n' + '\n'.join(tex_tree(child) for child in re.findall(r'\\input\{([^}]+)\}', content))

content = tex_tree('main')
bib = (PAPER / 'bibliography/references.bib').read_text()
keys = set(re.findall(r'@\w+\s*\{\s*([^,]+),', bib))
citations = {key.strip() for block in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', content) for key in block.split(',')}
required_modern_citations = {'npmtrustedpub2026','npmexpiry2026','opencode2026','litellm2026',
    'litellmincident2026','railway2026','railwaydisclosure2026','nodejsbrotli2026',
    'gao2025emse','okafor2025','weeraddana2024','jayasuriya2024'}
check(required_modern_citations <= citations, 'Missing Task 15 primary or academic citations')
for key in citations-keys:
    check(False, f'Undefined citation: {key}')
for relative in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', content):
    check((PAPER / 'figures' / relative).is_file(), f'Missing active figure: {relative}')
figure_manifest = read_json(RESULTS / 'figure_manifest.json')
for field in ('inputs_sha256', 'scripts_sha256'):
    for name, expected in figure_manifest[field].items():
        check_hash(ROOT / name, expected)
for name, expected in figure_manifest['outputs_sha256'].items():
    check_hash(PAPER / name, expected)
check(sum(f['in_paper'] for f in figure_manifest['figures'].values()) == 4, 'Unexpected main figure count')
figure_data = read_json(RESULTS / 'analysis_figure_data.json')
for row in figure_data['figures']['coverage_partition']['segments']:
    r = one(rows, endpoint='workflow_repositories', method=row['method'], budget=100)
    check(row['all_sources_selected'] == r['fully_protected_endpoints'] and row['covered_total'] == r['covered_endpoints'],
          'Source-partition figure disagrees with research')
    check(row['all_sources_selected'] + row['other_covered'] + row['uncovered_reachable'] + row['no_observed_source_excluded'] == 7171,
          'Source-partition figure does not conserve observed repository count')
prose = '\n'.join(p.read_text() for p in (PAPER / 'sections').glob('*.tex'))
check(not re.search(r'given SQL|supplied artifacts|provided repository|at the platform', prose, re.I), 'External-review framing remains in paper')

report = {'source_and_output_hashes_checked': checked_hashes, 'deterministic_budget_rows': len(rows),
    'random_budget_rows': len(random_rows), 'active_citation_count': len(citations),
    'active_tex_inputs': sorted(visited), 'generated_macros_checked': len(expected_macros),
    'cohort_records': len(captures), 'cohort_outcomes_pending': 100,
    'conference_modernization_checked': True, 'identifier_scope_checked': True, 'resource_profile_checked': profile_path.exists(),
    'figure_provenance_checked': True, 'active_figure_count': 4,
    'checks_pass': not failures, 'failures': failures,
    'scope': 'Technical evidence consistency; does not certify authorship, venue policy, prediction validity or real control efficacy.'}
(RESULTS / 'research_verification.json').write_text(json.dumps(report, indent=2)+'\n')
if failures:
    print('\n'.join(failures), file=sys.stderr)
    sys.exit(1)
print(f"Verified {checked_hashes} hashes, {len(rows)} deterministic/{len(random_rows)} random rows, {len(citations)} active citations, generated values and frozen cohort timing.")
