# GitFlow - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

GitFlow is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: GitFlow + AgentHealth](#pattern-1-gitflow--agenthealth)
2. [Pattern 2: GitFlow + SynapseLink](#pattern-2-gitflow--synapselink)
3. [Pattern 3: GitFlow + TaskQueuePro](#pattern-3-gitflow--taskqueuepro)
4. [Pattern 4: GitFlow + MemoryBridge](#pattern-4-gitflow--memorybridge)
5. [Pattern 5: GitFlow + SessionReplay](#pattern-5-gitflow--sessionreplay)
6. [Pattern 6: GitFlow + ContextCompressor](#pattern-6-gitflow--contextcompressor)
7. [Pattern 7: GitFlow + ConfigManager](#pattern-7-gitflow--configmanager)
8. [Pattern 8: GitFlow + CollabSession](#pattern-8-gitflow--collabsession)
9. [Pattern 9: Multi-Tool Development Workflow](#pattern-9-multi-tool-development-workflow)
10. [Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: GitFlow + AgentHealth

**Use Case:** Correlate git activity with agent health monitoring

**Why:** Understand how development work affects agent performance and track productivity

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects")
from AgentHealth.agenthealth import AgentHealth
from GitFlow.gitflow import GitFlow

# Initialize both tools
health = AgentHealth()
gf = GitFlow()

# Start development session with shared ID
session_id = "dev_session_001"
health.start_session("ATLAS", session_id=session_id)

try:
    # Check repository health
    health.heartbeat("ATLAS", status="active", notes="Starting git analysis")
    
    if gf.is_git_repo():
        # Get repository statistics
        stats = gf.get_repo_stats()
        health.heartbeat("ATLAS", status="active", 
                        notes=f"Repo: {stats['total_commits']} commits")
        
        # Get recent commits
        commits = gf.get_commit_log(count=10)
        health.heartbeat("ATLAS", status="active",
                        notes=f"Analyzed {len(commits)} recent commits")
        
        # Log success
        health.end_session("ATLAS", session_id=session_id, status="success")
        print(f"[OK] Session complete: {stats['total_commits']} commits analyzed")
    else:
        health.end_session("ATLAS", session_id=session_id, status="failed")
        print("[X] Not a git repository")
        
except Exception as e:
    health.log_error("ATLAS", str(e))
    health.end_session("ATLAS", session_id=session_id, status="failed")
    print(f"[X] Error: {e}")
```

**Result:** Git activity is correlated with agent health metrics for analysis

---

## Pattern 2: GitFlow + SynapseLink

**Use Case:** Notify Team Brain when significant git events occur

**Why:** Keep team informed of repository activity automatically

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects")
from SynapseLink.synapselink import quick_send
from GitFlow.gitflow import GitFlow

gf = GitFlow()

# Get repository status
stats = gf.get_repo_stats()
commits = gf.get_commit_log(count=5)

# Format recent commits
recent = "\n".join([f"- {c['hash']}: {c['message']}" for c in commits])

# Notify team of repository status
quick_send(
    "TEAM",
    "Daily Repository Status",
    f"Repository Health Report\n"
    f"========================\n"
    f"Total commits: {stats['total_commits']}\n"
    f"Contributors: {stats['contributors']}\n"
    f"Activity (30 days): {stats['commits_last_30_days']} commits\n"
    f"\nRecent Commits:\n{recent}",
    priority="NORMAL"
)

print("[OK] Team notified of repository status")

# Notify on branch cleanup
branches = gf.cleanup_branches(dry_run=True)
if len(branches) > 3:
    quick_send(
        "FORGE",
        "Branch Cleanup Recommended",
        f"Repository has {len(branches)} merged branches that can be deleted:\n"
        + "\n".join([f"- {b}" for b in branches[:10]]),
        priority="LOW"
    )
    print(f"[OK] Cleanup notification sent ({len(branches)} branches)")
```

**Result:** Team stays informed without manual status updates

---

## Pattern 3: GitFlow + TaskQueuePro

**Use Case:** Manage git-related tasks in centralized queue

**Why:** Track git operations alongside other agent tasks

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects")
from TaskQueuePro.taskqueuepro import TaskQueuePro
from GitFlow.gitflow import GitFlow

queue = TaskQueuePro()
gf = GitFlow()

# Create task for branch cleanup
task_id = queue.create_task(
    title="Weekly branch cleanup",
    agent="ATLAS",
    priority=2,
    metadata={"tool": "GitFlow", "operation": "cleanup"}
)

# Mark as in-progress
queue.start_task(task_id)

try:
    # Preview cleanup
    branches_to_delete = gf.cleanup_branches(dry_run=True)
    
    if branches_to_delete:
        # Execute cleanup
        deleted = gf.cleanup_branches(dry_run=False)
        
        # Complete task with results
        queue.complete_task(
            task_id,
            result={
                "status": "success",
                "deleted_count": len(deleted),
                "branches": deleted
            }
        )
        print(f"[OK] Deleted {len(deleted)} branches")
    else:
        queue.complete_task(
            task_id,
            result={"status": "success", "deleted_count": 0, "message": "No branches to clean"}
        )
        print("[OK] No branches needed cleanup")
        
except Exception as e:
    queue.fail_task(task_id, error=str(e))
    print(f"[X] Failed: {e}")
```

**Result:** Git tasks tracked in centralized queue for visibility

---

## Pattern 4: GitFlow + MemoryBridge

**Use Case:** Persist git history summaries to memory core

**Why:** Maintain long-term history of repository evolution

**Code:**

```python
import sys
from datetime import datetime
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects")
from MemoryBridge.memorybridge import MemoryBridge
from GitFlow.gitflow import GitFlow

memory = MemoryBridge()
gf = GitFlow()

# Load historical data
history = memory.get("gitflow_history", default=[])

# Get current stats
stats = gf.get_repo_stats()
commits = gf.get_commit_log(count=5)

# Create snapshot
snapshot = {
    "timestamp": datetime.now().isoformat(),
    "total_commits": stats['total_commits'],
    "total_files": stats['total_files'],
    "contributors": stats['contributors'],
    "recent_activity": stats['commits_last_30_days'],
    "recent_commits": [c['message'] for c in commits],
    "current_branch": gf.get_current_branch()
}

# Append to history (keep last 30 entries)
history.append(snapshot)
history = history[-30:]

# Save to memory
memory.set("gitflow_history", history)
memory.sync()

print(f"[OK] Saved snapshot: {stats['total_commits']} commits")
print(f"[OK] History contains {len(history)} snapshots")

# Analyze trends
if len(history) >= 2:
    growth = history[-1]['total_commits'] - history[0]['total_commits']
    print(f"[INFO] Commit growth since first snapshot: +{growth}")
```

**Result:** Historical data persisted for trend analysis

---

## Pattern 5: GitFlow + SessionReplay

**Use Case:** Record git operations for debugging

**Why:** Replay git workflows when issues occur

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects")
from SessionReplay.sessionreplay import SessionReplay
from GitFlow.gitflow import GitFlow

replay = SessionReplay()
gf = GitFlow()

# Start recording session
session_id = replay.start_session("ATLAS", task="Git repository analysis")

try:
    # Log: Check repository
    replay.log_input(session_id, "Checking if git repository")
    is_repo = gf.is_git_repo()
    replay.log_output(session_id, f"Is git repo: {is_repo}")
    
    if is_repo:
        # Log: Get stats
        replay.log_input(session_id, "Getting repository statistics")
        stats = gf.get_repo_stats()
        replay.log_output(session_id, f"Stats: commits={stats['total_commits']}, files={stats['total_files']}")
        
        # Log: Get commits
        replay.log_input(session_id, "Getting recent commits (10)")
        commits = gf.get_commit_log(count=10)
        replay.log_output(session_id, f"Got {len(commits)} commits")
        
        # Log: Generate changelog
        replay.log_input(session_id, "Generating changelog for last 7 days")
        changelog = gf.generate_changelog(since='7.days')
        replay.log_output(session_id, f"Changelog: {len(changelog)} characters")
        
        # Mark success
        replay.end_session(session_id, status="COMPLETED")
        print("[OK] Session recorded successfully")
    else:
        replay.log_error(session_id, "Not a git repository")
        replay.end_session(session_id, status="FAILED")
        
except Exception as e:
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
    print(f"[X] Error recorded: {e}")
```

**Result:** Full session replay available for debugging

---

## Pattern 6: GitFlow + ContextCompressor

**Use Case:** Compress changelog output before sharing

**Why:** Save tokens when sharing large changelogs

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects")
from ContextCompressor.contextcompressor import ContextCompressor
from GitFlow.gitflow import GitFlow

compressor = ContextCompressor()
gf = GitFlow()

# Generate full changelog (could be large)
changelog = gf.generate_changelog()  # All commits

print(f"Original changelog: {len(changelog)} characters")

# Compress for sharing
compressed = compressor.compress_text(
    changelog,
    query="key changes and important commits",
    method="summary"
)

print(f"Compressed: {len(compressed.compressed_text)} characters")
print(f"Savings: ~{(1 - len(compressed.compressed_text)/len(changelog))*100:.0f}%")

# Share compressed version
print("\n=== Compressed Changelog ===")
print(compressed.compressed_text)
```

**Result:** Large changelogs compressed for efficient sharing

---

## Pattern 7: GitFlow + ConfigManager

**Use Case:** Centralize GitFlow settings

**Why:** Share configuration across tools and agents

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects")
from ConfigManager.configmanager import ConfigManager
from GitFlow.gitflow import GitFlow

config = ConfigManager()

# Load/create GitFlow configuration
gf_config = config.get("gitflow", {
    "auto_push": True,
    "default_commit_type": "feat",
    "protected_branches": ["main", "master", "develop"],
    "changelog_days_default": 7,
    "log_count_default": 10
})

# Use configuration
gf = GitFlow()

# Get commits with configured default
commits = gf.get_commit_log(count=gf_config.get('log_count_default', 10))
print(f"Last {len(commits)} commits:")
for c in commits:
    print(f"  {c['hash']} - {c['message']}")

# Generate changelog with configured default
changelog = gf.generate_changelog(
    since=f"{gf_config.get('changelog_days_default', 7)}.days"
)
print(f"\nChangelog generated for last {gf_config['changelog_days_default']} days")

# Update config if needed
config.set("gitflow.last_used", "2026-01-24")
config.save()
```

**Result:** Centralized configuration for consistent behavior

---

## Pattern 8: GitFlow + CollabSession

**Use Case:** Coordinate git operations across agents

**Why:** Prevent conflicts when multiple agents work on same repo

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects")
from CollabSession.collabsession import CollabSession
from GitFlow.gitflow import GitFlow

collab = CollabSession()
gf = GitFlow()

# Create coordination session for release
session_id = collab.start_session(
    "release_prep_v2.0",
    participants=["ATLAS", "CLIO", "FORGE"]
)

# Lock repository for release operations
collab.lock_resource(session_id, "repo:main-branch", "FORGE")

try:
    # Announce to participants
    collab.broadcast(session_id, "Starting release preparation...")
    
    # Generate changelog
    changelog = gf.generate_changelog(since='2026-01-01')
    collab.broadcast(session_id, f"Changelog generated: {len(changelog)} chars")
    
    # Clean up branches
    branches = gf.cleanup_branches(dry_run=False)
    collab.broadcast(session_id, f"Cleaned {len(branches)} merged branches")
    
    # Get final stats
    stats = gf.get_repo_stats()
    collab.broadcast(session_id, 
        f"Release ready: {stats['total_commits']} commits, {stats['total_files']} files")
    
finally:
    # Always release lock
    collab.unlock_resource(session_id, "repo:main-branch")
    collab.end_session(session_id)
    print("[OK] Release preparation complete")
```

**Result:** Safe, coordinated git operations across agents

---

## Pattern 9: Multi-Tool Development Workflow

**Use Case:** Complete development session using multiple tools

**Why:** Demonstrate real production scenario

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects")
from TaskQueuePro.taskqueuepro import TaskQueuePro
from SessionReplay.sessionreplay import SessionReplay
from AgentHealth.agenthealth import AgentHealth
from SynapseLink.synapselink import quick_send
from GitFlow.gitflow import GitFlow

# Initialize stack
queue = TaskQueuePro()
replay = SessionReplay()
health = AgentHealth()
gf = GitFlow()

# Create task
task_id = queue.create_task("Feature development session", agent="ATLAS")

# Start recording
session_id = replay.start_session("ATLAS", task="Feature development")
health.start_session("ATLAS", session_id=session_id)

try:
    # Start task
    queue.start_task(task_id)
    replay.log_input(session_id, "Starting development session")
    
    # Check repository status
    health.heartbeat("ATLAS", status="active", notes="Checking repo")
    stats = gf.get_repo_stats()
    replay.log_output(session_id, f"Repo: {stats['total_commits']} commits")
    
    # Simulate development work...
    health.heartbeat("ATLAS", status="active", notes="Making changes")
    replay.log_input(session_id, "Development work in progress")
    
    # After development, would commit:
    # gf.run_git(['add', '-A'])
    # gf.run_git(['commit', '-m', 'feat: Add new feature'])
    
    # End of session
    commits = gf.get_commit_log(count=3)
    replay.log_output(session_id, f"Session commits: {len(commits)}")
    
    # Success path
    queue.complete_task(task_id, result={"commits": len(commits)})
    replay.end_session(session_id, status="COMPLETED")
    health.end_session("ATLAS", session_id=session_id, status="success")
    
    # Notify team
    quick_send("TEAM", "Development Session Complete", 
              f"Session finished with {len(commits)} recent commits")
    
    print("[OK] Development session complete")
    
except Exception as e:
    # Failure path
    queue.fail_task(task_id, error=str(e))
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
    health.log_error("ATLAS", str(e))
    health.end_session("ATLAS", session_id=session_id, status="failed")
    
    quick_send("FORGE", "Development Session Failed", str(e), priority="HIGH")
    print(f"[X] Session failed: {e}")
```

**Result:** Fully instrumented, coordinated development workflow

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Ultimate integration - all tools working together

**Why:** Production-grade development operation

**Code:**

```python
import sys
from datetime import datetime
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects")

# Import all tools
from TaskQueuePro.taskqueuepro import TaskQueuePro
from SessionReplay.sessionreplay import SessionReplay
from AgentHealth.agenthealth import AgentHealth
from SynapseLink.synapselink import quick_send
from MemoryBridge.memorybridge import MemoryBridge
from ConfigManager.configmanager import ConfigManager
from GitFlow.gitflow import GitFlow

def full_stack_workflow():
    """Complete workflow using all integrated tools."""
    
    # Initialize
    queue = TaskQueuePro()
    replay = SessionReplay()
    health = AgentHealth()
    memory = MemoryBridge()
    config = ConfigManager()
    gf = GitFlow()
    
    # Load config
    gf_config = config.get("gitflow", {"log_count": 10})
    
    # Create task
    task_id = queue.create_task("Full stack git workflow", agent="ATLAS", priority=1)
    session_id = replay.start_session("ATLAS", task="Full stack workflow")
    health.start_session("ATLAS", session_id=session_id)
    
    results = {
        "start_time": datetime.now().isoformat(),
        "operations": []
    }
    
    try:
        queue.start_task(task_id)
        
        # Operation 1: Repository analysis
        replay.log_input(session_id, "Analyzing repository")
        health.heartbeat("ATLAS", status="active")
        
        stats = gf.get_repo_stats()
        results["operations"].append({
            "op": "stats",
            "commits": stats['total_commits'],
            "files": stats['total_files']
        })
        replay.log_output(session_id, f"Stats: {stats}")
        
        # Operation 2: Commit log
        replay.log_input(session_id, "Getting commit log")
        commits = gf.get_commit_log(count=gf_config.get('log_count', 10))
        results["operations"].append({
            "op": "log",
            "count": len(commits)
        })
        
        # Operation 3: Branch cleanup
        replay.log_input(session_id, "Checking for cleanup")
        branches = gf.cleanup_branches(dry_run=True)
        results["operations"].append({
            "op": "cleanup_check",
            "branches_to_delete": len(branches)
        })
        
        # Operation 4: Changelog
        replay.log_input(session_id, "Generating changelog")
        changelog = gf.generate_changelog(since='7.days')
        results["operations"].append({
            "op": "changelog",
            "length": len(changelog)
        })
        
        # Save to memory
        results["end_time"] = datetime.now().isoformat()
        history = memory.get("workflow_history", [])
        history.append(results)
        memory.set("workflow_history", history[-50:])  # Keep last 50
        memory.sync()
        
        # Complete everything
        queue.complete_task(task_id, result=results)
        replay.end_session(session_id, status="COMPLETED")
        health.end_session("ATLAS", session_id=session_id, status="success")
        
        # Notify
        quick_send("TEAM", "Full Stack Workflow Complete",
            f"Operations completed:\n" +
            "\n".join([f"- {op['op']}" for op in results['operations']]))
        
        print("[OK] Full stack workflow complete")
        return results
        
    except Exception as e:
        queue.fail_task(task_id, error=str(e))
        replay.log_error(session_id, str(e))
        replay.end_session(session_id, status="FAILED")
        health.end_session("ATLAS", session_id=session_id, status="failed")
        quick_send("FORGE", "Workflow Failed", str(e), priority="HIGH")
        raise

if __name__ == "__main__":
    full_stack_workflow()
```

**Result:** Production-grade workflow with full observability

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. SynapseLink - Team notifications
2. AgentHealth - Health correlation
3. SessionReplay - Debugging

**Week 2 (Productivity):**
4. TaskQueuePro - Task management
5. MemoryBridge - Data persistence
6. ConfigManager - Configuration

**Week 3 (Advanced):**
7. ContextCompressor - Large output handling
8. CollabSession - Multi-agent coordination
9. Full stack integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

### Import Errors

```python
# Ensure all tools are in Python path
import sys
from pathlib import Path

base = Path("C:/Users/logan/OneDrive/Documents/AutoProjects")
for tool in ['GitFlow', 'SynapseLink', 'AgentHealth']:
    sys.path.append(str(base / tool))

# Then import
from gitflow import GitFlow
from synapselink import quick_send
from agenthealth import AgentHealth
```

### Git Not Found

```python
from gitflow import GitFlow
gf = GitFlow()
success, output = gf.run_git(['--version'])
if not success:
    print(f"Git error: {output}")
    # Install git or add to PATH
```

### Configuration Issues

```python
from configmanager import ConfigManager
config = ConfigManager()

# Check current config
print(config.get("gitflow"))

# Reset if needed
config.set("gitflow", {
    "auto_push": True,
    "log_count": 10
})
config.save()
```

---

**Last Updated:** January 24, 2026
**Maintained By:** Atlas (Team Brain)
