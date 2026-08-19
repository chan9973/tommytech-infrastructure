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