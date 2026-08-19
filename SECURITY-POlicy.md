# TommyTech Infrastructure Security Policy

## Purpose

This document establishes the security baseline for TommyTech's technical infrastructure, including the GitHub repository, CI/CD pipelines, vector storage, and PostgreSQL+DuckDB backend.

## Security Controls

### 1. Repository Configuration

- **Branch Protection**: `main` and `develop` branches require PR approvals and passing CI/CD before merge
- **Secrets Management**: All database credentials, API keys are stored in GitHub Secrets and referenced via `${{ secrets.* }}` pattern
- **Code Review**: All code changes require review by CTO or Infrastructure Lead

### 2. CI/CD Security

- **Bandit Scans**: Continuous integration runs `bandit` security scanning on every PR
- **Safety Checks**: Dependency vulnerability scanning (`safety check`)
- **Scheduled Scans**: Weekly vulnerability assessment (Monday at 3AM UTC)

### 3. Database Security (PostgreSQL + DuckDB)

- **Connection Pooling**: SQLAlchemy with `pool_pre_ping=True` prevents stale connections
- **Schema Separation**: DuckDB vector store isolated in dedicated file (`vector_store.duckdb`)
- **Read-Write Separation**: Use `get_vector_store_schema()` for reads, `upsert_` functions for writes

### 4. Secret Rotation

**Schedule**: Quarterly

**Process**:
1. Generate new secrets in GitHub Secrets UI
2. Update deployment key references
3. Commit updated configuration (not old values)
4. Trigger pipeline to verify connectivity

### 5. Vector Storage Security

- **Encryption at Rest**: DuckDB file stored in encrypted workspace directory
- **Access Control**: Repository-level permissions only grant read to `infrastructure-lead` role
- **Data Integrity**: SQLAlchemy pool pre-ping validates connection health before query execution

## Incident Response

### Severity Classification

| Level | Definition | Response Time |
|-------|------------|---------------|
| CRITICAL | Production outage, data corruption | Immediate |
| HIGH | Security vulnerability, blocked deployment | < 2 hours |
| MEDIUM | CI/CD failure, non-critical bug | < 24 hours |
| LOW | Documentation, improvement suggestion | < 1 week |

### Escalation Path

1. **Lead Engineer** - Initial point of contact
2. **CTO** - Security and architecture decisions
3. **External** - Vendor support (DuckDB, PostgreSQL, GitHub)

## Compliance Note

This policy aligns with FAIR standards for infrastructure data storage and auditability.
