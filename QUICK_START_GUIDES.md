# GitFlow - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#-forge-quick-start)
- [Atlas (Executor)](#-atlas-quick-start)
- [Clio (Linux Agent)](#-clio-quick-start)
- [Nexus (Multi-Platform)](#-nexus-quick-start)
- [Bolt (Free Executor)](#-bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Use GitFlow for commit standards enforcement and repository oversight

### Step 1: Installation Check

```bash
# Navigate to any git repository
cd C:\Users\logan\OneDrive\Documents\AutoProjects

# Verify GitFlow is available
python GitFlow/gitflow.py --help

# Check in a specific repo
cd SynapseLink
python ../GitFlow/gitflow.py stats
```

### Step 2: First Use - Repository Health Check

```python
# In your Forge session
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow

gf = GitFlow()

# Quick health check
stats = gf.get_repo_stats()
print(f"Repository: {stats['total_commits']} commits, {stats['contributors']} contributors")
print(f"Recent activity: {stats['commits_last_30_days']} commits (30 days)")
```

### Step 3: Review Commit Quality

```python
# Check commit message consistency
commits = gf.get_commit_log(count=20)

conventional_formats = ['feat:', 'fix:', 'docs:', 'style:', 'refactor:', 
                        'perf:', 'test:', 'chore:', 'build:', 'ci:']

good_commits = sum(1 for c in commits 
                   if any(c['message'].lower().startswith(f) for f in conventional_formats))

print(f"Conventional commits: {good_commits}/{len(commits)} ({100*good_commits//len(commits)}%)")

if good_commits < len(commits) * 0.8:
    print("[!] Consider enforcing conventional commit format")
```

### Step 4: Generate Release Changelog

```bash
# CLI usage for release preparation
python gitflow.py changelog --since 2026-01-01 --output CHANGELOG.md

# Preview in console
python gitflow.py changelog --since 7.days
```

### Common Forge Commands

```bash
# Repository health
python gitflow.py stats

# Review recent work
python gitflow.py log --count 20

# Generate changelog for release
python gitflow.py changelog --since [date] --output CHANGELOG.md

# Check branches (for cleanup review)
python gitflow.py cleanup --dry-run
```

### Next Steps for Forge

1. Review [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Forge section
2. Set up commit message guidelines for team
3. Add GitFlow stats to orchestration reports
4. Schedule weekly changelog generation

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Use GitFlow for consistent commits during tool development

### Step 1: Installation Check

```bash
# Verify GitFlow works
cd C:\Users\logan\OneDrive\Documents\AutoProjects
python GitFlow/gitflow.py --version
```

### Step 2: First Use - Development Commit

```bash
# Navigate to your working project
cd MyNewTool

# After making changes, create a conventional commit
python ../GitFlow/gitflow.py commit feat "Add main functionality"

# Output:
# [...] Staging changes...
# [...] Committing: feat: Add main functionality
# [OK] Committed: [FEAT] New feature
# [...] Pushing to remote...
# [OK] Pushed to remote
```

### Step 3: Tool Development Workflow

```bash
# Start of session: Check status
python ../GitFlow/gitflow.py status
python ../GitFlow/gitflow.py log --count 3

# During development - use appropriate commit types:
# New feature
python ../GitFlow/gitflow.py commit feat "Add validation module" --scope core

# Bug fix discovered
python ../GitFlow/gitflow.py commit fix "Handle edge case in parser" --scope parser

# Updated tests
python ../GitFlow/gitflow.py commit test "Add unit tests for validation"

# Documentation
python ../GitFlow/gitflow.py commit docs "Update README with examples"

# Local commit only (work in progress)
python ../GitFlow/gitflow.py commit chore "WIP - refactoring" --no-push
```

### Step 4: End of Session Review

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow

gf = GitFlow()

# Session summary
print("=== Session Summary ===")
commits = gf.get_commit_log(count=5)
for c in commits:
    print(f"  {c['hash']} - {c['message']}")

# Check for uncommitted changes
success, output = gf.run_git(['status', '--short'])
if output:
    print("\n[!] Uncommitted changes:")
    print(output)
```

### Common Atlas Commands

```bash
# Daily workflow
python gitflow.py status                           # Check state
python gitflow.py commit feat "Description"        # New feature
python gitflow.py commit fix "Bug fix" --scope X   # Bug fix with scope
python gitflow.py commit test "Add tests"          # Tests
python gitflow.py commit docs "Update docs"        # Documentation
python gitflow.py log --count 5                    # Review work
```

### Next Steps for Atlas

1. Always use GitFlow for commits (consistency!)
2. Use scopes for multi-module projects
3. Generate changelog before tool release
4. Integrate into Holy Grail automation workflow

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Use GitFlow in Linux CLI environment

### Step 1: Linux Installation

```bash
# Clone from GitHub (if needed)
cd ~/AutoProjects
git clone https://github.com/DonkRonk17/GitFlow.git

# Verify installation
python3 GitFlow/gitflow.py --version
```

### Step 2: Shell Alias Setup (Recommended)

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'alias gf="python3 ~/AutoProjects/GitFlow/gitflow.py"' >> ~/.bashrc
source ~/.bashrc

# Now use short command
gf --help
gf stats
gf log
```

### Step 3: First Use - Linux CLI Workflow

```bash
# Navigate to repository
cd /path/to/my-project

# Check status
gf status

# Make changes and commit
gf commit feat "Add Linux-specific feature"

# View recent activity
gf log --count 10

# Generate changelog
gf changelog --since 7.days
```

### Step 4: Linux Automation Script

```bash
#!/bin/bash
# save as ~/scripts/git-daily.sh

# Daily git maintenance script
cd ~/projects

for dir in */; do
    if [ -d "$dir/.git" ]; then
        echo "=== Processing: $dir ==="
        cd "$dir"
        
        # Show status
        gf status
        
        # Show recent commits
        gf log --count 3
        
        cd ..
    fi
done
```

### Common Clio Commands

```bash
# Using alias 'gf'
gf status              # Check repository state
gf log                 # View recent commits
gf stats               # Repository statistics
gf branches            # List branches
gf commit feat "Msg"   # Conventional commit
gf changelog --since 7.days  # Generate changelog
gf cleanup --dry-run   # Preview cleanup
```

### Platform-Specific Notes

- Uses `python3` by default on most Linux systems
- Shell aliases make CLI usage faster
- Can be integrated into cron jobs
- Works with any terminal emulator

### Next Steps for Clio

1. Add shell alias to your dotfiles
2. Create automation scripts for common tasks
3. Set up cron job for weekly changelog generation
4. Test on Ubuntu environment

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Use GitFlow consistently across platforms

### Step 1: Platform Detection

```python
import platform
import sys

# Platform-agnostic path
if platform.system() == "Windows":
    sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
else:
    sys.path.append("/home/logan/AutoProjects/GitFlow")

from gitflow import GitFlow

print(f"Running on: {platform.system()}")
gf = GitFlow()
print(f"Git available: {gf.run_git(['--version'])[0]}")
```

### Step 2: First Use - Cross-Platform Workflow

```python
from gitflow import GitFlow

gf = GitFlow()

# These operations work identically on all platforms
if gf.is_git_repo():
    # Get stats
    stats = gf.get_repo_stats()
    print(f"Commits: {stats['total_commits']}")
    
    # Get branch
    branch = gf.get_current_branch()
    print(f"Branch: {branch}")
    
    # Get commits
    commits = gf.get_commit_log(count=5)
    for c in commits:
        print(f"  {c['hash']} - {c['message']}")
```

### Step 3: Platform-Adaptive CLI Usage

**Windows:**
```cmd
cd C:\Users\logan\OneDrive\Documents\AutoProjects\MyProject
python ..\GitFlow\gitflow.py stats
python ..\GitFlow\gitflow.py commit feat "Add feature"
```

**Linux/macOS:**
```bash
cd ~/AutoProjects/MyProject
python3 ../GitFlow/gitflow.py stats
python3 ../GitFlow/gitflow.py commit feat "Add feature"
```

### Step 4: Cross-Platform Script Template

```python
#!/usr/bin/env python3
"""Cross-platform git workflow script."""
import platform
import sys
from pathlib import Path

# Platform-adaptive import
if platform.system() == "Windows":
    base_path = Path("C:/Users/logan/OneDrive/Documents/AutoProjects")
else:
    base_path = Path.home() / "AutoProjects"

sys.path.append(str(base_path / "GitFlow"))
from gitflow import GitFlow

def main():
    gf = GitFlow()
    
    if not gf.is_git_repo():
        print("[X] Not a git repository")
        return
    
    print(f"Platform: {platform.system()}")
    print(f"Branch: {gf.get_current_branch()}")
    
    stats = gf.get_repo_stats()
    print(f"Commits: {stats['total_commits']}")
    print(f"Files: {stats['total_files']}")

if __name__ == "__main__":
    main()
```

### Platform-Specific Considerations

**Windows:**
- Use `python` command
- Backslashes in paths (or forward slashes)
- Git for Windows recommended

**Linux:**
- Use `python3` command
- Forward slashes in paths
- Git usually pre-installed

**macOS:**
- Use `python3` command
- Forward slashes in paths
- Install git via Xcode or Homebrew

### Next Steps for Nexus

1. Test on all 3 platforms
2. Create platform-adaptive scripts
3. Report any platform-specific issues
4. Add to multi-platform workflows

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Use GitFlow for bulk operations without API costs

### Step 1: Verify Free Access

```bash
# No API key required!
python gitflow.py --version

# All operations are local (no cost)
python gitflow.py stats
python gitflow.py log
```

### Step 2: First Use - Bulk Operations

```bash
# Batch cleanup across multiple repos
for dir in */; do
    if [ -d "$dir/.git" ]; then
        echo "Processing: $dir"
        (cd "$dir" && python ../GitFlow/gitflow.py cleanup --force)
    fi
done
```

### Step 3: Automation Script

```bash
#!/bin/bash
# Automated git maintenance - runs without human interaction

REPOS_DIR="/path/to/repos"
GITFLOW="/path/to/GitFlow/gitflow.py"
LOG_FILE="/tmp/git-maintenance.log"

echo "Git Maintenance - $(date)" > "$LOG_FILE"

cd "$REPOS_DIR"
for dir in */; do
    if [ -d "$dir/.git" ]; then
        echo "=== $dir ===" >> "$LOG_FILE"
        cd "$dir"
        
        # Cleanup merged branches
        python "$GITFLOW" cleanup --force >> "$LOG_FILE" 2>&1
        
        # Generate weekly changelog
        python "$GITFLOW" changelog --since 7.days \
            --output "CHANGELOG_WEEKLY.md" >> "$LOG_FILE" 2>&1
        
        cd ..
    fi
done

echo "Complete: $(date)" >> "$LOG_FILE"
```

### Step 4: Scheduled Task Example

```bash
# Add to crontab for weekly execution
# crontab -e
# 0 2 * * 0 /path/to/git-maintenance.sh

# Or Windows Task Scheduler:
# Action: python C:\...\GitFlow\gitflow.py
# Arguments: cleanup --force
# Trigger: Weekly
```

### Common Bolt Commands

```bash
# Bulk operations (no cost!)
python gitflow.py cleanup --force        # Clean all merged branches
python gitflow.py changelog --since 30.days --output CHANGELOG.md
python gitflow.py stats                   # Repository metrics

# Batch processing
for d in */; do (cd "$d" && python gitflow.py stats); done
```

### Cost Considerations

- **Zero API cost** - All operations are local
- **No tokens used** - Pure git commands
- **Good for:** Repetitive maintenance tasks
- **Good for:** Scheduled automation
- **Good for:** Bulk processing

### Next Steps for Bolt

1. Add to Cline workflows
2. Create maintenance scripts
3. Schedule regular cleanup tasks
4. Report any issues via Synapse

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/GitFlow/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message Atlas

---

**Last Updated:** January 24, 2026
**Maintained By:** Atlas (Team Brain)
