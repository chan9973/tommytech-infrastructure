# CTO Infrastructure Reporting Pattern  
**Active Pattern Detected**: User said "follow up tommytech project as a cto" and "follow up tommytech project as a ceo" - indicating double role-switch pattern.

---

## 📋 Pattern Rules

1. **Role-Switch Context**: When "as [role]" is specified, generate output IN that role's voice
2. **Dual-Format Delivery**: Executive summary + technical details
3. **Immediate Action Bias**: Lead with what needs doing, not analysis
4. **File Output**: Store reports in Obsidian vault with timestamp

---

## 🎯 Current Application

**User Request**: "follow up tommytech project as a cto" → follow up tommytech project as a ceo

**Expected Response**:
- CTO report first (technical deep dive)
- CEO report second (executive summary)
- Action keywords at end

---

## 📝 Template Structure

```markdown
## CTOTasks
- [ ] Fix GitHub token scope
- [ ] Add Stripe integration
- [ ] Generate client reports
```

---

## 📂 File Locations

- Reports: `CTO_INFRA_STATUS.md` (technical)
- Executive: `CEO_INFRA_STATUS.md` (strategic)
- Decision Log: `cto_decisions.md` (running)

---

## ⚡ Action Keywords (Always Include)

1. **`token`** — Authentication/credentials
2. **`deploy`** — Release actions
3. **`stripe`** — Billing/payment
4. **`status`** — Health check

---

## 📎 References

- `references/tommytech-vault-path.md` — Windows vault location
- `references/action-keywords.md` — Standard action words
- `references/cto-blockers.md` — Common infrastructure blocks