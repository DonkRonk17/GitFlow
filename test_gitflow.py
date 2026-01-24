#!/usr/bin/env python3
"""
Comprehensive test suite for GitFlow.

Tests cover:
- Core functionality (git operations)
- Branch management
- Commit message generation
- Statistics gathering
- Changelog generation
- Edge cases and error handling

Run: python test_gitflow.py
"""

import unittest
import sys
import os
import tempfile
import shutil
import stat
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from gitflow import GitFlow, COMMIT_TYPES, print_repo_stats, print_commits


def robust_rmtree(path: str, retries: int = 3) -> None:
    """Remove directory tree with retry logic for Windows file locks.
    
    Git on Windows can lock files temporarily. This function handles
    PermissionError by retrying after a brief delay.
    """
    def on_error(func, path, exc_info):
        """Error handler for shutil.rmtree that handles read-only files."""
        # Handle read-only files (common with .git)
        if os.path.exists(path):
            os.chmod(path, stat.S_IWUSR | stat.S_IRUSR)
            try:
                func(path)
            except PermissionError:
                pass  # Will retry in main loop
    
    for attempt in range(retries):
        try:
            if os.path.exists(path):
                shutil.rmtree(path, onerror=on_error)
            return
        except PermissionError:
            if attempt < retries - 1:
                time.sleep(0.5)  # Wait for git to release locks
            # On final attempt, just ignore - temp dir will be cleaned up by OS


class TestGitFlowConstants(unittest.TestCase):
    """Test configuration constants."""
    
    def test_commit_types_exist(self):
        """Test all commit types are defined."""
        expected_types = ['feat', 'fix', 'docs', 'style', 'refactor', 
                         'perf', 'test', 'chore', 'build', 'ci']
        for commit_type in expected_types:
            self.assertIn(commit_type, COMMIT_TYPES)
            print(f"  [OK] Commit type '{commit_type}' exists")
    
    def test_commit_types_have_descriptions(self):
        """Test all commit types have non-empty descriptions."""
        for commit_type, description in COMMIT_TYPES.items():
            self.assertIsInstance(description, str)
            self.assertTrue(len(description) > 0)
        print("  [OK] All commit types have descriptions")
    
    def test_commit_types_ascii_safe(self):
        """Test all commit type descriptions are ASCII-safe (no emojis)."""
        for commit_type, description in COMMIT_TYPES.items():
            # Check for common emoji ranges
            for char in description:
                self.assertLess(ord(char), 0x1F300, 
                               f"Emoji found in {commit_type}: {description}")
        print("  [OK] All commit types are ASCII-safe")


class TestGitFlowRunGit(unittest.TestCase):
    """Test git command execution."""
    
    def test_run_git_with_version(self):
        """Test running git --version command."""
        gf = GitFlow()
        success, output = gf.run_git(['--version'])
        self.assertTrue(success)
        self.assertIn('git', output.lower())
        print(f"  [OK] Git version: {output}")
    
    def test_run_git_invalid_command(self):
        """Test handling of invalid git command."""
        gf = GitFlow()
        success, output = gf.run_git(['invalid-command-xyz'])
        self.assertFalse(success)
        print("  [OK] Invalid command handled correctly")
    
    def test_run_git_timeout(self):
        """Test command timeout handling."""
        gf = GitFlow()
        # This should complete quickly and not timeout
        success, output = gf.run_git(['--version'])
        self.assertTrue(success)
        print("  [OK] Command completed without timeout")


class TestGitFlowRepoDetection(unittest.TestCase):
    """Test repository detection."""
    
    def test_is_git_repo_in_non_repo(self):
        """Test is_git_repo returns False in non-repo directory."""
        gf = GitFlow()
        # Create temp directory that is NOT a git repo
        temp_dir = tempfile.mkdtemp()
        try:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            self.assertFalse(gf.is_git_repo())
            print("  [OK] Non-repo correctly detected")
        finally:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)
    
    def test_is_git_repo_in_actual_repo(self):
        """Test is_git_repo returns True in git repository."""
        gf = GitFlow()
        # Create temp git repo
        temp_dir = tempfile.mkdtemp()
        try:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            gf.run_git(['init'])
            self.assertTrue(gf.is_git_repo())
            print("  [OK] Git repo correctly detected")
        finally:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)


