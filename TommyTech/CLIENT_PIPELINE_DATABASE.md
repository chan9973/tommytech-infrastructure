# 📋 Tommatech Client Pipeline Tracker Database

**Sales Manager:** Tommy Chan  
**Created:** 19 August 2026  
**Target:** 15 APAC SMEs • Jakarta focus • Q4 Pilot Program

---

## 🎯 Overview

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Outreach Complete | 15 | 0 | ⏳ Ready |
| Response Rate | 40% | - | Pending |
| Qualified Leads | 5 | 0 | Pending |
| Pilots Closed | 3 | 0 | Pending |
| Monthly Revenue | $4,500 | $0 | Pending |

---

## 📊 Client Pipeline Table

| # | Company | Contact | Role | Location | Pain Point | Template | Channel | Status | Email |
|---|---------|---------|------|----------|------------|----------|---------|--------|-------|
| 1 | JayaAnona Logistics | Rizky Pradana | Operations Head | Jakarta | Manual route planning & vendor sync | Template_1_JakartaSME | LinkedIn | ⏳ Prospecting | rizky.pradana@jayaanona.com |
| 2 | Tokopedia Operations | Arifin Setiawan | CTO | Jakarta | Seller onboarding 6+ weeks | Template_3_Growth | LinkedIn | ⏳ Prospecting | a.setiawan@tokopedia.com |
| 3 | Blibli Retail | Siti Rahayu | Supply Chain Lead | Jakarta | Inventory reconciliation errors 40% monthly | Template_1_JakartaSME | LinkedIn | ⏳ Prospecting | s.rahayu@blibli.com |
| 4 | Grab Financial Services | Lee Wei | Director | Singapore | Compliance reporting lag 3 days | Template_2_Compliance | LinkedIn | ⏳ Prospecting | w.lee@grab.com |
| 5 | SeaMoney Operations | Chua Kevin | Fintech Lead | Singapore | Customer support overload | Template_3_Growth | LinkedIn | ⏳ Prospecting | kevin.chua@sea.com |
| 6 | Shopee Mart Ops | Tan Ming Heng | Support Director | Singapore | Customer support bottlenecks | Template_3_Growth | LinkedIn | ⏳ Prospecting | m.tan@shopee.com |
| 7 | LinkAja | Wong Jia Heng | VP Payments | Jakarta | Fraud detection latency 45s | Template_2_Compliance | LinkedIn | ⏳ Prospecting | j.heng@linkaja.id |
| 8 | Bukalapak Retail | Dian Permata | GM Operations | Jakarta | Vendor sync failures weekly | Template_1_JakartaSME | LinkedIn | ⏳ Prospecting | d.permata@bukalapak.com |
| 9 | Gojek Support | Ong Wei Leong | Operations Manager | Jakarta | Tier-1 query overload | Template_3_Growth | LinkedIn | ⏳ Prospecting | w.leong@gojek.com |
| 10 | Traveloka Ops | Lim Chen Hau | Engineering Lead | Singapore | Dynamic pricing lag 2h | Template_3_Growth | LinkedIn | ⏳ Prospecting | chen.hou@traveloka.com |
| 11 | Axiata Digital | Michelle Tan | Head R&D | Singapore | Crypto compliance queries complex | Template_2_Compliance | LinkedIn | ⏳ Prospecting | m.tan@axiata.com |
| 12 | Razer Fintech | Bobby Santoso | CMO | Singapore | Compliance training new staff | Template_1_JakartaSME | LinkedIn | ⏳ Prospecting | b.santoso@razer.com |
| 13 | Bersama Payments | Farah Nasya | Process Lead | Jakarta | SME merchant onboarding 3w | Template_3_Growth | LinkedIn | ⏳ Prospecting | f.nasya@bersama.id |
| 14 | Zoje Tech | Nurul Hidayat | Head IT | Singapore | Agent drift incidents monthly | Template_2_Compliance | LinkedIn | ⏳ Prospecting | n.hidayat@zoje.com |
| 15 | Sea Limited | Kenji Yamamoto | Service Director | Singapore | Marketplace coordination sync | Template_1_JakartaSME | LinkedIn | ⏳ Prospecting | kenji.yamamoto@sea.com |

---

## 🎨 Color-Coded Pipeline View

### 🔴 Jakarta Priority (7 firms)
**Target: $1.5k/mo pilots → 3 wins = $4,500/mo**

