# GitFlow - Integration Plan

**Goal:** 100% Utilization & Compliance  
**Target Date:** 1 week from deployment  
**Owner:** Atlas (Team Brain)

---

## 🎯 INTEGRATION GOALS

| Goal | Target | Metric |
|------|--------|--------|
| AI Agent Adoption | 100% | 5/5 agents using |
| Daily Usage | 10+ uses/day | Tool logs |
| Commit Consistency | 95%+ | Conventional commit format |

---

## 📦 BCH INTEGRATION

### Overview
GitFlow is primarily a CLI/development tool. BCH integration is **optional** but can be useful for:
- Repository monitoring dashboard
- Team activity reports
- Automated changelog generation

### Potential BCH Endpoints

**Endpoint 1:** `/api/tools/gitflow/stats`
```python
@router.get("/gitflow/stats")
async def get_repo_stats(repo_path: str):
    """Get repository statistics."""
    import sys
    sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
    from gitflow import GitFlow
    
    original_dir = os.getcwd()
    try:
        os.chdir(repo_path)
        gf = GitFlow()
        if gf.is_git_repo():
            stats = gf.get_repo_stats()
            return {"status": "success", "stats": stats}
        return {"status": "error", "message": "Not a git repository"}
    finally:
        os.chdir(original_dir)
```

**Endpoint 2:** `/api/tools/gitflow/log`
```python
@router.get("/gitflow/log")
async def get_commit_log(repo_path: str, count: int = 10):
    """Get recent commits."""
    # Similar pattern to above
    gf = GitFlow()
    commits = gf.get_commit_log(count=count)
    return {"status": "success", "commits": commits}
```

### @mention Handler (Optional)

**Pattern:** `@gitflow [command] [args]`

**Example:**
```
User: @gitflow stats /path/to/repo
BCH: Repository Statistics:
     Commits: 342, Files: 87, Contributors: 5
```

---

## 🤖 AI AGENT INTEGRATION

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | Commit standards enforcement, repo oversight | CLI/Python | HIGH |
| **Atlas** | Tool development, automated commits | CLI/Python | HIGH |
| **Clio** | Linux development, repo management | CLI | HIGH |
| **Nexus** | Cross-platform development | CLI/Python | MEDIUM |
| **Bolt** | Bulk operations, automation | CLI | MEDIUM |

### Agent-Specific Workflows

#### Forge (Orchestrator / Reviewer)

**Primary Use Cases:**
1. Review commit history for quality
2. Generate changelogs for releases
3. Monitor repository health
4. Enforce commit message standards

**Integration Steps:**
1. Import GitFlow in orchestration scripts
2. Use `get_commit_log()` to review recent changes
3. Use `get_repo_stats()` for health monitoring
4. Generate changelogs for release planning

**Example Workflow:**
```python
# Forge reviewing repository before release
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow

gf = GitFlow()

# Review recent activity
print("=== Repository Health Check ===")
stats = gf.get_repo_stats()
print(f"Total commits: {stats['total_commits']}")
print(f"Recent activity: {stats['commits_last_30_days']} commits (30 days)")

# Check commit message quality
commits = gf.get_commit_log(count=20)
conventional_count = 0
for commit in commits:
    msg = commit['message']
    # Check for conventional format (type: message)
    if ':' in msg and msg.split(':')[0].lower() in ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'chore', 'build', 'ci']:
        conventional_count += 1

print(f"Conventional commits: {conventional_count}/{len(commits)} ({100*conventional_count//len(commits)}%)")

# Generate release changelog
changelog = gf.generate_changelog(since='30.days')
print("\n=== Changelog Preview ===")
print(changelog[:500] + "...")
```

#### Atlas (Executor / Builder)

**Primary Use Cases:**
1. Create consistent commits during tool development
2. Track development progress
3. Maintain clean git history
4. Generate documentation from commits

**Integration Steps:**
1. Use CLI for all commits during development
2. Follow conventional commit format religiously
3. Use scopes for module organization
4. Generate changelogs for tool releases

**Example Workflow:**
```python
# Atlas tool development workflow
import subprocess
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow

gf = GitFlow()

# Start development session
print("=== Development Session Start ===")
print(f"Branch: {gf.get_current_branch()}")

# After making changes, commit with GitFlow CLI
def commit_changes(commit_type: str, message: str, scope: str = None):
    """Helper to commit using GitFlow CLI."""
    cmd = ['python', 'gitflow.py', 'commit', commit_type, message]
    if scope:
        cmd.extend(['--scope', scope])
    subprocess.run(cmd)

# Example commits during development
# commit_changes('feat', 'Add new validation function', 'core')
# commit_changes('test', 'Add tests for validation', 'core')
# commit_changes('docs', 'Update README with examples')

# End of session: review work
commits = gf.get_commit_log(count=5)
print(f"\n=== Session Summary ({len(commits)} commits) ===")
for c in commits:
    print(f"  {c['hash']} - {c['message']}")
```

#### Clio (Linux / Ubuntu Agent)

