# CTO Technical Decisions - TommyTech Infrastructure

## Initial Infrastructure Setup (2024-01-01)

### Decision 1: Git Repository Strategy
**Decision**: Single repository (`tommytech-infrastructure`) for all infrastructure code.

**Rationale**: Centralized repository reduces context switching and simplifies access control. All CI/CD, security configs, and vector store utilities are infrastructure-adjacent, not application code.

**Owner**: CTO

---

### Decision 2: PostgreSQL + DuckDB Hybrid Architecture
**Decision**: PostgreSQL for persistent vector embeddings; DuckDB for local analytics/testing.

**Rationale**: PostgreSQL provides ACID compliance, connection pooling, and shared infrastructure with application services. DuckDB enables zero-config local development with identical SQL dialect, supporting "schema on read" analytics without separate deployment.

**Owner**: Infrastructure Lead

---

### Decision 3: CI/CD Pipeline Configuration
**Decision**: GitHub Actions with four distinct jobs:
- **security-scan**: Bandit + Safety checks (runs on all PRs)
- **code-quality**: Black, flake8, mypy validation
- **database-tests**: PostgreSQL connectivity via testcontainer
- **vector-storage-test**: DuckDB integration tests

**Rationale**: Job dependency (`needs`) ensures fast failure of security checks without waiting for unit tests. Scheduled weekly scan catches drift in dependencies.

**Owner**: CTO

---

### Decision 4: Secret Management Strategy
**Decision**: GitHub Secrets pattern `${{ secrets.* }}` with no local `.env` files in repository.

**Rationale**: Eliminates credential leakage risk. Secrets rotate independently of code commits. Deployment keys reference single source of truth.

**Owner**: Infrastructure Lead

**Pending**: Implement `hermes secrets` CLI integration for automated quarterly rotation (ticket: INFRA-2024-Q1-07).

---

### Decision 5: Role-Based Access Control (RBAC)
**Decision**: Two roles defined in `.github/security-team.yml`:
- **cto**: Full infrastructure write access, deployment approval
- **infrastructure-lead**: PR review, security scan execution

**Rationale**: Minimal privilege principle. CTO retains architecture oversight; lead engineers execute routine operations without elevated permissions.

**Owner**: CTO

**Pending**: Add third-party security scanner integration (Snyk or Trivy) to pipeline (ticket: INFRA-2024-Q1-08).

---

### Decision 6: Vector Store Schema
**Decision**: Single `vector_embeddings` table with `embedding_vector DOUBLE PRECISION[]` for efficient similarity search.

**Rationale**: DuckDB's native array types provide sub-second indexing for small-to-medium collections (<100K embeddings). For larger scale, transition to pgvector or Pinecone recommended.

**Owner**: Infrastructure Lead

**Pending**: Implement cosine similarity query function for retrieval (ticket: INFRA-2024-Q1-09).

---

### Decision 7: Code Review Convention
**Decision**: All changes require CI passing + two independent approvals before merge.

**Rationale**: Prevents "merge drift" from single-author control. Two-approval rule ensures architecture intent remains consistent.

**Owner**: CTO

---

## Next Planning Cycle

- [ ] Implement security scan dashboard for weekly reporting
- [ ] Migrate FLUX vector embeddings to PostgreSQL `pgvector` extension for unified storage
- [ ] Add Terraform/Ansible provisioning scripts
- [ ] Establish incident response runbooks for database corruption scenarios