1. **JayaAnona Logistics** - Manual route planning
   - Value: 3-agent cluster @ $1.5k/mo
   - Pitch: "Cut inventory errors by 73%"
   - Contact: Operations Head, direct email

2. **Tokopedia Operations** - Seller onboarding bottleneck
   - Value: Framework playbook, 1-week cut
   - Pitch: "3-day onboarding vs 6+ weeks"
   - Contact: CTO, technical decision maker

3. **BLIBLI Retail** - Inventory reconciliation errors
   - Value: Auto-reconciliation cluster
   - Pitch: "40% error reduction, $10k/week saved"
   - Contact: Supply Chain Lead

4. **Bukalapak Retail** - Vendor sync failures
   - Value: Integration audit
   - Pitch: "Weekly $10k savings"
   - Contact: GM Operations

5. **LinkAja** - Fraud detection latency
   - Value: Real-time audit trail
   - Pitch: "45s→<5s response time"
   - Contact: VP Payments

6. **Gojek Support** - Tier-1 query overload
   - Value: Chatbot agent cluster
   - Pitch: "70% automation, 60% Tier-1"
   - Contact: Operations Manager

7. **Bersama Payments** - Merchant onboarding 3w
   - Value: White-label framework
   - Pitch: "3 days onboarding"
   - Contact: Process Lead

### 🟡 Singapore Premium (8 firms)
**Target: $7.5k/mo standard tier**

1. **Grab Financial Services** - Compliance reporting
   - Value: SOC2-aligned retainer
   - Pitch: "Compliance layer automation"

2. **SeaMoney Operations** - Support overload
   - Value: 3-agent tier system
   - Pitch: "10k tickets/day capacity"

3. **Shopee Mart Ops** - Support bottlenecks
   - Value: Multi-agent support
   - Pitch: "Staffed ops at $7.5k/mo"

4. **Traveloka Ops** - Dynamic pricing lag
   - Value: Real-time agent loop
   - Pitch: "Sub-minute sync vs 2h"

5. **Axiata Digital** - Crypto compliance
   - Value: GDPR-ready ops layer
   - Pitch: "85% query automation"

6. **Razer Fintech** - Compliance training
   - Value: Training layer
   - Pitch: "5 days vs 4 weeks certification"

7. **Zoje Tech** - Agent drift incidents
   - Value: Safety layer
   - Pitch: "95% incident catch rate"

8. **Sea Limited** - Marketplace coordination
   - Value: 4-agent orchestration
   - Pitch: "99.8% sync maintenance"

---

## 📈 Success Metrics Dashboard

```dataview
TABLE 
length(filter(rows, (r) => contains(r.status, "⏳"))) as "Pending",
length(filter(rows, (r) => contains(r.status, "✅"))) as "Closed Won",
length(filter(rows, (r) => contains(r.status, "❌"))) as "Closed Lost",
sum(filter(rows, (r) => contains(r.status, "✅"), (r) => r.value)) as "MRR"
FROM "TommyTech/clients"
WHERE type = "client"
```

---

## 🚀 Weekly Execution Plan

### Week 1 (Aug 24)
- [ ] **Monday**: Send all 15 LinkedIn connection requests
- [ ] **Tuesday**: Send Day 1 email sequence to Jakarta targets
- [ ] **Wednesday**: Send Day 1 emails to Singapore targets
- [ ] **Thursday-Friday**: Monitor responses, engage comments
- [ ] **Saturday**: Follow up with non-responders

### Week 2 (Aug 31)
- [ ] **Discovery calls**: Book with 5 qualified leads
- [ ] **Workshop prep**: Customize requirements docs
- [ ] **Proposal drafts**: Create for pilot-ready prospects

---

## 🛠️ Templates & Resources

| Resource | Location | Purpose |
|----------|----------|---------|
| Email Sequences | [[tommytech-sdr-outreach]] | 3-step follow-up templates |
| LinkedIn Messages | [[tommytech-sdr-outreach]] | Messaging variations |
| Pipeline Process | [[agents/client_pipeline]] | 6-phase onboarding |
| Operations Dashboard | [[operations_dashboard]] | Company status |
| Raw Data | [[linkedin-outreach.csv]] | Original outreach list |

---

## 📎 Related Files

- `linkedin-outreach.csv` - Raw prospect data
- `tommytech-sdr-outreach.md` - Outreach templates
- `operations_dashboard.md` - Live dashboard
- `agents/client_pipeline.md` - Process guide
- `pipeline_database.md` - Dataview queries