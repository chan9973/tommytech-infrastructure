# CTO Infrastructure Status Report Pattern

**Signal**: User wants me to "follow up [project] as [role]" - act AS the role character, not just report ON them.

## When to Use This Skill

Trigger phrases:
- "Follow up [project] as CTO"
- "Update me as the CEO on..."
- "Act as the [role] and report status"
- "[Role] perspective on..."

## Output Pattern

### Executive Summary (First)
- 3-5 bullet points, max
- Status emoji markers (✅ ⚠️ ⏸️ ⚪ ❌)
- Immediate/next actions
- Budget impact

### Technical Deep Dive (As requested or by default)
- Code blocks with ready commands
- File locations (Obsidian vault paths)
- Tool-specific commands

### End with Action Keywords
List 2-4 options with keywords:
1. **`action1`** — brief description
2. **`action2`** — brief description

Let CEO pick one.

## User Preference Reminders

From session patterns:
- **Concise**: Skip process explanations, give direct results
- **Action-first**: Lead with what NEEDS to be done
- **Emoji markers**: Quick status scanning
- **Dual delivery**: File + chat summary

## Template

```markdown
## Status Snapshot
- Repo: ✅ Active at `user/project`
- CI/CD: ⚠️ Blocked (token scope)
- Budget: $0 until deploy
- Next action: `refresh_token` → `stripe_key` → `deploy`

## Technical Details
<details>
<summary>Infrastructure files</summary>

### Files
- `repo/.github/workflows/ci.yml` - CI config
- `repo/docker-compose.prod.yml` - Production stack
- `README.md` - Quick start guide

### Commands
```bash
gh auth refresh -s admin:repo,workflow
```
</details>

---

**CEO Options:**
1. **`token`** — Refresh GitHub auth
2. **`stripe`** — Add billing credentials  
3. **`deploy`** — Launch production once above done
```