**Primary Use Cases:**
1. CLI-first git workflow
2. Repository management on Linux servers
3. Automation scripts
4. Cross-system development

**Platform Considerations:**
- Works natively on Linux without modification
- Shell aliases recommended for convenience
- Can be integrated into bash scripts

**Example:**
```bash
# Clio CLI usage in bash script
#!/bin/bash

# Add to ~/.bashrc for convenience
alias gf="python3 ~/AutoProjects/GitFlow/gitflow.py"

# Daily workflow
gf status
gf log --count 5

# Commit work
gf commit feat "Add new feature"

# Generate weekly report
gf changelog --since 7.days --output ~/reports/weekly_$(date +%Y%m%d).md
gf stats >> ~/reports/stats_$(date +%Y%m%d).txt
```

#### Nexus (Multi-Platform Agent)

**Primary Use Cases:**
1. Cross-platform development consistency
2. Universal git workflow
3. Platform-agnostic scripting

**Cross-Platform Notes:**
- Works on Windows, Linux, macOS
- Uses Python's pathlib for path handling
- Git must be in PATH on all platforms

**Example:**
```python
# Nexus cross-platform workflow
import platform
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow

gf = GitFlow()

print(f"Running on: {platform.system()}")
print(f"Git repository: {gf.is_git_repo()}")

if gf.is_git_repo():
    # Same operations work on all platforms
    stats = gf.get_repo_stats()
    print(f"Repository has {stats['total_commits']} commits")
    
    branch = gf.get_current_branch()
    print(f"Current branch: {branch}")
```

#### Bolt (Cline / Free Executor)

**Primary Use Cases:**
1. Bulk commit operations
2. Automated repository maintenance
3. Scheduled tasks (cleanup, changelogs)

**Cost Considerations:**
- Zero API cost - purely local operations
- Can handle repetitive git tasks
- Good for maintenance automation

**Example:**
```bash
# Bolt automation script
#!/bin/bash

# Weekly cleanup script
cd /path/to/repos

for dir in */; do
    if [ -d "$dir/.git" ]; then
        echo "Processing: $dir"
        cd "$dir"
        
        # Clean up merged branches
        python gitflow.py cleanup --force
        
        # Generate weekly changelog
        python gitflow.py changelog --since 7.days --output CHANGELOG_WEEKLY.md
        
        cd ..
    fi
done

echo "Maintenance complete!"
```

---

## 🔗 INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With AgentHealth

**Correlation Use Case:** Track git activity alongside agent health metrics.

**Integration Pattern:**
```python
from agenthealth import AgentHealth
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow

health = AgentHealth()
gf = GitFlow()

# Start session
session_id = "dev_session_001"
health.start_session("ATLAS", session_id=session_id)

# Track git work
stats = gf.get_repo_stats()
health.heartbeat("ATLAS", status="active", 
                 notes=f"Working on repo with {stats['total_commits']} commits")

# End session
health.end_session("ATLAS", session_id=session_id, status="success")
```

### With SynapseLink

**Notification Use Case:** Share git activity with team.

**Integration Pattern:**
```python
from synapselink import quick_send
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow

gf = GitFlow()

# Generate report
stats = gf.get_repo_stats()
commits = gf.get_commit_log(count=5)

# Format message
recent_commits = "\n".join([f"- {c['message']}" for c in commits])

# Notify team
quick_send(
    "TEAM",
    "Repository Status Update",
    f"Repository Health:\n"
    f"- Total commits: {stats['total_commits']}\n"
    f"- Contributors: {stats['contributors']}\n"
    f"- Recent activity: {stats['commits_last_30_days']} (30 days)\n\n"
    f"Recent commits:\n{recent_commits}",
    priority="NORMAL"
)
```

### With TaskQueuePro

**Task Management Use Case:** Track git-related tasks.

**Integration Pattern:**
```python
from taskqueuepro import TaskQueuePro
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow

queue = TaskQueuePro()
gf = GitFlow()

# Create task for branch cleanup
task_id = queue.create_task(
    title="Monthly branch cleanup",
    agent="ATLAS",
    priority=2,
    metadata={"tool": "GitFlow", "operation": "cleanup"}
)

# Execute
queue.start_task(task_id)
branches = gf.cleanup_branches(dry_run=False)

# Complete
queue.complete_task(
    task_id,
    result={"deleted_branches": len(branches), "branches": branches}
)
```

### With MemoryBridge

**Context Persistence Use Case:** Store git history summaries.

**Integration Pattern:**
```python
from memorybridge import MemoryBridge
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow
from datetime import datetime

memory = MemoryBridge()
gf = GitFlow()

# Get current stats
stats = gf.get_repo_stats()

# Store in memory
memory.set("gitflow_last_stats", {
    "timestamp": datetime.now().isoformat(),
    "total_commits": stats['total_commits'],
    "contributors": stats['contributors'],
    "recent_activity": stats['commits_last_30_days']
})

memory.sync()
```

### With SessionReplay

**Debugging Use Case:** Record git operations for debugging.

