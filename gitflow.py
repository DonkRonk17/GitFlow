#!/usr/bin/env python3
"""
GitFlow - Smart Git Workflow Assistant
A CLI helper for common git operations - commit messages, branch management, stats, and more.
"""

import os
import sys
import io
import subprocess
import argparse
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from collections import Counter

# Fix Unicode output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# --- Config ---
COMMIT_TYPES = {
    "feat": "[FEAT] New feature",
    "fix": "[FIX] Bug fix",
    "docs": "[DOCS] Documentation",
    "style": "[STYLE] Code style",
    "refactor": "[REFACTOR] Refactor",
    "perf": "[PERF] Performance",
    "test": "[TEST] Tests",
    "chore": "[CHORE] Chore",
    "build": "[BUILD] Build",
    "ci": "[CI] CI/CD"
}

class GitFlow:
    """Git workflow helper"""
    
    @staticmethod
    def run_git(command: List[str], capture_output: bool = True) -> Tuple[bool, str]:
        """Run git command"""
        try:
            result = subprocess.run(
                ['git'] + command,
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                text=True,
                timeout=30
            )
            
            if capture_output:
                output = result.stdout if result.returncode == 0 else result.stderr
                return result.returncode == 0, output.strip()
            else:
                return result.returncode == 0, ""
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except FileNotFoundError:
            return False, "Git not found. Please install git."
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def is_git_repo() -> bool:
        """Check if current directory is a git repository"""
        success, _ = GitFlow.run_git(['rev-parse', '--git-dir'])
        return success
    
    @staticmethod
    def get_current_branch() -> Optional[str]:
        """Get current branch name"""
        success, output = GitFlow.run_git(['branch', '--show-current'])
        return output if success else None
    
    @staticmethod
    def get_branches(remote: bool = False) -> List[str]:
        """Get list of branches"""
        cmd = ['branch', '-r'] if remote else ['branch']
        success, output = GitFlow.run_git(cmd)
        
        if not success:
            return []
        
        branches = []
        for line in output.split('\n'):
            line = line.strip()
            if line and not line.startswith('*'):
                # Remove remote prefix
                branch = line.replace('origin/', '') if remote else line
                branches.append(branch)
        
        return branches
    
    @staticmethod
    def get_repo_stats() -> Dict:
        """Get repository statistics"""
        stats = {}
        
        # Total commits
        success, output = GitFlow.run_git(['rev-list', '--count', 'HEAD'])
        stats['total_commits'] = int(output) if success else 0
        
        # Contributors
        success, output = GitFlow.run_git(['shortlog', '-sn', '--all'])
        if success:
            contributors = output.split('\n')
            stats['contributors'] = len(contributors)
            stats['top_contributors'] = []
            for line in contributors[:5]:
                match = re.match(r'\s*(\d+)\s+(.+)', line)
                if match:
                    count, name = match.groups()
                    stats['top_contributors'].append((name, int(count)))
        else:
            stats['contributors'] = 0
            stats['top_contributors'] = []
        
        # Files
        success, output = GitFlow.run_git(['ls-files'])
        stats['total_files'] = len(output.split('\n')) if success and output else 0
        
        # Recent activity (last 30 days)
        since = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        success, output = GitFlow.run_git(['rev-list', '--count', f'--since={since}', 'HEAD'])
        stats['commits_last_30_days'] = int(output) if success else 0
        
        return stats
    
    @staticmethod
    def get_commit_log(count: int = 10) -> List[Dict]:
        """Get recent commit log"""
        success, output = GitFlow.run_git([
            'log',
            f'-{count}',
            '--pretty=format:%H|%an|%ae|%ar|%s'
        ])
        
        if not success:
            return []
        
        commits = []
        for line in output.split('\n'):
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 5:
                commits.append({
                    'hash': parts[0][:7],
                    'author': parts[1],
                    'email': parts[2],
                    'time': parts[3],
                    'message': parts[4]
                })
        
        return commits
    
    @staticmethod
    def cleanup_branches(dry_run: bool = True) -> List[str]:
        """Find branches to clean up (merged or old)"""
        # Get merged branches
        success, output = GitFlow.run_git(['branch', '--merged'])
        if not success:
            return []
        
        merged_branches = []
        for line in output.split('\n'):
            branch = line.strip().lstrip('* ')
            if branch and branch not in ['main', 'master', 'develop']:
                merged_branches.append(branch)
        
        if not dry_run:
            for branch in merged_branches:
                GitFlow.run_git(['branch', '-d', branch])
        
        return merged_branches
    
    @staticmethod
    def generate_changelog(since: str = None) -> str:
        """Generate changelog from commits"""
        cmd = ['log', '--pretty=format:%s']
        if since:
            cmd.append(f'--since={since}')
        
        success, output = GitFlow.run_git(cmd)
        if not success:
            return "No commits found"
        
        # Group by commit type
        grouped = {key: [] for key in COMMIT_TYPES.keys()}
        grouped['other'] = []
        
        for line in output.split('\n'):
            if not line:
                continue
            
            # Check for conventional commit format
            match = re.match(r'^(\w+)(?:\([\w-]+\))?: (.+)$', line)
            if match:
                commit_type, message = match.groups()
                if commit_type in grouped:
                    grouped[commit_type].append(message)
                else:
                    grouped['other'].append(line)
            else:
                grouped['other'].append(line)
        
        # Build changelog
        changelog = []
        changelog.append(f"# Changelog")
        changelog.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        for type_key, type_desc in COMMIT_TYPES.items():
            commits = grouped[type_key]
            if commits:
                changelog.append(f"\n## {type_desc}\n")
                for commit in commits:
                    changelog.append(f"- {commit}")
        
        if grouped['other']:
            changelog.append(f"\n## Other Changes\n")
            for commit in grouped['other']:
                changelog.append(f"- {commit}")
        
        return '\n'.join(changelog)


