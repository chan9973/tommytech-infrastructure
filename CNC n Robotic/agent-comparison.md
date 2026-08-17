# AI Coding Agent Comparison: OpenCode vs Claude Code
**Vault:** `CNC n Robotic` | **Version:** 2026.08.v1  
---

## Quick Decision Matrix

| Use Case | Best Tool | Why |
|----------|-----------|-----|
| **One-shot tasks (CI/CD)** | Claude (`-p`) | No interactive overhead |
| **Multi-turn projects** | Claude (tmux) | Better context awareness |
| **Open-source/free agents** | OpenCode | Provider-agnostic, open-source TUI |
| **Parallel work streams** | Any (with worktrees) | Both support isolated git trees |
| **PR review automation** | Either | Both have dedicated PR commands |

---

## Core Architecture Comparison

### **Claude Code** (Anthropic's Agent CLI)
- **Provider:** Anthropic (`claude-sonnet`, `claude-opus`, etc.)  
- **License:** MIT  
- **Platform:** Linux/macOS/Windows CLI  
- **Key Feature:** Advanced reasoning with native multi-turn chat  
- **Max Context:** 200K tokens (model-dependent)  
- **Pricing:** Pay-per-token (~$3-15/K token depending on model)  

### **OpenCode** (anomalyco's Agent Platform)  
- **Provider:** Provider-agnostic (supports ANY LLM API: OpenRouter, Together, etc.)  
- **License:** MIT (open-source CLI + TUI)  
- **Platform:** Linux/macOS/Windows CLI with native TUI  
- **Key Feature:** Flexibility to switch providers/models on-the-fly  
- **Max Context:** 128K tokens (by design)  
- **Pricing:** Whatever your API provider charges  

---

## Installation Comparison

### Claude Code
```bash
npm install -g @anthropic-ai/claude-code

# Auth: run once to sign in (browser or API key)
claude

# Check status
claude auth status --text

# Update
claude update
```

### OpenCode
```bash
npm i -g opencode-ai@latest

# OR via Homebrew (macOS)
brew install anomalyco/tap/opencode

# Auth: configure providers
opencode auth login

# Verify providers
opencode auth list
```

---

## CLI Usage Side-by-Side

| Task | Claude Code | OpenCode |
|------|--------------|----------|
| **One-shot task** \| ```claude -p "task" --max-turns 10 --allowedTools "Read,Write,Bash"``` \| ```opencode run "task"` |
| **Interactive session** \| `tmux send-keys 'claude'` (via tmux) | `opencode` (native TUI) |
| **Resume last session** |\n\n```\nclaude -c  \nclaude --resume <session-id>``` |\n\n```\nopencode -c  \nopencode -s <session-id>\n``` |
| **PR review** |\n\n```\nclaude -p "Review PR #42" --from-pr 42``` |n\n```opencode pr 42``` |
| **Attach files** | `--file "id:relative_path"` | `-f file1.md -f file2.md` |
| **Specified model** | `--model opus` | `--model openrouter/anthropic/claude-sonnet-4` |
| **Thinking mode** | N/A (internal) | `--thinking` (show prompts in TUI) |

---

## Mode Comparison: Interactive Sessions

### **Claude Code (tmux-based)**
```bash
# Start session in detached tmux pane
tmux new-session -d -s claude-work

# Launch Claude
tmux send-keys -t claude-work 'claude' Enter

# Wait for welcome screen (~5s)
sleep 5

# Send first task
tmux send-keys -t claude-work "Refactor the auth module" Enter

# Monitor progress every 20s
while true; do
  echo "=== Progress ===" 
  tmux capture-pane -t claude-work -p -S -50
  sleep 20
done
```

### **OpenCode (native TUI)**
```bash
# One-shot task (runs and exits)
opencode run "task" --thinking

# Interactive session (starts TUI, runs in foreground)
opencode --title my-project

# Send a prompt (double-press Enter if needed)
Enter  # Submit message
Enter  # If text buffer needs finalization

# Monitor via poll (if running in background)
process(action="poll", session_id="<id>")
```

**Key difference:** OpenCode's TUI is native and doesn't require tmux for interactive work, while Claude Code REQUIRES tmux orchestration for multi-turn sessions.

---

## Tool Capabilities & Permissions

### **Shared Capabilities (Both Support):**
- ✨ Git operations (branching, commits, PRs)  
- 📄 File reading/writing  
- 🔧 Shell command execution  
- ✂️ Code refactoring suggestions  
- 🧪 Test generation and execution  

### **Claude Code Specific:**
- 🧠 Advanced reasoning modes (`/effort max`)  
- 💬 Rich markdown chats with memory compaction  
- 🎯 Precise permission flags (`--allowedTools`, `--permission-mode`)  
- 🔍 Context window monitoring (`/context` slash command)  

### **OpenCode Specific:**
- 🎨 Native TUI with visual feedback  
- 🔄 Provider switching mid-session (`--model`)  
- 💭 Thinking mode visibility (`--thinking`)  
- ⚙️ Variant reasoning control (`--variant high/minimal/max`)  

---

## Multi-Agent / Parallel Workflows