**Integration Pattern:**
```python
from sessionreplay import SessionReplay
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow

replay = SessionReplay()
gf = GitFlow()

# Start recording
session_id = replay.start_session("ATLAS", task="Git operations")

# Log operations
replay.log_input(session_id, "Getting repository stats")
stats = gf.get_repo_stats()
replay.log_output(session_id, f"Stats: {stats}")

replay.log_input(session_id, "Generating changelog")
changelog = gf.generate_changelog(since='7.days')
replay.log_output(session_id, f"Changelog generated: {len(changelog)} chars")

# End session
replay.end_session(session_id, status="COMPLETED")
```

### With ConfigManager

**Configuration Use Case:** Centralize GitFlow settings.

**Integration Pattern:**
```python
from configmanager import ConfigManager
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow

config = ConfigManager()

# Load GitFlow config
gf_config = config.get("gitflow", {
    "default_commit_type": "feat",
    "auto_push": True,
    "protected_branches": ["main", "master", "develop"],
    "changelog_format": "markdown"
})

# Use config with GitFlow
gf = GitFlow()
# (Future: pass config to GitFlow constructor)
```

### With CollabSession

**Coordination Use Case:** Coordinate git operations across agents.

**Integration Pattern:**
```python
from collabsession import CollabSession
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow

collab = CollabSession()
gf = GitFlow()

# Create coordination session for release
session_id = collab.start_session(
    "release_v2.0",
    participants=["ATLAS", "CLIO", "FORGE"]
)

# Lock main branch for release
collab.lock_resource(session_id, "branch:main", "FORGE")

try:
    # Generate changelog
    changelog = gf.generate_changelog(since='2026-01-01')
    
    # Clean up branches
    deleted = gf.cleanup_branches(dry_run=False)
    
    # Share results
    collab.broadcast(session_id, 
        f"Release prep complete: {len(deleted)} branches cleaned")
    
finally:
    # Release lock
    collab.unlock_resource(session_id, "branch:main")
    collab.end_session(session_id)
```

---

## 🚀 ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)

**Goal:** All agents aware and can use basic features

**Steps:**
1. [x] Tool deployed (already on GitHub)
2. [ ] Quick-start guides sent via Synapse
3. [ ] Each agent tests basic workflow
4. [ ] Feedback collected

**Success Criteria:**
- All 5 agents have used tool at least once
- No blocking issues reported

### Phase 2: Integration (Week 2-3)

**Goal:** Integrated into daily workflows

**Steps:**
1. [ ] Add to agent startup routines
2. [ ] Create shell aliases for convenience
3. [ ] Integrate with existing tools
4. [ ] Monitor usage patterns

**Success Criteria:**
- Used daily by at least 3 agents
- Conventional commit adoption > 80%

### Phase 3: Optimization (Week 4+)

**Goal:** Optimized and fully adopted

**Steps:**
1. [ ] Collect efficiency metrics
2. [ ] Implement v1.1 improvements
3. [ ] Create advanced workflow examples
4. [ ] Full Team Brain ecosystem integration

**Success Criteria:**
- Measurable time savings
- Positive feedback from all agents
- v1.1 improvements identified

---

## 📊 SUCCESS METRICS

**Adoption Metrics:**
- Number of agents using tool: [Track]
- Daily usage count: [Track]
- Conventional commit percentage: [Track]

**Efficiency Metrics:**
- Time saved per commit: ~30 seconds
- Cleanup time saved: ~5 minutes/week
- Changelog generation time saved: ~10 minutes/release

**Quality Metrics:**
- Commit message consistency: [Track]
- Bug reports: [Track]
- Feature requests: [Track]

---

## 🛠️ TECHNICAL INTEGRATION DETAILS

### Import Paths

```python
# Standard import
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/GitFlow")
from gitflow import GitFlow, COMMIT_TYPES

# After pip install
from gitflow import GitFlow
```

### Configuration Integration

**Future Config File:** `~/.gitflowrc`

```json
{
  "auto_push": true,
  "default_commit_type": "feat",
  "protected_branches": ["main", "master", "develop"],
  "changelog_format": "markdown"
}
```

### Error Handling Integration

**Standardized Return Values:**
- Methods return `(success: bool, output: str)` tuples
- Empty lists/dicts on failure (never None)
- Exceptions only for critical errors

### Logging Integration

**Log Format:** Compatible with Team Brain standard

**Log Location:** Console output (future: `~/.teambrain/logs/gitflow.log`)

---

## 🔧 MAINTENANCE & SUPPORT

### Update Strategy
- Minor updates (v1.x): As needed
- Major updates (v2.0+): Quarterly
- Bug fixes: Immediate

### Support Channels
- GitHub Issues: Bug reports
- Synapse: Team Brain discussions
- Direct to Atlas: Complex issues

### Known Limitations
- Requires git in PATH
- No GUI interface
- Single repository at a time
- No merge conflict resolution

---

## 📚 ADDITIONAL RESOURCES

- Main Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Quick Start Guides: [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- GitHub: https://github.com/DonkRonk17/GitFlow

---

**Last Updated:** January 24, 2026
**Maintained By:** Atlas (Team Brain)