def print_repo_stats(stats: Dict):
    """Pretty print repository statistics"""
    print("\n=== Repository Statistics ===\n")
    print(f"Total Commits:     {stats['total_commits']}")
    print(f"Total Files:       {stats['total_files']}")
    print(f"Contributors:      {stats['contributors']}")
    print(f"Recent Activity:   {stats['commits_last_30_days']} commits (last 30 days)")
    
    if stats['top_contributors']:
        print(f"\n--- Top Contributors ---\n")
        for name, count in stats['top_contributors']:
            print(f"  {count:>4} commits  {name}")
    
    print()


def print_commits(commits: List[Dict]):
    """Pretty print commit log"""
    print("\n=== Recent Commits ===\n")
    for commit in commits:
        print(f"{commit['hash']}  {commit['message']}")
        print(f"         {commit['author']} - {commit['time']}")
        print()


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="GitFlow - Smart Git Workflow Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gitflow commit feat "Add user login"      # Conventional commit
  gitflow log                                # Recent commits
  gitflow stats                              # Repository statistics
  gitflow branches                           # List branches
  gitflow cleanup --dry-run                  # Preview branch cleanup
  gitflow changelog --since 7.days          # Generate changelog
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Commit command
    commit_parser = subparsers.add_parser('commit', help='Create conventional commit')
    commit_parser.add_argument('type', choices=list(COMMIT_TYPES.keys()),
                              help='Commit type')
    commit_parser.add_argument('message', help='Commit message')
    commit_parser.add_argument('--scope', help='Commit scope (optional)')
    commit_parser.add_argument('--no-push', action='store_true', help='Don\'t push after commit')
    
    # Log command
    log_parser = subparsers.add_parser('log', help='Show recent commits')
    log_parser.add_argument('--count', type=int, default=10, help='Number of commits')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show repository statistics')
    
    # Branches command
    branches_parser = subparsers.add_parser('branches', help='List branches')
    branches_parser.add_argument('--remote', action='store_true', help='Show remote branches')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up merged branches')
    cleanup_parser.add_argument('--dry-run', action='store_true', help='Preview without deleting')
    cleanup_parser.add_argument('--force', action='store_true', help='Actually delete branches')
    
    # Changelog command
    changelog_parser = subparsers.add_parser('changelog', help='Generate changelog')
    changelog_parser.add_argument('--since', help='Start date (e.g., 7.days, 2024-01-01)')
    changelog_parser.add_argument('--output', help='Output file (default: stdout)')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Enhanced git status')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize git repository')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    gf = GitFlow()
    
    # Check if git repo (except for init)
    if args.command != 'init' and not gf.is_git_repo():
        print("[X] Not a git repository")
        print("[INFO] Run 'gitflow init' or 'git init' to initialize")
        return
    
    # Execute command
    if args.command == 'init':
        success, output = gf.run_git(['init'])
        if success:
            print("[OK] Initialized git repository")
        else:
            print(f"[X] Failed: {output}")
    
    elif args.command == 'commit':
        # Build commit message
        scope_part = f"({args.scope})" if args.scope else ""
        message = f"{args.type}{scope_part}: {args.message}"
        
        # Stage all changes
        print("[...] Staging changes...")
        success, output = gf.run_git(['add', '-A'])
        if not success:
            print(f"[X] Failed to stage: {output}")
            return
        
        # Commit
        print(f"[...] Committing: {message}")
        success, output = gf.run_git(['commit', '-m', message])
        if not success:
            print(f"[X] Failed to commit: {output}")
            return
        
        print(f"[OK] Committed: {COMMIT_TYPES[args.type]}")
        
        # Push (if not disabled)
        if not args.no_push:
            print("[...] Pushing to remote...")
            success, output = gf.run_git(['push'])
            if success:
                print("[OK] Pushed to remote")
            else:
                print(f"[!] Push failed: {output}")
                print("[INFO] Run 'git push' manually if needed")
    
    elif args.command == 'log':
        commits = gf.get_commit_log(args.count)
        if commits:
            print_commits(commits)
        else:
            print("[INFO] No commits found")
    
    elif args.command == 'stats':
        print("[...] Analyzing repository...")
        stats = gf.get_repo_stats()
        print_repo_stats(stats)
    
    elif args.command == 'branches':
        current = gf.get_current_branch()
        branches = gf.get_branches(args.remote)
        
        if not branches:
            print("[INFO] No branches found")
            return
        
        title = "Remote Branches" if args.remote else "Local Branches"
        print(f"\n=== {title} ===\n")
        
        for branch in branches:
            marker = ">" if branch == current else " "
            print(f"  {marker} {branch}")
        
        print()
    
    elif args.command == 'cleanup':
        if args.dry_run or not args.force:
            print("[...] Finding merged branches...\n")
            branches = gf.cleanup_branches(dry_run=True)
            
            if branches:
                print("Branches that can be deleted:\n")
                for branch in branches:
                    print(f"  - {branch}")
                print(f"\nTotal: {len(branches)} branch(es)")
                
                if args.dry_run:
                    print("\n[INFO] Run with --force to actually delete")
            else:
                print("[OK] No branches to clean up")
        else:
            branches = gf.cleanup_branches(dry_run=False)
            if branches:
                print(f"[OK] Deleted {len(branches)} branch(es)")
            else:
                print("[OK] No branches to clean up")
    
    elif args.command == 'changelog':
        print("[...] Generating changelog...")
        
        # Parse since parameter
        since_date = None
        if args.since:
            if args.since.endswith('.days'):
                days = int(args.since.replace('.days', ''))
                since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            else:
                since_date = args.since
        
        changelog = gf.generate_changelog(since_date)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(changelog)
            print(f"[OK] Changelog saved to: {args.output}")
        else:
            print(changelog)
    
    elif args.command == 'status':
        # Enhanced status
        current_branch = gf.get_current_branch()
        print(f"\n=== On branch: {current_branch} ===\n")
        
        # Run git status
        success, output = gf.run_git(['status', '--short'])
        if success and output:
            print("Changes:\n")
            for line in output.split('\n'):
                if line:
                    print(f"  {line}")
            print()
        else:
            print("[OK] Working tree clean\n")
        
        # Show recent commit
        commits = gf.get_commit_log(1)
        if commits:
            commit = commits[0]
            print(f"Last commit: {commit['hash']} - {commit['message']}")
            print(f"   {commit['author']} - {commit['time']}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] GitFlow interrupted")
    except Exception as e:
        print(f"\n[X] Error: {e}")
        sys.exit(1)
