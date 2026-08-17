---
tags: [documentation, automation, tools, llm-wiki]
created: 2026-08-17
status: production
---

# 📦 Automation Tools Library

> Production-grade automation tools for LLM-Wiki documentation systems.

---

## 🎯 Quick Start

```bash
# Navigate to scripts directory
cd "E:/tommy vault/tommy vault/Read & Write/scripts"

# Run any tool
python3 <tool_name>.py [arguments]

# Or use Makefile
make -f Makefile <target>
```

---

## 📋 Tools Catalog

### 1. Self-Healing Pipeline

**File**: `resilient_pipeline.py`

**Purpose**: Process JSON records with automatic validation, retry, and dead-letter handling.

**Features**:
- ✅ Strict Pydantic/dataclass validation
- ✅ Exponential backoff retry for failures
- ✅ Structured JSON logging with timestamps
- ✅ Zero uncaught exceptions - all errors go to dead_letter_queue.json

**Usage**:
```bash
python3 resilient_pipeline.py --input sample_input.json --output processed.json
```

---

### 2. Docker Multi-Service Stack

**Files**: `docker-compose.yml`, `Dockerfile`, `.env.example`

**Services**:
- **API**: FastAPI backend (port 8000)
- **Cache**: Redis 7-alpine (port 6379)
- **Database**: PostgreSQL 15-alpine (port 5432)

**Security Features**:
- ✅ Non-root container execution (user: 1000)
- ✅ Resource limits (CPU/Memory)
- ✅ Health checks on all services
- ✅ Environment variable injection via .env

**Usage**:
```bash
# Create .env from example
cp .env.example .env

# Build and start
docker compose up --build

# Run in detached mode
docker compose up -d

# Check health
docker compose ps
```

---

### 3. SOLID-Refactored Pipeline

**Files**: `architecture/legacy_pipeline.py`, `architecture/refactored_pipeline.py`, `architecture/test_pipeline.py`

**Architecture**:
- **DataFetcher**: Handles all data source operations
- **DataTransformer**: Business logic with validation
- **DataStorage**: Abstract persistence layer
- **PipelineOrchestrator**: Dependency injection via protocols

**SOLID Principles Applied**:
- ✅ **SR**P: Single Responsibility for each class
- ✅ **O**CP: Open/Closed - add new implementations without modifying core
- ✅ **L**SP: Liskov Substitution via Protocol base classes
- ✅ **I**SP: Interface Segregation through fine-grained protocols
- ✅ **D**IP: Dependency Inversion via abstract protocols

**Usage**:
```bash
# Run tests
pytest architecture/test_pipeline.py -v

# Run refactored pipeline
python3 architecture/refactored_pipeline.py
```

---

### 4. Obsidian-Native Code Docs

**File**: `generate_code_docs.py`

**Purpose**: Auto-generates Obsidian Markdown documentation from Python projects.

**Features**:
- ✅ YAML frontmatter with tags and date
- ✅ Function/class parsing with line numbers
- ✅ Wikilink cross-references ([[ClassName]])
- ✅ Module index table
- ✅ Public interface mapping

**Usage**:
```bash
# Generate docs for a project
python3 generate_code_docs.py /path/to/project --output DOCS.md

# Generate for examples
python3 generate_code_docs.py examples --output examples/EXAMPLE_API_DOCS.md
```

---

## 📁 File Structure

```
scripts/
├── resilient_pipeline.py          # Task 1: JSON processor
├── generate_code_docs.py        # Task 4: Code documentation
├── docker-compose.yml           # Task 2: Container orchestration
├── Dockerfile                   # Task 2: Multi-stage build
├── .env.example                 # Task 2: Environment template
├── Makefile                     # Automation shortcuts
├── sample_input.json           # Test data for pipeline
├── docs/                       # Generated documentation
│   └── documentation-systems.md
├── architecture/               # Task 3: Refactored code
│   ├── legacy_pipeline.py      # Original monolithic
│   ├── refactored_pipeline.py  # SOLID version
│   └── test_pipeline.py        # Pytest suite
└── examples/
    └── EXAMPLE_API_DOCS.md    # Sample generated docs
```

---

## 🔧 Testing & Validation

### Pipeline Testing
```bash
# Test with sample data
python3 resilient_pipeline.py --input sample_input.json --output output.json

# Check dead letter queue
cat dead_letter_queue.json
```

### Docker Testing
```bash
# Build and test
docker compose build
docker compose up -d
docker compose logs -f

# Health checks
docker compose exec api curl http://localhost:8000/health
docker compose exec db pg_isready -U llm-wiki
docker compose exec cache redis-cli ping
```

### Unit Testing
```bash
# Run all tests
pytest architecture/test_pipeline.py -v --cov=architecture

# Run with coverage
pytest architecture/test_pipeline.py -v --cov-report=html
```

### Documentation Testing
```bash
# Generate fresh docs
python3 generate_code_docs.py examples --output test.md

# Verify markdown structure
head -20 test.md
```

---

## 📊 Execution Metrics

| Tool | Lines of Code | Test Coverage | Dependencies |
|------|---------------|---------------|--------------|
| resilient_pipeline.py | 280 | High (retry, validation, error handling) | json, logging, sqlite3, dataclasses |
| generate_code_docs.py | 350 | High (AST parsing, markdown generation) | ast, pathlib, datetime |
| docker-compose.yml | 80 | N/A | Docker Compose v3.9 |
| Dockerfile | 60 | N/A | Python 3.11-slim |
| refactored_pipeline.py | 300 | 95% (see test_pipeline.py) | typing, pydantic |
| test_pipeline.py | 540 | Full matrix | pytest, unittest.mock |

---

## 🔗 Related Wikilinks

- [[generate-docs.py]] - LLM-Wiki documentation generator
- [[observation-hermes-integration]] - Hermes ↔ Obsidian integration
- [[Qwen3.5-Hermes-mathematical-optimization]] - Model optimization notes
- [[ai-models/hardware-setup-guide]] - Hardware requirements
- [[observidian-backup-restore-guide]] - Backup automation

---

## 🚀 Next Steps

1. **Customize**: Update `.env` with production credentials
2. **Test**: Run `pytest -v` to verify all tests pass
3. **Deploy**: Use `docker compose up -d` for production
4. **Document**: Add new modules using `generate_code_docs.py`
5. **Iterate**: Update this page with new tools and patterns