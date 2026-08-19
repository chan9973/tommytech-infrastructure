# TommyTech — Client Pipeline Management

## 1. Onboarding Pipeline (6 Phases)

| Phase | Owner | Inputs | Outputs | Criteria | Duration |
|-------|-------|--------|---------|----------|----------|
| **1. Pre-Onboard** | CEO + CSM | Request → RFP → NDA | Pre-Intake Brief | Topic validated; scope acceptable | 1–2 days |
| **2. Kickoff / Intake** | CSM | NDA signed; stakeholder IDs | Stakeholder Map + Use Case Brief | All decision-makers present | 48–72h |
| **3. Requirements Workshop** | Lead Agent + CSM | Intake brief; KPIs | Requirements Document (MoSCoW) | Must state KPIs, constraints, timelines | 90–120 min |
| **4. Setup & Integration** | CTO + Lead Agent | Requirements doc; environment | Metrics Tracker + Risk Register | API hooks wired; data flows confirmed | 2–5 days |
| **5. Training & UAT** | Lead Agent | Integration baseline | 30/60/90 Plan + Retrospective | Stakeholders can execute independently | 2–3 days |
| **6. Go-Live & Handoff** | CEO + CSM | Sign-off on all docs | Launch Notification | All gates passed; support path active | <24h |

## 2. Client Intake Protocol

**48h Kickoff Trigger:**
- Call slots reserved as non-negotiable
- Meeting deck pre-distributed via client portal

**Agenda (7 Blocks):**
1. Executive Vision Statement (CEO present, 5 min)
2. Scope of Work & Objectives (client lead, 10 min)
3. Constraints & Risk Appetite (client/CEO, 10 min)
4. Data Availability & Integrations (CTO, 10 min)
5. Timeline & Release Expectations (client, 15 min)
6. Communication Protocols & Escalations (CSM, 10 min)
7. Sign-Off & Next Steps (CEO, 5 min)

**Same-Day Deliverables (Required for Pipeline Gate):**
- Stakeholder Map (roles/delays/escalations)
- Use Case Brief (3–5 outcomes prioritized)
- Intake Summary (draft scope + suggested onboarding plan)

## 3. Requirements Gathering Blueprint

**90min Workshop Format:**
- Facilitated by Lead Agent; notes streamed to CSM
- MoSCoW scoring applied live (Must/Should/Could/Won't)

**Core Output (Requirements Document):**
1. Outcome Definitions + Success Metrics
2. Scope Boundaries + Explicit Exclusions
3. Data & Integration Inventory
4. People & Process Mapping

**Governance Rules:**
- Never invent: cite exact source (speaker, doc, record)
- One KPI per outcome; never aggregate metrics
- No open-ended deliverables unless scoped in appendix
- All decisions must be explicitly recorded in Risk Register

## 4. Communication Protocols & SLAs

| Channel | Purpose | Response SLA | Escalation Flag | Owner |
|---------|---------|--------------|-----------------|-------|
| Slack | Daily ops + quick decisions | ≤30 min | 🔴 → 15 min reply | CSM |
| Email | Client updates + requests | ≤4h business | 🟠 → 1h reply | CSM |
| GitHub | Tech decisions + PRs | ≤12h | 🟡 → 6h review | CTO |
| Notion/HubSpot | CRM + milestone tracking | N/A | — | CSM + Lead Agent |

**Meeting Cadence:**
- Daily Standup: 15 min, CSM–Lead Agents
- Weekly Steering: 45 min, CEO + Key Agents + Client
- Monthly Business Review: 90 min, CEO + Client Executive (QBR)

**3-Level Escalation Path:**
1. **Level 1 (CSM):** Document in Slack; notify client via email
2. **Level 2 (CEO):** Direct Slack message + calendar emergency; Slack message: `@channel 🔴 BLOCKER`
3. **Level 3 (Executive):** Direct hotline or email with explicit SLA expectation

## 5. Action Item Management

**Rules:**
- Single owner per action; never multiple assignees
- Never invent steps: derive from documented requirements
- Tracking via Notion or Zapier → links to Requirements Doc
- Zero open items allowed at Go-Live gate

**Standard Action-Item Template:**
```markdown
- [ ] ID-001: Owner | Deadline | Status | Source
- [x] ID-002: Owner | Deadline | Status | Source (✓ verified)
```

**Skill References:**
- Source procedure: `meeting-action-items` skill (loaded for audit compliance)