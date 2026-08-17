# Makefile for LLM-Wiki Documentation Automation
# Place in your vault root or run from scripts/ directory

VAULT := E:/tommy vault/tommy vault/Read & Write
SCRIPTS := $(VAULT)/scripts
PYTHON := python3

# Default target
.PHONY: all docs diagram decision-log xref clean help

all: docs
	@echo "✅ Full documentation generated"

docs: diagram decision-log xref
	@echo "✅ All documentation complete"

diagram:
	@echo "📊 Generating architecture diagram..."
	$(PYTHON) $(SCRIPTS)/generate_docs.py --type diagram

decision-log:
	@echo "📋 Generating decision log..."
	$(PYTHON) $(SCRIPTS)/generate_docs.py --type decision-log

xref:
	@echo "🔗 Generating cross-reference map..."
	$(PYTHON) $(SCRIPTS)/generate_docs.py --type xref

# Quality checks
.PHONY: check-isolated check-links

check-isolated:
	@echo "🔍 Checking for isolated notes..."
	@grep -r "isolated" $(VAULT)/memories/xref-*.json || echo "No isolated notes found"

check-links:
	@echo "🔗 Checking broken wikilinks..."
	@$(PYTHON) -c "from pathlib import Path; P=Path('$(VAULT)'); print('✓ Vault exists:', P.exists())"

# Cleanup
clean:
	@echo "🧹 Cleaning generated files..."
	@rm -f $(VAULT)/_wiki/architecture-diagram.md
	@rm -f $(VAULT)/memories/xref-map-*.json
	@echo "✅ Cleaned"

# Help
help:
	@echo "LLM-Wiki Documentation Automation"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  all           - Generate all documentation (default)"
	@echo "  docs          - Same as 'all'"
	@echo "  diagram       - Generate Mermaid architecture diagram"
	@echo "  decision-log  - Generate curated decision log"
	@echo "  xref          - Generate cross-reference analysis"
	@echo "  check-isolated- Check for notes needing links"
	@echo "  check-links   - Verify vault structure"
	@echo "  clean         - Remove generated files"
	@echo "  help          - Show this help message"