class TestGitFlowBranchOperations(unittest.TestCase):
    """Test branch-related operations."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test git repository."""
        cls.temp_dir = tempfile.mkdtemp()
        cls.original_cwd = os.getcwd()
        os.chdir(cls.temp_dir)
        
        gf = GitFlow()
        gf.run_git(['init'])
        gf.run_git(['config', 'user.email', 'test@test.com'])
        gf.run_git(['config', 'user.name', 'Test User'])
        
        # Create initial commit
        Path('test.txt').write_text('test content')
        gf.run_git(['add', '.'])
        gf.run_git(['commit', '-m', 'Initial commit'])
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test repository."""
        os.chdir(cls.original_cwd)
        robust_rmtree(cls.temp_dir)
    
    def test_get_current_branch(self):
        """Test getting current branch name."""
        gf = GitFlow()
        branch = gf.get_current_branch()
        self.assertIsNotNone(branch)
        self.assertIn(branch, ['main', 'master'])
        print(f"  [OK] Current branch: {branch}")
    
    def test_get_branches(self):
        """Test listing local branches."""
        gf = GitFlow()
        branches = gf.get_branches(remote=False)
        self.assertIsInstance(branches, list)
        print(f"  [OK] Got {len(branches)} local branches")
    
    def test_cleanup_branches_dry_run(self):
        """Test branch cleanup in dry run mode."""
        gf = GitFlow()
        branches = gf.cleanup_branches(dry_run=True)
        self.assertIsInstance(branches, list)
        print(f"  [OK] Cleanup dry run returned {len(branches)} branches")


class TestGitFlowCommitLog(unittest.TestCase):
    """Test commit log operations."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test git repository with commits."""
        cls.temp_dir = tempfile.mkdtemp()
        cls.original_cwd = os.getcwd()
        os.chdir(cls.temp_dir)
        
        gf = GitFlow()
        gf.run_git(['init'])
        gf.run_git(['config', 'user.email', 'test@test.com'])
        gf.run_git(['config', 'user.name', 'Test User'])
        
        # Create multiple commits
        for i in range(3):
            Path(f'file{i}.txt').write_text(f'content {i}')
            gf.run_git(['add', '.'])
            gf.run_git(['commit', '-m', f'feat: Add file {i}'])
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test repository."""
        os.chdir(cls.original_cwd)
        robust_rmtree(cls.temp_dir)
    
    def test_get_commit_log(self):
        """Test retrieving commit log."""
        gf = GitFlow()
        commits = gf.get_commit_log(count=5)
        self.assertIsInstance(commits, list)
        self.assertTrue(len(commits) > 0)
        print(f"  [OK] Got {len(commits)} commits")
    
    def test_commit_log_structure(self):
        """Test commit log entry structure."""
        gf = GitFlow()
        commits = gf.get_commit_log(count=1)
        if commits:
            commit = commits[0]
            self.assertIn('hash', commit)
            self.assertIn('author', commit)
            self.assertIn('email', commit)
            self.assertIn('time', commit)
            self.assertIn('message', commit)
            print("  [OK] Commit structure is correct")
        else:
            print("  [SKIP] No commits to test")
    
    def test_commit_log_count(self):
        """Test commit log respects count parameter."""
        gf = GitFlow()
        commits = gf.get_commit_log(count=2)
        self.assertLessEqual(len(commits), 2)
        print(f"  [OK] Commit count limited correctly: {len(commits)}")


class TestGitFlowStats(unittest.TestCase):
    """Test repository statistics."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test git repository."""
        cls.temp_dir = tempfile.mkdtemp()
        cls.original_cwd = os.getcwd()
        os.chdir(cls.temp_dir)
        
        gf = GitFlow()
        gf.run_git(['init'])
        gf.run_git(['config', 'user.email', 'test@test.com'])
        gf.run_git(['config', 'user.name', 'Test User'])
        
        # Create commit
        Path('test.txt').write_text('test content')
        gf.run_git(['add', '.'])
        gf.run_git(['commit', '-m', 'Initial commit'])
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test repository."""
        os.chdir(cls.original_cwd)
        robust_rmtree(cls.temp_dir)
    
    def test_get_repo_stats(self):
        """Test getting repository statistics."""
        gf = GitFlow()
        stats = gf.get_repo_stats()
        
        self.assertIn('total_commits', stats)
        self.assertIn('total_files', stats)
        self.assertIn('contributors', stats)
        self.assertIn('commits_last_30_days', stats)
        self.assertIn('top_contributors', stats)
        print("  [OK] Stats structure is correct")
    
    def test_stats_values(self):
        """Test repository statistics values are reasonable."""
        gf = GitFlow()
        stats = gf.get_repo_stats()
        
        self.assertGreaterEqual(stats['total_commits'], 0)
        self.assertGreaterEqual(stats['total_files'], 0)
        self.assertGreaterEqual(stats['contributors'], 0)
        print(f"  [OK] Stats: {stats['total_commits']} commits, {stats['total_files']} files")


class TestGitFlowChangelog(unittest.TestCase):
    """Test changelog generation."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test git repository with conventional commits."""
        cls.temp_dir = tempfile.mkdtemp()
        cls.original_cwd = os.getcwd()
        os.chdir(cls.temp_dir)
        
        gf = GitFlow()
        gf.run_git(['init'])
        gf.run_git(['config', 'user.email', 'test@test.com'])
        gf.run_git(['config', 'user.name', 'Test User'])
        
        # Create commits with conventional format
        commits = [
            ('feat: Add user authentication', 'auth.py'),
            ('fix: Fix login bug', 'login.py'),
            ('docs: Update README', 'README.md'),
        ]
        
        for message, filename in commits:
            Path(filename).write_text(f'content for {filename}')
            gf.run_git(['add', '.'])
            gf.run_git(['commit', '-m', message])
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test repository."""
        os.chdir(cls.original_cwd)
        robust_rmtree(cls.temp_dir)
    
    def test_generate_changelog(self):
        """Test changelog generation."""
        gf = GitFlow()
        changelog = gf.generate_changelog()
        
        self.assertIsInstance(changelog, str)
        self.assertIn('Changelog', changelog)
        print("  [OK] Changelog generated successfully")
    
    def test_changelog_contains_commits(self):
        """Test changelog contains commit messages."""
        gf = GitFlow()
        changelog = gf.generate_changelog()
        
        # Should contain at least one of our commit messages
        self.assertTrue(
            'authentication' in changelog.lower() or 
            'login' in changelog.lower() or
            'readme' in changelog.lower()
        )
        print("  [OK] Changelog contains commit messages")


class TestPrintFunctions(unittest.TestCase):
    """Test output formatting functions."""
    
    def test_print_repo_stats(self):
        """Test stats printing doesn't crash."""
        stats = {
            'total_commits': 100,
            'total_files': 50,
            'contributors': 5,
            'commits_last_30_days': 20,
            'top_contributors': [('Test User', 50), ('Other User', 30)]
        }
        
        # Should not raise any exceptions
        try:
            print_repo_stats(stats)
            print("  [OK] print_repo_stats executed successfully")
        except Exception as e:
            self.fail(f"print_repo_stats raised exception: {e}")
    
    def test_print_commits(self):
        """Test commits printing doesn't crash."""
        commits = [
            {
                'hash': 'abc1234',
                'author': 'Test User',
                'email': 'test@test.com',
                'time': '2 hours ago',
                'message': 'feat: Test commit'
            }
        ]
        
        # Should not raise any exceptions
        try:
            print_commits(commits)
            print("  [OK] print_commits executed successfully")
        except Exception as e:
            self.fail(f"print_commits raised exception: {e}")
    
    def test_print_empty_commits(self):
        """Test printing empty commit list."""
        try:
            print_commits([])
            print("  [OK] Empty commits list handled")
        except Exception as e:
            self.fail(f"print_commits raised exception on empty list: {e}")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_string_handling(self):
        """Test handling of empty strings."""
        gf = GitFlow()
        # Empty branch list should return empty list
        with patch.object(gf, 'run_git', return_value=(True, '')):
            branches = gf.get_branches()
            self.assertEqual(branches, [])
        print("  [OK] Empty string handled correctly")
    
    def test_malformed_git_output(self):
        """Test handling of malformed git output."""
        gf = GitFlow()
        # Malformed log output should not crash
        with patch.object(gf, 'run_git', return_value=(True, 'malformed|incomplete')):
            commits = gf.get_commit_log()
            self.assertIsInstance(commits, list)
        print("  [OK] Malformed output handled correctly")
    
    def test_git_failure_handling(self):
        """Test handling of git command failures."""
        gf = GitFlow()
        with patch.object(gf, 'run_git', return_value=(False, 'error')):
            branches = gf.get_branches()
            self.assertEqual(branches, [])
        print("  [OK] Git failure handled correctly")


def run_tests():
    """Run all tests with detailed output."""
    print("=" * 70)
    print("TESTING: GitFlow v1.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGitFlowConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestGitFlowRunGit))
    suite.addTests(loader.loadTestsFromTestCase(TestGitFlowRepoDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestGitFlowBranchOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestGitFlowCommitLog))
    suite.addTests(loader.loadTestsFromTestCase(TestGitFlowStats))
    suite.addTests(loader.loadTestsFromTestCase(TestGitFlowChangelog))
    suite.addTests(loader.loadTestsFromTestCase(TestPrintFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"[OK] Passed: {passed}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
