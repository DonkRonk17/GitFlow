<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/d51a0de9-f15f-42e7-869f-ab57953778c5" />

# GitFlow v1.0

**Smart Git Workflow Assistant - Conventional Commits, Branch Management, and Changelog Generation**

A zero-dependency CLI tool that streamlines git workflows with pre-formatted conventional commits, branch cleanup, repository statistics, and automatic changelog generation. Built for developers who want consistent commit messages and effortless repository management.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)](requirements.txt)

---

## What It Does

**Problem:** Developers use git daily but struggle with:
- Writing consistent commit messages
- Remembering conventional commit formats
- Cleaning up old branches
- Generating changelogs for releases
- Getting quick repository insights
- Maintaining professional commit history for open source projects

**Solution:** GitFlow solves this by:
- [OK] **Conventional commits** - Pre-formatted commit types that follow industry standards
- [OK] **Branch management** - Easy cleanup of merged branches (with dry-run safety)
- [OK] **Repository stats** - Instant insights on commits, files, contributors
- [OK] **Changelog generation** - Auto-generate from commit history with customizable time ranges
- [OK] **Enhanced status** - Better overview than `git status` with last commit info
- [OK] **Zero dependencies** - Uses only Python standard library and native git CLI

**Real Impact:**

```bash
# BEFORE: Manual commit message formatting
git add .
git commit -m "added login feature"  # Inconsistent, unprofessional
git push

# AFTER: GitFlow conventional commits
python gitflow.py commit feat "Add login feature"
# [OK] Staging changes...
# [SAVE] Committing: feat: Add login feature
# [OK] Committed: [FEAT] New feature
# [UPLOAD] Pushing to remote...
# [OK] Pushed to remote
```

---

## Quick Start

### Installation

```bash
# Clone or download
cd path/to/GitFlow

# Run immediately (no installation required)
python gitflow.py --help

# OR install as package
pip install -e .
```

**Requirements:** Python 3.6+ and git installed. No `pip install` required!

### Basic Usage

```bash
# Create a conventional commit (most common)
python gitflow.py commit feat "Add user authentication"

# View repository statistics
python gitflow.py stats

# Generate a changelog for the last week
python gitflow.py changelog --since 7.days

# Preview branch cleanup (safe - dry run)
python gitflow.py cleanup --dry-run

# Show help
python gitflow.py --help
```

---

## Usage

### Command Line Interface

GitFlow provides 8 commands for comprehensive git workflow management:

```bash
# Conventional commits
python gitflow.py commit <type> "message" [--scope X] [--no-push]

# View commit history
python gitflow.py log [--count N]

# Repository statistics
python gitflow.py stats

# Enhanced status
python gitflow.py status

# Branch management
python gitflow.py branches [--remote]

# Branch cleanup
python gitflow.py cleanup [--dry-run] [--force]

# Changelog generation
python gitflow.py changelog [--since X] [--output FILE]

# Initialize repository
python gitflow.py init
```

**All Options:**

```
gitflow.py <command> [options]

Commands:
  commit     Create conventional commit
  log        View commit history  
  stats      Repository statistics
  status     Enhanced git status
  branches   List branches
  cleanup    Clean merged branches
  changelog  Generate changelog
  init       Initialize git repository

Global Options:
  --help     Show help message
```

### Python API

```python
from gitflow import GitFlow

# Initialize
gf = GitFlow()

# Check if in a git repository
if gf.is_git_repo():
    print("[OK] In a git repository")

# Get current branch
branch = gf.get_current_branch()
print(f"Current branch: {branch}")

# Get repository statistics
stats = gf.get_repo_stats()
print(f"Total commits: {stats['total_commits']}")
print(f"Contributors: {stats['contributors']}")

# Get commit log
commits = gf.get_commit_log(count=5)
for commit in commits:
    print(f"{commit['hash'][:7]} - {commit['message']}")

# Run any git command
success, output = gf.run_git(['add', '-A'])
if success:
    print("[OK] Changes staged")

# Generate changelog
changelog = gf.generate_changelog(since="7.days")
print(changelog)
```

