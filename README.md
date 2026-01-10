# 🌊 GitFlow - Smart Git Workflow Assistant

**Simple. Powerful. For Developers.**

A CLI tool that makes common git operations easier - conventional commits, branch cleanup, repository stats, changelog generation, and more.

---

## 🎯 Why GitFlow?

**Problem:** Developers use git daily but struggle with:
- Writing consistent commit messages
- Remembering conventional commit formats
- Cleaning up old branches
- Generating changelogs
- Getting quick repository insights

**Solution:** GitFlow provides:
- ✅ **Conventional commits** - Pre-formatted commit types
- ✅ **Branch management** - Easy cleanup of merged branches
- ✅ **Repository stats** - Instant insights on commits, files, contributors
- ✅ **Changelog generation** - Auto-generate from commit history
- ✅ **Enhanced status** - Better overview than `git status`
- ✅ **Zero dependencies** - Uses native git CLI

---

## 🚀 Quick Start

```bash
# Navigate to your git repository
cd my-project

# Create a conventional commit
python gitflow.py commit feat "Add user authentication"

# View repository statistics
python gitflow.py stats

# Generate changelog
python gitflow.py changelog --since 7.days

# Clean up merged branches
python gitflow.py cleanup --dry-run
```

---

## 📖 Commands

### 1. Conventional Commits

Create properly formatted commits following conventional commit standards:

```bash
# Basic syntax
python gitflow.py commit <type> "message"

# Types available:
# feat     - ✨ New feature
# fix      - 🐛 Bug fix  
# docs     - 📝 Documentation
# style    - 💎 Code style
# refactor - ♻️  Refactor
# perf     - ⚡ Performance
# test     - ✅ Tests
# chore    - 🔧 Chore
# build    - 📦 Build
# ci       - 👷 CI/CD

# Examples:
python gitflow.py commit feat "Add login page"
python gitflow.py commit fix "Fix navbar responsive issue"
python gitflow.py commit docs "Update API documentation"

# With scope:
python gitflow.py commit feat "Add export button" --scope dashboard

# Without auto-push:
python gitflow.py commit fix "Fix typo" --no-push
```

### 2. Commit Log

View recent commits in a clean format:

```bash
# Last 10 commits (default)
python gitflow.py log

# Custom count
python gitflow.py log --count 20

# Output:
# 📝 Recent Commits
#
# a3b2c1d  feat: Add user authentication
#          John Doe • 2 hours ago
#
# d4e5f6g  fix: Fix login button styling
#          Jane Smith • 5 hours ago
```

### 3. Repository Statistics

Get instant insights about your repository:

```bash
python gitflow.py stats

# Output:
# 📊 Repository Statistics
#
# Total Commits:     342
# Total Files:       87
# Contributors:      5
# Recent Activity:   23 commits (last 30 days)
#
# 👥 Top Contributors:
#    156 commits  John Doe
#     98 commits  Jane Smith
#     45 commits  Bob Johnson
```

### 4. Branch Management

List and manage branches:

```bash
# List local branches
python gitflow.py branches

# List remote branches
python gitflow.py branches --remote

# Output:
# 🌿 Local Branches
#
#   → main
#     feature/login
#     feature/dashboard
#     bugfix/navbar
```

### 5. Branch Cleanup

Clean up merged branches safely:

```bash
# Preview what would be deleted
python gitflow.py cleanup --dry-run

# Output:
# 🔍 Finding merged branches...
#
# 🗑️  These branches can be deleted:
#
#   • feature/old-login
#   • bugfix/fix-typo
#   • feature/completed-feature
#
# 📊 Total: 3 branch(es)
# 💡 Run with --force to actually delete

# Actually delete merged branches
python gitflow.py cleanup --force
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

# Output:
# # Changelog
#
# Generated: 2026-01-10 00:30
#
# ## ✨ New feature
# - Add user authentication
# - Add dashboard page
#
# ## 🐛 Bug fix
# - Fix navbar responsive issue
# - Fix login button styling
```

### 7. Enhanced Status

Better overview than regular git status:

```bash
python gitflow.py status

# Output:
# 🌿 On branch: main
#
# 📝 Changes:
#   M src/app.py
#   A new-file.txt
#   D old-file.txt
#
# 📌 Last commit: a3b2c1d - feat: Add user auth
#    John Doe • 2 hours ago
```

### 8. Initialize Repository

Quick git init:

```bash
python gitflow.py init
# ✅ Initialized git repository
```

---

## 💡 Examples

### Example 1: Daily Workflow

```bash
# Morning: Check what's happening
$ python gitflow.py status
$ python gitflow.py log --count 5

# Work on feature
$ # ... make changes ...

# Commit work
$ python gitflow.py commit feat "Add user profile page"
📦 Staging changes...
💾 Committing: feat: Add user profile page
✅ Committed: ✨ New feature
📤 Pushing to remote...
✅ Pushed to remote
```

### Example 2: Release Preparation

```bash
# Generate changelog since last release
$ python gitflow.py changelog --since 2024-01-01 --output CHANGELOG.md
✅ Changelog saved to: CHANGELOG.md

# Check repository stats
$ python gitflow.py stats

# Clean up merged branches
$ python gitflow.py cleanup --force
✅ Deleted 5 branch(es)
```

### Example 3: Code Review

```bash
# Check recent activity
$ python gitflow.py log --count 20

# See all branches
$ python gitflow.py branches --remote

# Check repository health
$ python gitflow.py stats
```

---

## 🎨 Commit Types Reference

| Type | Emoji | Description | Example |
|------|-------|-------------|---------|
| `feat` | ✨ | New feature | `feat: Add user login` |
| `fix` | 🐛 | Bug fix | `fix: Fix navbar overflow` |
| `docs` | 📝 | Documentation | `docs: Update API guide` |
| `style` | 💎 | Code style/formatting | `style: Format with prettier` |
| `refactor` | ♻️ | Code refactoring | `refactor: Extract helper function` |
| `perf` | ⚡ | Performance improvement | `perf: Optimize image loading` |
| `test` | ✅ | Add/update tests | `test: Add login tests` |
| `chore` | 🔧 | Maintenance | `chore: Update dependencies` |
| `build` | 📦 | Build system | `build: Add webpack config` |
| `ci` | 👷 | CI/CD changes | `ci: Add GitHub Actions` |

---

## 🔧 Use Cases

### For Solo Developers
- Consistent commit messages without memorizing formats
- Quick repository insights
- Clean up old branches easily
- Generate changelogs for releases

### For Teams
- Enforce conventional commit standards
- Track contributor activity
- Generate release notes automatically
- Maintain clean branch structure

### For Open Source
- Professional commit history
- Easy changelog generation
- Repository health monitoring
- Contributor statistics

---

## ❓ FAQ

### Q: Do I need to install anything?
**A:** Just Python 3.6+ and git. No external packages required!

### Q: Does this replace git?
**A:** No! GitFlow uses git under the hood. It's a helper, not a replacement.

### Q: What's a conventional commit?
**A:** A format like `type: message` (e.g., `feat: Add login`). It makes commits consistent and enables automation.

### Q: Will this work with my existing repo?
**A:** Yes! GitFlow works with any git repository.

### Q: Can I customize commit types?
**A:** Currently no, but you can edit the `COMMIT_TYPES` dict in the code.

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

## 🤝 Contributing

Contributions welcome! This is a simple tool - feel free to add features.

---

## 🚀 Quick Reference

```bash
# Commits
gitflow commit <type> "message" [--scope X] [--no-push]

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

**🌊 Make your git workflow flow!**
