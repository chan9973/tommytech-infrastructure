# TommyTech Infrastructure Repository

## 🏗️ Overview
Centralized Git repository for TommyTech's autonomous AI agent consulting service infrastructure.

## 📂 Structure
```
.
├── .github/workflows/ci.yml       # Automated deployment & testing
├── .bandit.yaml                  # Security scanning configuration
├── Dockerfile                    # Production containerization
├── docker-compose.prod.yml       # Production orchestration
└── README.md                     # This file
```

## 📋 Documentation

All client-facing documentation stored in Obsidian vault:

```
E:/tommy vault/tommy vault/Read & Write/TommyTech/
├── CLIENT_PIPELINE_DATABASE.md    # Main CRM database
├── pipeline_database.md             # Dataview queries
├── clients/                         # Individual client tracking
│   ├── jayaanona-logistics.md
│   ├── tokopedia-operations.md
│   └── ... (13 more)
├── tommytech-sdr-outreach.md        # Email/LinkedIn sequences
├── operations_dashboard.md          # Live ops status
├── agents/                          # Process documentation
│   ├── client_pipeline.md         # 6-phase onboarding process
│   ├── research_lead_profile.md
│   ├── csm_profile.md
│   └── billing_ops.md
└── linkedin-outreach.csv            # Raw prospect data
```

## 📊 Sales Pipeline Status

| Phase | Status | Target |
|-------|--------|--------|
| Outreach Preparation | ✅ Complete | 15 targets identified |
| LinkedIn Connection | ⏳ Ready | Today |
| Email Sequences | ✅ Built | 3 templates |
| Discovery Calls | ⏳ Pending | Week 2 |
| Pilot Onboarding | ⏳ Available | Week 3+ |

**Q4 Goal: 3 Jakarta pilots → $4,500/mo MRR**

---

## 🚀 Quick Start

```bash
git clone https://github.com/tommy-tech/tommytech-infrastructure.git
cd tommytech-infrastructure
docker-compose -f docker-compose.prod.yml up -d
```

## 🔐 Security & Compliance
- Bandit scanning enabled via `.bandit.yaml`
- Automated vulnerability checks in CI pipeline
- All infrastructure logs immutable (DuckDB-backed)

## 📋 Deployments
| Environment | Status | Notes |
|-------------|--------|-------|
| Dev (Local) | ✅ Active | Ollama + browser-use + local Docker |
| GitHub Actions | 🔄 Queue | Waiting for token auth |
| Production | ⏸️ Pending | Requires GitHub token + Stripe integration |

---
*Maintained by: TommyTech CEO Agent*  
*Last Updated: 19 August 2026*