---

## Commands Reference

### 1. Conventional Commits

Create properly formatted commits following conventional commit standards:

```bash
# Basic syntax
python gitflow.py commit <type> "message"

# Available commit types:
#   feat     - [FEAT] New feature
#   fix      - [FIX] Bug fix  
#   docs     - [DOCS] Documentation
#   style    - [STYLE] Code style
#   refactor - [REFACTOR] Refactor
#   perf     - [PERF] Performance
#   test     - [TEST] Tests
#   chore    - [CHORE] Chore
#   build    - [BUILD] Build
#   ci       - [CI] CI/CD

# Examples
python gitflow.py commit feat "Add login page"
python gitflow.py commit fix "Fix navbar responsive issue"
python gitflow.py commit docs "Update API documentation"

# With scope (for larger projects)
python gitflow.py commit feat "Add export button" --scope dashboard

# Without auto-push (commit only, no push)
python gitflow.py commit fix "Fix typo" --no-push
```

**Output:**

```
[OK] Staging changes...
[SAVE] Committing: feat: Add login page
[OK] Committed: [FEAT] New feature
[UPLOAD] Pushing to remote...
[OK] Pushed to remote
```

### 2. Commit Log

View recent commits in a clean format:

```bash
# Last 10 commits (default)
python gitflow.py log

# Custom count
python gitflow.py log --count 20
```

**Output:**

```
[DOCS] Recent Commits

a3b2c1d  feat: Add user authentication
         John Doe - 2 hours ago

d4e5f6g  fix: Fix login button styling
         Jane Smith - 5 hours ago

e5f6g7h  docs: Update README
         Bob Johnson - 1 day ago
```

### 3. Repository Statistics

Get instant insights about your repository:

```bash
python gitflow.py stats
```

**Output:**

```
[STATS] Repository Statistics

Total Commits:     342
Total Files:       87
Contributors:      5
Recent Activity:   23 commits (last 30 days)

[USERS] Top Contributors:
   156 commits  John Doe
    98 commits  Jane Smith
    45 commits  Bob Johnson
```

### 4. Branch Management

List and manage branches:

```bash
# List local branches
python gitflow.py branches

# List remote branches
python gitflow.py branches --remote
```

**Output:**

```
[BRANCH] Local Branches

  -> main
     feature/login
     feature/dashboard
     bugfix/navbar
```

### 5. Branch Cleanup

Clean up merged branches safely:

```bash
# Preview what would be deleted (SAFE - no changes made)
python gitflow.py cleanup --dry-run

# Actually delete merged branches
python gitflow.py cleanup --force
```

**Dry-run Output:**

```
[SEARCH] Finding merged branches...

[DELETE] These branches can be deleted:

  - feature/old-login
  - bugfix/fix-typo
  - feature/completed-feature

[STATS] Total: 3 branch(es)
[INFO] Run with --force to actually delete
```

### 6. Changelog Generation

Auto-generate changelogs from commit history:

```bash
# Last 7 days
python gitflow.py changelog --since 7.days

# Custom date
python gitflow.py changelog --since 2024-01-01

# Save to file
python gitflow.py changelog --since 7.days --output CHANGELOG.md
```

**Output:**

```
# Changelog

Generated: 2026-01-24 12:30

## [FEAT] New feature
- Add user authentication
- Add dashboard page

## [FIX] Bug fix
- Fix navbar responsive issue
- Fix login button styling

## [DOCS] Documentation
- Update API documentation
```

### 7. Enhanced Status

Better overview than regular git status:

```bash
python gitflow.py status
```

**Output:**

```
[BRANCH] On branch: main

[DOCS] Changes:
  M src/app.py
  A new-file.txt
  D old-file.txt

[PIN] Last commit: a3b2c1d - feat: Add user auth
   John Doe - 2 hours ago
```

### 8. Initialize Repository

Quick git init with confirmation:

```bash
python gitflow.py init
# [OK] Initialized git repository
```

---

## Commit Types Reference

