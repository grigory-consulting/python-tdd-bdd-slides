"""Offline regression checks for the uploader; no Docker or API access."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('manage', HERE / 'manage.py')
manage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manage)


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(HERE.parent.parent, self.root, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('docker', '.venv', '__pycache__', '.pytest_cache'))

    def test_unfinished_exercise_fails_before_upload(self):
        with self.assertRaisesRegex(RuntimeError, 'TODOs'):
            manage.snapshot(self.root)

    def test_demo_does_not_edit_source_files(self):
        before = (self.root / 'Jenkinsfile').read_bytes()
        files = manage.snapshot(self.root, demo=True)
        self.assertNotIn('TODO_', files['Jenkinsfile'])
        self.assertEqual(before, (self.root / 'Jenkinsfile').read_bytes())
        self.assertIn('tests/test_approval_report.test_preisreport.approved.txt', files)

    def test_private_and_generated_files_stay_out(self):
        for name in ('.env', 'tests/.env', 'tests/.private.py', 'reports/pytest.xml', 'docker/token.txt'):
            path = self.root / name
            path.parent.mkdir(exist_ok=True)
            path.write_text('DO-NOT-UPLOAD')
        files = manage.snapshot(self.root, demo=True)
        self.assertFalse(any('DO-NOT-UPLOAD' in v for v in files.values()))
        self.assertFalse(any(p.startswith(('docker/', 'reports/')) for p in files))

    def test_symlink_cannot_upload_an_external_file(self):
        private = self.root / '.private'
        private.write_text('DO-NOT-UPLOAD')
        try:
            (self.root / 'tests/leak.py').symlink_to(private)
        except OSError:
            self.skipTest('Symlinks are unavailable on this host')
        self.assertNotIn('tests/leak.py', manage.snapshot(self.root, demo=True))

    def test_comparison_cases_only_change_snapshot(self):
        base = manage.snapshot(self.root, demo=True)
        for case, expected in (('unit-red', 1), ('bdd-red', 2), ('coverage-low', 1)):
            files = manage.snapshot(self.root, demo=True, case=case)
            self.assertEqual(len(base) + expected, len(files))
            self.assertEqual(base, {p: files[p] for p in base})
        self.assertEqual(base, manage.snapshot(self.root, demo=True))

    def test_junit_and_cobertura_keep_their_distinct_meaning(self):
        result = manage.xml_summary({
            'reports/pytest.xml': b'<testsuites><testsuite tests="88" failures="1" errors="0" skipped="0"/></testsuites>',
            'reports/behave/TESTS-rabatt.xml': b'<testsuite tests="8" failures="0" errors="0" skipped="1"/>',
            'reports/coverage.xml': b'<coverage line-rate="0.42" branch-rate="0.25"/>',
        })
        self.assertEqual(result['reports/pytest.xml']['failures'], 1)
        self.assertEqual(result['reports/behave/TESTS-rabatt.xml']['skipped'], 1)
        self.assertEqual(result['reports/coverage.xml']['line-rate'], .42)

    def test_windows_bom_and_line_endings_are_normalized(self):
        path = self.root / '.gitlab-ci.yml'
        text = path.read_text()
        path.write_bytes(b'\xef\xbb\xbf' + text.replace('\n', '\r\n').encode())
        uploaded = manage.snapshot(self.root, demo=True)['.gitlab-ci.yml']
        self.assertFalse(uploaded.startswith('\ufeff'))
        self.assertNotIn('\r', uploaded)

    def test_own_main_can_follow_first_demo_run(self):
        calls = []

        def api(path, method='GET', data=None):
            calls.append((path, method, data))
            if '/branches?' in path:
                return [{'name': 'demo'}]
            if '/tree?' in path:
                return [{'type': 'blob', 'path': 'Jenkinsfile'}]
            return {'id': 'new-commit'}

        with patch.object(manage, 'gl', api):
            self.assertEqual(manage.commit_snapshot(1, 'main', {'Jenkinsfile': 'pipeline {}'}), 'new-commit')
        commit = next(data for path, method, data in calls if method == 'POST')
        self.assertEqual(commit['start_branch'], 'demo')
        self.assertIn(('/projects/1', 'PUT', {'default_branch': 'main'}), calls)


if __name__ == '__main__':
    unittest.main()
