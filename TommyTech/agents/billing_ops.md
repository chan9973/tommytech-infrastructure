# TommyTech — Finance Operations Framework
**Version:** 2.0 — Updated for Autonomous AI Setup Service  
**Owner:** Finance Agent | Review Cycle: Monthly

## 1. Agent Cost Modeling Ledger

| Resource | Unit Cost (USD) | Est. Usage/Month | Monthly Budget |
|----------|-----------------|------------------|----------------|
| Model Token Generation (Claude+Qwen+Ollama local) | $0.80–$2.50/1M tokens | 12–18M tokens | $10–$45 |
| Browser Automation (browser-use) | $1.20 per 500 ops | 2–3k ops | $5–$6 |
| API Calls (GitHub CLI, Notion, email tools) | $0.10–$1.00 per 1k calls | 500–1k calls | $0.50–$1 |
| Cloud Storage (DuckDB vectors, Notion, GitHub) | $5–$15/month (local disk = $0) | — | $5–$15 |
| **Total Estimated Run Rate** | | | **$26–$67/month** |

### Notes
- Local Ollama deployment → near-zero compute cost
- Hermetic caching → 20–30% token reduction
- Batch agent reads/writes → optimize peak token consumption

## 2. Client Billing Models & Tiering

### A. Tier-Structured Pricing

| Tier | Target Market | Price Range | Deliverables | Payment Terms |
|------|---------------|-------------|--------------|---------------|
| **Personal** | Home lab, hobbyists | $500 one-time | 1 agent, basic setup, 7-day support | 50% upfront |
| **Business** | SMEs (10–500 employees) | $1,500 one-time | 3-agent cluster, full vault, 14-day support | 50% upfront |
| **Enterprise** | Mid-market + | $3,000 one-time | 5+ agents, custom workflows, 30-day support | 50% upfront |

### B. Engagement Pricing (Per-Event)

| Engagement | Duration | Price Range | Usage Notes |
|------------|----------|-------------|-------------|
| Agent Architecture Audit | 3–6 weeks | $25k–$120k | Pre-salvage analysis; pure scoping |
| Framework Playbook License | 3–7 days | $15k setup + $40k/year | Vertical domain expertise |
| Build-Then-Build-Out MVP | 4–6 weeks | $60k–$180k | Pilot cluster; Phase 2 upsell |
| Governance & Safety Layer | 2–4 weeks | $20k–$85k | Adds 15–20% margin to any build |
| Staffed Ops Retainer | Ongoing | $7.5k–$30k/mo | 24/7 monitoring, training, patching |

### C. Add-Ons & Professional Services

| Add-On | Price | Trigger |
|--------|-------|---------|
| Emergency Agent Rescue | $15k per rescue | Agent drift, stalled pipelines |
| Security Penetration Test | $40k per engagement | AI/Agents security audit |
| Board-Ready Reporting Package | $10k per quarter | Executive dashboards |
| Monthly Monitoring Retainer | $500/mo | Ongoing agent health |
| Custom Agent Development | $5k per agent | Per client-specific agent |

## 3. Invoicing & Collection Protocols

- **Billing Cycle**: One-time for setup; monthly for retainers
- **Invoice Terms**: Net 15 for setup; Net 30 for retainers
- **Late Policy**: 1.5% monthly interest; services paused after 14 days past due
- **Pre-Billing Milestones**: No work beyond scope without milestone approval

### Automations
- **SmartInvoicing**: Notion + Zapier auto-generates invoices from milestone completion
- **Stripe/PayPal**: Upfront deposits; auto-recurring billing for retainers

## 4. ROI Audit Framework

### Agent Cost Efficiency Metrics

| Metric | Calculation | Target Band | Tracking |
|--------|-------------|-------------|----------|
| Cost per Decision | (Agent ops + tool calls + compute) / decisions | $0.50–$5.00 | Real-time dashboard |
| FTE Equivalency | (Agent ops hrs / 2000h) × avg-salary | 1 agent ≈ 3–5 FTE | Monthly audit |
| Latency-to-Action | Prompt → verified output | <15 min (pilot) | Daily |
| Agent Downtime % | Downtime / total × 100 | <3% target | Real-time |
| Token Utilization | (Actual / estimated) × 100 | 80–100% | Monthly review |

### Client ROI Proof Package (Quarterly)
1. **Financial Impact**: FTE hours saved, operational savings
2. **Risk Metrics**: Drift incidents, safety flags, compliance audits
3. **Cost Breakdown**: Transparent ledger by agent cluster
4. **Forecast**: Next quarter's projection + cost-benefit model

## 5. Compliance & Audit Controls (Minimal Viable)
- All agent interactions logged to timestamped audit trail
- Security checks: weekly automated code scan + monthly penetration test
- Data privacy: encrypted storage; PII masking in agent context windows
- Financial audit trail: immutable ledger for all model/tool/API calls

## 6. Performance Benchmarks vs. Market

| Dimension | TommyTech Target | Industry Mean | Advantage Source |
|-----------|------------------|---------------|------------------|
| Cost per Decision | $0.50–$5.00 | $15–$100 | Local model + batching |
| Response Latency | <15 min | 30–60 min | Zero-latency Ollama + cache |
| Compliance Readiness | Built-in | External audit | Embedded safety prompts |
| Staffed Ops Scaling | <$30k/mo | $100k+ | Automated monitoring + LLM triage |

---

*Version: 2.0 — Last updated: 19 August 2026*  
*Owner: Finance Agent | Review Cycle: Monthly*
