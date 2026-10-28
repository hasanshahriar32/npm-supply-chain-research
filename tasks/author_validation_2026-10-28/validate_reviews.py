"""Read-only check of task-sheet identity, allowed values and completeness.

Does not infer labels, compute agreement, modify sheets, or certify the review.
"""
from pathlib import Path
import csv
import json

HERE = Path(__file__).resolve().parent
LABELS = ['repository_mapping_supported', 'workflow_file_present',
          'install_directive_observed', 'lockfile_present', 'dependency_version_supported']


def main():
    frame = json.loads((HERE / 'task_manifest.json').read_text())['review_identity_rows']
    identity = {r['audit_id']: r for r in frame}
    reports = []
    for name in ['Shahriar_Hasan', 'Md_Ashikul_Islam']:
        path = HERE / 'reviews' / (name + '_independent_labels.csv')
        with path.open(newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames
            rows = list(reader)
        issues = []
        expected = ['audit_id', 'repository', 'commit_sha', *LABELS, 'evidence_notes']
        if fields != expected:
            issues.append('Header does not match the provided template.')
        ids = [r.get('audit_id') for r in rows]
        if len(rows) != 120 or len(set(ids)) != 120 or set(ids) != set(identity):
            issues.append('Expected exactly the 120 original audit IDs, without duplicates.')
        complete = 0
        for row in rows:
            aid = row.get('audit_id')
            if aid not in identity:
                continue
            for key in ['repository', 'commit_sha']:
                if row.get(key) != identity[aid][key]:
                    issues.append(f'{aid}: identity mismatch in {key}.')
            values = [(row.get(key) or '').strip().lower() for key in LABELS]
            if any(value not in ['', 'supported', 'unsupported', 'unknown'] for value in values):
                issues.append(f'{aid}: invalid label value.')
            if all(value in ['supported', 'unsupported', 'unknown'] for value in values):
                if (row.get('evidence_notes') or '').strip():
                    complete += 1
                else:
                    issues.append(f'{aid}: missing evidence notes.')
        reports.append({'author_sheet': name, 'complete_rows_with_notes': complete,
                        'expected_rows': 120, 'structure_issues': issues,
                        'ready_for_handoff_structure_only': complete == 120 and not issues})
    print(json.dumps({'reports': reports,
                      'scope': 'File structure and completeness only; no agreement calculated and no review certified.'}, indent=2))


if __name__ == '__main__':
    main()
