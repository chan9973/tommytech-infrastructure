# Makefile for LLM-Wiki Documentation Automation
# Usage: make <target>

VAULT := "E:/tommy vault/tommy vault/Read & Write"
SCRIPTS := $(VAULT)/scripts

.PHONY: all docs diagram decision-log xref optimize analyze help

all: docs

docs: diagram decision-log xref

# Generate architecture diagram
diagram:
	@echo "📊 Generating architecture diagram..."
	python3 $(SCRIPTS)/generate_docs.py --type diagram
	@echo "✅ Diagram generated"

# Generate decision log
decision-log:
	@echo "📝 Generating decision log..."
	python3 $(SCRIPTS)/generate_docs.py --type decision-log
	@echo "✅ Decision log generated"

# Generate cross-reference map
xref:
	@echo "🔗 Generating cross-reference map..."
	python3 $(SCRIPTS)/generate_docs.py --type xref
	@echo "✅ XRef map generated"

# Run vault optimization analysis
optimize:
	@echo "🔍 Running vault optimization..."
	python3 $(SCRIPTS)/optimize_vault.py --report
	@echo "✅ Optimization complete"

# Full analysis: docs + optimization
analyze: optimize
	@echo "📈 Full analysis complete"

# Quick update of master index
update-index:
	@echo "📚 Updating knowledge tree..."
	python3 -c "from generate_docs import WikiGraph; import json; g=WikiGraph('$(VAULT)'); print(json.dumps(g.nodes.keys(), indent=2))" | head -20
	@echo "✅ Index snapshot taken"

help:
	@echo "LLM-Wiki Documentation Automation"
	@echo ""
	@echo "Available targets:"
	@echo "  make docs       - Generate all documentation"
	@echo "  make diagram    - Architecture diagram (Mermaid)"
	@echo "  make decision-log  - Decision log from active docs"
	@echo "  make xref       - Cross-reference analysis map"
	@echo "  make optimize   - Run vault quality optimization"
	@echo "  make analyze    - Full analysis (docs + optimize)"
	@echo "  make update-index - Quick vault index update"
	@echo "  make help       - Show this help"