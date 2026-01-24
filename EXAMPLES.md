# GitFlow - Usage Examples

**Complete Working Examples for All Features**

Quick navigation:
- [Example 1: Basic Commit](#example-1-basic-commit)
- [Example 2: Commit with Scope](#example-2-commit-with-scope)
- [Example 3: Local Commit Only](#example-3-local-commit-only)
- [Example 4: View Commit Log](#example-4-view-commit-log)
- [Example 5: Repository Statistics](#example-5-repository-statistics)
- [Example 6: Branch Management](#example-6-branch-management)
- [Example 7: Branch Cleanup](#example-7-branch-cleanup)
- [Example 8: Generate Changelog](#example-8-generate-changelog)
- [Example 9: Enhanced Status](#example-9-enhanced-status)
- [Example 10: Initialize New Repo](#example-10-initialize-new-repo)
- [Example 11: Python API Usage](#example-11-python-api-usage)
- [Example 12: Complete Workflow](#example-12-complete-workflow)

---

## Example 1: Basic Commit

**Scenario:** You've made changes and want to create a properly formatted conventional commit.

**Steps:**

```bash
# Navigate to your git repository
cd my-project

# Make some changes to files
echo "new feature code" >> feature.py

# Create a conventional commit
python gitflow.py commit feat "Add user authentication module"
```

**Expected Output:**

```
[...] Staging changes...
[...] Committing: feat: Add user authentication module
[OK] Committed: [FEAT] New feature
[...] Pushing to remote...
[OK] Pushed to remote
```

**What Happened:**
- All changes were staged (`git add -A`)
- Commit was created with conventional format: `feat: Add user authentication module`
- Changes were pushed to remote automatically

---

## Example 2: Commit with Scope

**Scenario:** You want to specify which part of the codebase this commit affects.

**Steps:**

```bash
# Add scope to organize commits by module/component
python gitflow.py commit fix "Resolve null pointer exception" --scope auth

# Another example with different scope
python gitflow.py commit feat "Add export button" --scope dashboard
```

**Expected Output:**

```
[...] Staging changes...
[...] Committing: fix(auth): Resolve null pointer exception
[OK] Committed: [FIX] Bug fix
[...] Pushing to remote...
[OK] Pushed to remote
```

**What Happened:**
- Commit message format: `type(scope): message`
- Scope helps organize commits by feature area
- Useful for large projects with multiple modules

---

## Example 3: Local Commit Only

**Scenario:** You want to commit but NOT push to remote (e.g., work in progress).

**Steps:**

```bash
# Commit without pushing
python gitflow.py commit wip "Work in progress - not ready for review" --no-push
```

**Expected Output:**

```
[...] Staging changes...
[...] Committing: chore: Work in progress - not ready for review
[OK] Committed: [CHORE] Chore
```

**What Happened:**
- Changes committed locally only
- No push to remote
- Useful for WIP commits or offline work

---

## Example 4: View Commit Log

**Scenario:** You want to see recent commit history in a clean format.

**Steps:**

```bash
# View last 10 commits (default)
python gitflow.py log

# View last 20 commits
python gitflow.py log --count 20

# View last 5 commits
python gitflow.py log --count 5
```

**Expected Output:**

```
=== Recent Commits ===

a3b2c1d  feat: Add user authentication module
         John Doe - 2 hours ago

d4e5f6g  fix(auth): Resolve null pointer exception
         Jane Smith - 5 hours ago

7h8i9j0  docs: Update API documentation
         Bob Johnson - 1 day ago

k1l2m3n  refactor: Extract helper functions
         John Doe - 2 days ago
```

**What You See:**
- Short commit hash (7 characters)
- Full commit message
- Author name and relative time

---

## Example 5: Repository Statistics

**Scenario:** You want to get a quick overview of repository health and activity.

**Steps:**

```bash
python gitflow.py stats
```

**Expected Output:**

```
[...] Analyzing repository...

=== Repository Statistics ===

Total Commits:     342
Total Files:       87
Contributors:      5
Recent Activity:   23 commits (last 30 days)

--- Top Contributors ---

   156 commits  John Doe
    98 commits  Jane Smith
    45 commits  Bob Johnson
    28 commits  Alice Williams
    15 commits  Charlie Brown
```

**What You Learn:**
- Total commit count shows project maturity
- File count indicates project size
- Contributor count shows team size
- Recent activity indicates project health
- Top contributors show who's most active

---

## Example 6: Branch Management

**Scenario:** You want to see all branches and which one you're on.

**Steps:**

```bash
# List local branches
python gitflow.py branches

# List remote branches
python gitflow.py branches --remote
```

**Expected Output (Local):**

```
=== Local Branches ===

  > main
    feature/user-auth
    feature/dashboard
    bugfix/login-error
    release/v2.0
```

**Expected Output (Remote):**

```
=== Remote Branches ===

    main
    develop
    feature/api-v2
    release/v1.5
```

**What You See:**
- `>` marker shows current branch
- Clean list of all branches
- Easy to see project structure

---

## Example 7: Branch Cleanup

**Scenario:** You want to clean up old branches that have been merged.

**Steps:**

```bash
# Step 1: Preview what would be deleted (safe)
python gitflow.py cleanup --dry-run

# Step 2: Actually delete merged branches
python gitflow.py cleanup --force
```

**Expected Output (Dry Run):**

```
[...] Finding merged branches...

Branches that can be deleted:

  - feature/old-login
  - bugfix/typo-fix
  - feature/completed-feature
  - hotfix/urgent-patch

Total: 4 branch(es)

[INFO] Run with --force to actually delete
```

**Expected Output (Force):**

```
[OK] Deleted 4 branch(es)
```

**Safety Features:**
- Protected branches (main, master, develop) are NEVER deleted
- Dry run lets you preview before deleting
- Only merged branches are candidates for deletion

---

## Example 8: Generate Changelog

**Scenario:** You're preparing a release and need a changelog.

**Steps:**

```bash
# Changelog from last 7 days
python gitflow.py changelog --since 7.days

# Changelog from specific date
python gitflow.py changelog --since 2026-01-01

# Save changelog to file
python gitflow.py changelog --since 7.days --output CHANGELOG.md
```

**Expected Output:**

```
[...] Generating changelog...
# Changelog

Generated: 2026-01-24 14:30

## [FEAT] New feature

- Add user authentication module
- Add dashboard page
- Add export functionality

## [FIX] Bug fix

- Resolve null pointer exception
- Fix navbar responsive issue
- Correct date formatting

## [DOCS] Documentation

- Update API documentation
- Add installation guide

## Other Changes

- Merge branch 'develop'
- Update dependencies
```

**Features:**
- Automatically groups by commit type
- Conventional commits are parsed correctly
- Can save to file or print to console

---

## Example 9: Enhanced Status

**Scenario:** You want a better overview than plain `git status`.

**Steps:**

```bash
python gitflow.py status
```

**Expected Output:**

```
=== On branch: feature/user-auth ===

Changes:

  M src/auth.py
  M tests/test_auth.py
  A src/utils/helpers.py
  D old_file.py

Last commit: a3b2c1d - feat: Add authentication
   John Doe - 2 hours ago
```

**What You See:**
- Current branch name prominently displayed
- File status codes (M=Modified, A=Added, D=Deleted)
- Last commit information for context

---

## Example 10: Initialize New Repo

**Scenario:** You're starting a new project and need to initialize git.

**Steps:**

```bash
# Create new project directory
mkdir my-new-project
cd my-new-project

# Initialize git repository
python gitflow.py init
```

**Expected Output:**

```
[OK] Initialized git repository
```

**Next Steps:**
- Create your files
- Use `python gitflow.py commit feat "Initial project setup"`

---

## Example 11: Python API Usage

**Scenario:** You want to use GitFlow programmatically in Python scripts.

**Code:**

```python
import sys
sys.path.append('C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow')
from gitflow import GitFlow

# Create instance
gf = GitFlow()

# Check if in a git repo
if gf.is_git_repo():
    print("This is a git repository")
    
    # Get current branch
    branch = gf.get_current_branch()
    print(f"Current branch: {branch}")
    
    # Get repository statistics
    stats = gf.get_repo_stats()
    print(f"Total commits: {stats['total_commits']}")
    print(f"Contributors: {stats['contributors']}")
    
    # Get recent commits
    commits = gf.get_commit_log(count=5)
    for commit in commits:
        print(f"{commit['hash']} - {commit['message']}")
    
    # Get all branches
    branches = gf.get_branches()
    print(f"Branches: {branches}")
    
    # Generate changelog
    changelog = gf.generate_changelog(since='7.days')
    print(changelog)
else:
    print("Not a git repository")
```

**Expected Output:**

```
This is a git repository
Current branch: main
Total commits: 156
Contributors: 5
a3b2c1d - feat: Add user authentication
d4e5f6g - fix: Resolve bug
7h8i9j0 - docs: Update README
...
Branches: ['feature/login', 'feature/dashboard']
# Changelog
...
```

---

## Example 12: Complete Workflow

**Scenario:** A typical day using GitFlow for development.

**Steps:**

```bash
# Morning: Check repository status and recent activity
python gitflow.py status
python gitflow.py log --count 5
python gitflow.py stats

# Start work: Create feature branch and switch to it
git checkout -b feature/new-feature

# Work on feature
# ... make changes ...

# Commit work with conventional message
python gitflow.py commit feat "Add new feature module"

# Continue working
# ... more changes ...

# Commit fix discovered during development
python gitflow.py commit fix "Fix edge case in new module" --scope module

# Documentation update
python gitflow.py commit docs "Add documentation for new feature"

# End of day: Check status
python gitflow.py status
python gitflow.py log --count 3

# Weekly: Generate changelog for team update
python gitflow.py changelog --since 7.days --output WEEKLY_CHANGES.md

# Monthly: Clean up merged branches
python gitflow.py cleanup --dry-run
python gitflow.py cleanup --force
```

**Best Practices:**
1. Start day with `status` and `log` to understand context
2. Use appropriate commit types (feat, fix, docs, etc.)
3. Add scope for larger projects
4. Generate changelogs regularly
5. Clean up merged branches periodically

---

## Commit Type Quick Reference

| Type | When to Use | Example |
|------|------------|---------|
| `feat` | New features | `feat: Add user login page` |
| `fix` | Bug fixes | `fix: Correct date formatting` |
| `docs` | Documentation | `docs: Update API reference` |
| `style` | Code formatting | `style: Fix indentation` |
| `refactor` | Code restructuring | `refactor: Extract helper method` |
| `perf` | Performance | `perf: Optimize database query` |
| `test` | Adding tests | `test: Add unit tests for auth` |
| `chore` | Maintenance | `chore: Update dependencies` |
| `build` | Build system | `build: Add webpack config` |
| `ci` | CI/CD | `ci: Add GitHub Actions workflow` |

---

## Error Handling Examples

### Not a Git Repository

```bash
$ cd /tmp
$ python gitflow.py status
[X] Not a git repository
[INFO] Run 'gitflow init' or 'git init' to initialize
```

### No Remote Configured

```bash
$ python gitflow.py commit feat "New feature"
[...] Staging changes...
[...] Committing: feat: New feature
[OK] Committed: [FEAT] New feature
[...] Pushing to remote...
[!] Push failed: No remote configured
[INFO] Run 'git push' manually if needed
```

### No Changes to Commit

```bash
$ python gitflow.py commit fix "Fix bug"
[...] Staging changes...
[...] Committing: fix: Fix bug
[X] Failed to commit: nothing to commit, working tree clean
```

---

## Tips and Tricks

### 1. Alias for Convenience
```bash
# Add to your shell profile
alias gf="python C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow/gitflow.py"

# Then use:
gf commit feat "Add feature"
gf log
gf stats
```

### 2. Quick Status Check
```bash
# Fast morning overview
gf status && gf log --count 3
```

### 3. Release Preparation
```bash
# Generate changelog and check stats
gf changelog --since last-release-date --output CHANGELOG.md
gf stats
gf cleanup --force
```

### 4. Code Review Helper
```bash
# See what happened on a branch
gf log --count 20
gf branches --remote
```

---

**Last Updated:** January 24, 2026
**Maintained By:** Atlas (Team Brain)