### **Claude Code**
```bash
# Start 3 parallel agents in separate worktrees
task1="tmux new-session -d -s refactor-auth"
task2="tmux new-session -d -s add-tests"  
task3="tmux new-session -d -s update-docs"

tmux send-keys -t $task1 "claude -p 'Refactor auth module'" --worktree feature-auth
tmux send-keys -t $task2 "claude -p 'Write test suite'" --worktree tests
tmux send-keys -t $task3 "claude -p 'Update documentation'" --worktree docs

# Monitor all panes periodically
sleep 30 && for s in refactor-auth add-tests update-docs; do
  tmux capture-pane -t $s
done
```

### **OpenCode**
```bash
# Parallel tasks with isolated workdirs
opencode run "Task 1" --worktree task1 --title "task-1" &
sleep 2 && opencode run "Task 2" --worktree task2 --title "task-2" &

# OR use separate background processes
terminal(command="opencode run 'Fix issue #1' --worktree /tmp/issue-1", background=true, pty=true)
terminal(command="opencode run 'Add tests' --worktree /tmp/issue-2", background=true, pty=true)

# Monitor with process tool
process(action="list")  # List all active OpenCode sessions
```

---

## Cost Comparison

### **Claude Code**
- **Pricing model:** Anthropic tokens  
- **Estimated costs (typical):**  
  - Sonnet 4: ~$3/K input, $15/K output  
  - Opus 4: ~$15/K input, $75/K output  
- **Per task cost (simple 10-turn review):** ~$0.05-0.15  

### **OpenCode**
- **Pricing model:** Provider-dependent  
- **Estimated costs (same task with OpenRouter):**  
  - Anthropic via OpenRouter: ~$2-3/K (slightly cheaper)  
  - Groq Llama: <$0.01/K (free tier + paid)  
- **Per task cost (Groq/Llama):** ~$0.005-0.02  

**Winner:** OpenCode wins for cost-sensitive users due to API arbitrage (use cheaper providers like Groq, Together AI).

---

## Best Practices & Patterns

### **When to Use Claude Code:**
✅ High-stakes production code requiring deep reasoning  
✅ Complex architectural decisions (`/effort max`)  
✅ Security-critical code reviews (`--allowedTools Read,Bash`)  
✅ When you need Anthropic's built-in safety guardrails  
✅ Multi-turn sessions where rich chat context matters  

### **When to Use OpenCode:**
✅ Cost-sensitive workloads (cheaper API providers)  
✅ Rapid prototyping (switch models as needed)  
✅ Open-source projects where transparency matters  
✅ You want native TUI without tmux overhead  
✅ Testing multiple LLMs before committing to one  

---

## Configuration Files

### **Claude Code: `.claude/settings.json`**
```json
{
  "permissions": {
    "allow": ["Read", "Write", "Bash(git *)"],
    "ask": ["Write(*.js)", "Bash(npm run lint:*)"],
    "deny": ["Read(.env)"]
  },
  "model": "sonnet",
  "effort": "high"
}
```

### **OpenCode: No config file needed**
Configuration is CLI-based (flags like `--model`, `--agent`, `--variant`). Provider settings handled via auth commands.

---

## Decision Flowchart

```
Start: Need AI coding agent
   
       │
       ├── One-shot, automated task?
       │     └──► Yes → Claude Code with --print mode
       │           (e.g., "audit codebase")
       │     
       ├── Cost is primary constraint?
       │     └──► Yes → OpenCode with Groq/provider arbitrage
       │     
       ├── Need native TUI (no tmux)?
       │     └──► Yes → OpenCode
       │     
       ├── Multi-turn, high-reasoning work?
       │     └──► Yes → Claude Code with --max-turns + effort=max
       │     
       └── Use either based on comfort/availability
```

---

## My Recommendation 🎯

### For Production Work (My Personal Workflow):
**Primary:** **Claude Code**  
- Better documentation and tool maturity
- Superior reasoning capabilities for complex tasks
- Excellent security permissions system
- More reliable in production environments

**Secondary:** **OpenCode**  
- Use for:
  - Rapid prototyping / experimentation
  - Cost-sensitive iterations
  - Testing different LLM providers
  - Non-critical code generation

### For Learning AI Coding Agents:
Try both! OpenCode is more forgiving for experimentation. Once you're comfortable, graduate tasks to Claude Code for production work.

---

## Future-Proofing Considerations

| Factor | Claude Code | OpenCode |
|--------|------------|----------|
| **Long-term viability** | Anthropic-backed → Stable | Open-source → Flexible |
| **Provider switching** | Fixed (Anthropic only) | Easy via flags |
| **API stability** | Dependent on Anthropic | Choose your provider |
| **TUI features** | Tmux-dependent | Native |

**Strategy:** Keep both installed. Use Claude for core work, OpenCode for experimentation and cost optimization periods.

---

## TL;DR Summary

- **Claude Code**: Premium feature set with better reasoning, requires tmux, Anthropic tokens only
- **OpenCode**: Open-source, native TUI, provider-agnostic, more flexible but less documented
- **My workflow**: Claude Code for production, OpenCode for experimenting/cost savings

---

*Vault Location: `CNC n Robotic/agent-comparison.md`*  
*Created: 2026.08.16*  
*Wikilinks: [[Claude Code]], [[OpenCode]]*
