# TommyTech Infrastructure

## Overview

Centralized infrastructure repository for TommyTech's technical foundation, including CI/CD pipelines, security configurations, and vector storage utilities.

## Architecture

- **PostgreSQL**: Persistent vector embeddings storage (production-grade, ACID compliant)
- **DuckDB**: Local analytics and testing layer (zero-config, SQL-fluent)
- **GitHub Actions**: Automated security scanning, code quality, and deployment

## Quick Start

```bash
# Install dependencies
pip install -e ".[dev, database, analytics]"

# Verify connectivity
python -c "from database import InfrastructureClient; print('Connected')"

# Run tests
pytest tests/
```

## Security

- Bandit scans on every PR
- Weekly scheduled vulnerability assessment
- Secrets managed via GitHub Secrets (no `.env` files in repo)

## Roles

| Role | Permissions |
|------|-------------|
| CTO | Full infrastructure write, deployment approval |
| Infrastructure Lead | PR review, security scan execution |

## Documents

- [cto_decisions.md](./cto_decisions.md) — Key architectural decisions
- [SECURITY-POlicy.md](./SECURITY-POlicy.md) — Security baseline and incident response
