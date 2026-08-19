# 📋 Client Pipeline - Individual Tracking

## 🎯 TommyTech Client Pipeline Database

> Created: 19 August 2026  
> Sales Manager: Tommy Chan  
> Target: 15 APAC SMEs for Q4 Pilot Program

---

## 📊 Pipeline Status Table

| Company | Contact | Role | Location | Status | Value | Next Action |
|---------|---------|------|----------|--------|-------|-------------|
| JayaAnona Logistics | Rizky Pradana | Operations Head | Jakarta | ⏳ Prospecting | $1,500/mo | Connect via LinkedIn |
| Tokopedia Operations | Arifin Setiawan | CTO | Jakarta | ⏳ Prospecting | $1,500/mo | Connect via LinkedIn |
| Blibli Retail | Siti Rahayu | Supply Chain Lead | Jakarta | ⏳ Prospecting | $1,500/mo | Connect via LinkedIn |

---

## 🚦 Stage Filters (Dataview)

### Contacted This Week
```dataview
TABLE outreach_date, status, next_action
FROM "TommyTech"
WHERE outreach_date >= date(today) - dur(7 days)
SORT outreach_date DESC
```

### High Priority (Jakarta SMEs)
```dataview
TABLE company, contact, pain_point, template_used as "Template"
FROM "TommyTech"
WHERE location = "Jakarta"
SORT company ASC
```

---

## 📈 Pipeline Summary (Dataview)

```dataview
TABLE length(filter(rows, (r) => r.status = "Prospecting")) as "Prospecting",
       length(filter(rows, (r) => r.status = "Contacted")) as "Contacted",
       length(filter(rows, (r) => r.status = "Qualified")) as "Qualified",
       length(filter(rows, (r) => r.status = "Proposal Sent")) as "Proposal",
       sum(filter(rows, (r) => r.status = "Closed Won", (r) => r.value)) as "Won Revenue"
FROM "TommyTech"
FLATTEN company as company
WHERE contains(file.name, company)
```

---

## 🗓️ Weekly Action Plan

### Week 1 (Aug 24-30)
- [ ] **LinkedIn Outreach Day 1**: Send 15 connection requests
- [ ] **Email Sequence Day 1**: Follow up with Template 1
- [ ] **Engagement Monitoring**: Track responses and profile visits

### Week 2 (Aug 31 - Sep 6)  
- [ ] **Discovery Calls**: Schedule with warm leads
- [ ] **Workshop Prep**: Customize requirements doc
- [ ] **Email Day 3**: Send compliance/growth templates

### Week 3 (Sep 7-13)
- [ ] **Pilot Negotiations**: Finalize terms
- [ ] **Document Signing**: Get NDA and agreements
- [ ] **Onboarding Kickoff**: Schedule Phase 1

---

## 📎 Reference Documents

- [[client_pipeline_tracking]] - Main tracking page
- [[TommyTech/tommytech-sdr-outreach]] - Email/LinkedIn templates
- [[TommyTech/operations_dashboard]] - Live ops status
- [[TommyTech/agents/client_pipeline]] - Process documentation

---

## 🚀 Quick Actions

```dataviewjs
dv.container.innerHTML = `
<div style="display: flex; gap: 10px; flex-wrap: wrap;">
  <a href="https://www.linkedin.com" target="_blank" style="padding: 8px 16px; background: #0077b5; color: white; border-radius: 4px; text-decoration: none;">📧 LinkedIn Outreach</a>
  <a href="mailto:" style="padding: 8px 16px; background: #ea4335; color: white; border-radius: 4px; text-decoration: none;">📧 Send Emails</a>
  <a href="#" style="padding: 8px 16px; background: #34a853; color: white; border-radius: 4px; text-decoration: none;">📊 Update Pipeline</a>
</div>
`
```