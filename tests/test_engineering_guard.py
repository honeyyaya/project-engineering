import copy
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import engineering_guard as guard


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        path = guard.init_project(self.project, 'qt-project', 'new_project', ['queue', 'concurrency'])
        self.data = guard.read_yaml(path)
        self.note = self.project / 'evidence.txt'
        self.note.write_text('Synthetic evidence for gate engine tests only.', encoding='utf-8')
        self.evidence = [{'path': 'evidence.txt', 'sha256': hashlib.sha256(self.note.read_bytes()).hexdigest()}]

    def complete(self):
        _, risks, gates, _, _ = guard.configuration()
        for gate in gates.values():
            for name in gate['artifacts']:
                self.data['artifacts'].append({'id': name, 'revision': 'initial', 'evidence': self.evidence})
        for risk in risks.values():
            for phase in risk['stages']:
                self.data['checks'].append({'stage': phase, 'risk_id': risk['id'], 'revision': 'initial',
                    'status': 'passed', 'reason': 'Synthetic test decision.', 'evidence': self.evidence,
                    'discovered_by': risk['owner'], 'components': []})

    def test_empty_project_is_unverified(self):
        result = guard.evaluate(self.project, self.data)
        self.assertEqual('blocked', result['status'])
        self.assertTrue(any('unverified' in r for r in result['gates'][0]['reasons']))

    def test_init_never_overwrites_existing_record(self):
        before = (self.project / guard.RECORD).read_bytes()
        with self.assertRaises(ValueError):
            guard.init_project(self.project, 'qt-project', 'new_project', [])
        self.assertEqual(before, (self.project / guard.RECORD).read_bytes())

    def test_complete_record_passes(self):
        self.complete()
        self.assertEqual('passed', guard.evaluate(self.project, self.data, 'delivery')['status'])

    def test_missing_predecessor_blocks_delivery(self):
        self.complete()
        self.data['checks'] = [c for c in self.data['checks'] if c['stage'] != 'requirement']
        self.assertEqual('blocked', guard.evaluate(self.project, self.data, 'delivery')['status'])

    def test_changed_evidence_invalidates_pass(self):
        self.complete()
        self.note.write_text('Changed after review', encoding='utf-8')
        result = guard.evaluate(self.project, self.data)
        self.assertEqual('blocked', result['status'])
        self.assertTrue(any('changed evidence' in r for r in result['gates'][0]['reasons']))

    def test_revision_change_invalidates_prior_checks(self):
        self.complete()
        self.data['project']['revision'] = 'new-working-state'
        self.assertEqual('blocked', guard.evaluate(self.project, self.data)['status'])

    def test_not_applicable_requires_evidence_and_reason(self):
        self.complete()
        check = next(c for c in self.data['checks'] if c['risk_id'] == 'REQ-001' and c['stage'] == 'requirement')
        check.update(status='not-applicable', reason='', evidence=[])
        self.assertEqual('blocked', guard.evaluate(self.project, self.data)['status'])

    def test_s1_cannot_be_selected_as_default(self):
        self.data['selected_components'] = [{'id': 'superpowers.brainstorming', 'mode': 'default'}]
        with self.assertRaises(ValueError):
            guard.evaluate(self.project, self.data)

    def test_unknown_or_duplicate_check_is_rejected(self):
        self.complete()
        self.data['checks'].append(copy.deepcopy(self.data['checks'][0]))
        with self.assertRaises(ValueError):
            guard.evaluate(self.project, self.data)

    def test_open_high_issue_blocks_even_when_checks_pass(self):
        self.complete()
        self.data['issues'] = [{'id': 'ISSUE-1', 'risk_id': 'PERF-002', 'owner': 'architect',
                               'severity': 'high', 'status': 'open'}]
        self.assertEqual('blocked', guard.evaluate(self.project, self.data)['status'])

    def test_evidence_cannot_escape_target_project(self):
        self.assertTrue(guard.evidence_errors(self.project, [{'path': '../outside.txt', 'sha256': 'x'}]))

    def test_profile_features_cannot_be_removed(self):
        self.data['features'] = []
        with self.assertRaises(ValueError):
            guard.evaluate(self.project, self.data)

    def test_unknown_feature_cannot_silently_skip_risks(self):
        self.data['features'].append('concurency')
        with self.assertRaises(ValueError):
            guard.evaluate(self.project, self.data)

    def test_null_reason_cannot_pass(self):
        self.complete()
        self.data['checks'][0]['reason'] = None
        self.assertEqual('blocked', guard.evaluate(self.project, self.data)['status'])

    def test_acceptance_cannot_clear_high_risk(self):
        self.complete()
        self.data['issues'] = [{'id': 'ISSUE-1', 'risk_id': 'PERF-002', 'owner': 'architect',
            'severity': 'high', 'status': 'accepted', 'accepted_by': 'test-reviewer',
            'revision': 'initial', 'reason': 'Synthetic acceptance.', 'evidence': self.evidence}]
        self.assertEqual('blocked', guard.evaluate(self.project, self.data, 'delivery')['status'])

    def test_malformed_evidence_is_rejected(self):
        with self.assertRaises(ValueError):
            guard.evidence_errors(self.project, [None])


if __name__ == '__main__':
    unittest.main()