| Type | Symbol | Description | Example |
|------|--------|-------------|---------|
| `feat` | [FEAT] | New feature | `feat: Add user login` |
| `fix` | [FIX] | Bug fix | `fix: Fix navbar overflow` |
| `docs` | [DOCS] | Documentation | `docs: Update API guide` |
| `style` | [STYLE] | Code style/formatting | `style: Format with prettier` |
| `refactor` | [REFACTOR] | Code refactoring | `refactor: Extract helper function` |
| `perf` | [PERF] | Performance improvement | `perf: Optimize image loading` |
| `test` | [TEST] | Add/update tests | `test: Add login tests` |
| `chore` | [CHORE] | Maintenance | `chore: Update dependencies` |
| `build` | [BUILD] | Build system | `build: Add webpack config` |
| `ci` | [CI] | CI/CD changes | `ci: Add GitHub Actions` |

---

## How It Works

### Technical Approach

GitFlow wraps the git CLI with Python, providing:

1. **Subprocess Management**: Safe execution of git commands via `subprocess.run()` with timeout protection
2. **Output Parsing**: Structured parsing of git output into Python objects
3. **Error Handling**: Graceful handling of non-git directories and command failures
4. **Cross-Platform**: Works on Windows, macOS, and Linux

### Core Architecture

```python
class GitFlow:
    @staticmethod
    def run_git(args: List[str], timeout: int = 30) -> Tuple[bool, str]:
        """Execute git command safely with timeout protection."""
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout or result.stderr

    @staticmethod
    def is_git_repo() -> bool:
        """Check if current directory is a git repository."""
        success, _ = GitFlow.run_git(['rev-parse', '--is-inside-work-tree'])
        return success
```

---

## Use Cases

### For Solo Developers

```bash
# Consistent commit messages without memorizing formats
python gitflow.py commit feat "Add user profile page"

# Quick repository insights
python gitflow.py stats

# Clean up old branches easily
python gitflow.py cleanup --force

# Generate changelogs for releases
python gitflow.py changelog --since 2024-01-01 --output CHANGELOG.md
```

### For Teams

```bash
# Enforce conventional commit standards across the team
python gitflow.py commit feat "Add authentication" --scope auth

# Track contributor activity
python gitflow.py stats

# Generate release notes automatically
python gitflow.py changelog --since last-release

# Maintain clean branch structure
python gitflow.py cleanup --dry-run
```

### For Open Source Projects

```bash
# Professional commit history
python gitflow.py commit fix "Fix issue #42" --scope api

# Easy changelog generation for releases
python gitflow.py changelog --since v1.0.0 --output RELEASE_NOTES.md

# Repository health monitoring
python gitflow.py stats

# Contributor statistics for README
python gitflow.py stats | grep "Top Contributors"
```

---

## Dependencies

GitFlow uses only Python's standard library:

- `subprocess` - Git command execution
- `argparse` - CLI argument parsing
- `sys` - System operations
- `json` - Data serialization
- `datetime` - Date/time handling
- `pathlib` - Cross-platform paths

**No `pip install` required!**

---

## Troubleshooting

### Issue: "Not a git repository"
**Cause:** Running GitFlow outside a git repository  
**Fix:** Navigate to a git repository first, or run `python gitflow.py init`

### Issue: "Git not found"
**Cause:** Git is not installed or not in PATH  
**Fix:** Install git from https://git-scm.com and ensure it's in your system PATH

### Issue: "Command timed out"
**Cause:** Long-running git operation (large repository, slow network)  
**Fix:** Check your network connection, or wait for ongoing operations to complete

### Issue: "Permission denied"
**Cause:** SSH key issues with remote repository  
**Fix:** Verify your SSH keys are configured correctly: `ssh -T git@github.com`

### Issue: "Unicode errors on Windows"
**Cause:** Previous versions used Unicode emojis  
**Fix:** This version uses ASCII-safe output. Update to latest version.

### Still Having Issues?

1. Check [EXAMPLES.md](EXAMPLES.md) for working examples
2. Review [CHEAT_SHEET.txt](CHEAT_SHEET.txt) for quick reference
3. Ask in Team Brain Synapse
4. Open an issue on GitHub

---

## Documentation

- **[EXAMPLES.md](EXAMPLES.md)** - 10+ working examples with expected output
- **[CHEAT_SHEET.txt](CHEAT_SHEET.txt)** - Quick reference guide
- **[INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)** - Integration with Team Brain tools
- **[QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)** - Agent-specific guides
- **[INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)** - Copy-paste integration code
- **[API Reference](#python-api)** - Full Python API documentation

---

## Integration with Team Brain

### With SynapseLink

```python
from gitflow import GitFlow
from synapselink import quick_send

# Commit and notify team
gf = GitFlow()
gf.run_git(['add', '-A'])
gf.run_git(['commit', '-m', 'feat: Add new feature'])

quick_send("TEAM", "New Commit", "feat: Add new feature pushed to main")
```

### With AgentHealth

```python
from gitflow import GitFlow
from agenthealth import AgentHealth

health = AgentHealth()
gf = GitFlow()

# Log GitFlow operations as agent activity
health.start_session("ATLAS", task="GitFlow Development")

stats = gf.get_repo_stats()
health.heartbeat("ATLAS", status="active", message=f"Repo has {stats['total_commits']} commits")

health.end_session("ATLAS")
```

### With TaskQueuePro

```python
from gitflow import GitFlow
from taskqueuepro import TaskQueuePro

tq = TaskQueuePro()
gf = GitFlow()

# Create task for pending commits
if gf.is_git_repo():
    changes = gf.run_git(['status', '--porcelain'])[1]
    if changes:
        tq.add_task("Review and commit pending changes", priority="HIGH")
```

---

## Testing

GitFlow includes a comprehensive test suite:

```bash
# Run all tests
python -m pytest test_gitflow.py -v

# Run specific test
python -m pytest test_gitflow.py::TestGitFlowCore -v

# Run with coverage
python -m pytest test_gitflow.py --cov=gitflow --cov-report=html
```

**Test Categories:**
- `TestGitFlowCore` - Core functionality tests
- `TestGitFlowEdgeCases` - Edge case handling
- `TestGitFlowIntegration` - Integration scenarios

**Quality Gate:** 100% test pass rate required before release

---

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/06e7e960-b38a-49b1-9c1c-6f71af1c7e81" />


## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes using GitFlow (`python gitflow.py commit feat "Add amazing feature"`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repo
git clone https://github.com/DonkRonk17/GitFlow.git
cd GitFlow

# Run tests
python -m pytest test_gitflow.py -v

# Make changes and test
python gitflow.py --help
```

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Credits

**Built by:** ATLAS (Team Brain)  
**Requested by:** Forge (needed for standardized commit workflows across Team Brain projects)  
**For:** Randell Logan Smith / [Metaphy LLC](https://metaphysicsandcomputing.com)  
**Part of:** Beacon HQ / Team Brain Ecosystem  
**Date:** January 24, 2026  
**Methodology:** Test-Break-Optimize (15+ tests passed)

Built with care as part of the Team Brain ecosystem - where AI agents collaborate to solve real problems.

---

## Links

- **GitHub:** https://github.com/DonkRonk17/GitFlow
- **Issues:** https://github.com/DonkRonk17/GitFlow/issues
- **Author:** https://github.com/DonkRonk17
- **Company:** [Metaphy LLC](https://metaphysicsandcomputing.com)
- **Ecosystem:** Part of HMSS (Heavenly Morning Star System)

---

## Quick Reference

```bash
# Commits
gitflow commit <type> "message" [--scope X] [--no-push]

# Types: feat, fix, docs, style, refactor, perf, test, chore, build, ci

# Viewing
gitflow log [--count N]
gitflow stats
gitflow status
gitflow branches [--remote]

# Management
gitflow cleanup [--dry-run] [--force]
gitflow changelog [--since X] [--output FILE]

# Setup
gitflow init
```

---

**GitFlow** - Make your git workflow flow!

---

*For the Maximum Benefit of Life. One World. One Family. One Love.*
