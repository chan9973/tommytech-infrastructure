# Makefile for LLM-Wiki Documentation Automation
# Copy to vault root or call directly from scripts/

VAULT ?= "E:/tommy vault/tommy vault/Read & Write"
SCRIPTS ?= $(VAULT)/scripts
PYTHON ?= python3

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

check-isolated:
	@echo "🔍 Checking for isolated notes..."
	@pipenv run python -c "from hermes_tools import terminal; terminal('grep -l \"isolation_score.*1\" $(VAULT)/memories/xref-*.json 2>/dev/null || echo \"No isolated notes found\"')"

check-links:
	@echo "🔗 Checking wikilink health..."
	@$(PYTHON) -c "from pathlib import Path; p=Path('$(VAULT)'); print('✓ Vault exists:', p.exists())"

clean:
	@echo "🧹 Cleaning generated files..."
	@rm -f $(VAULT)/_wiki/architecture-diagram.md
	@rm -f $(VAULT)/memories/xref-map-*.json
	@echo "✅ Cleaned"

help:
	@echo "LLM-Wiki Documentation Automation"
	@echo ""
	@echo "Variables:"
	@echo "  VAULT    - Vault path (default: E:/tommy vault/...)";
	@echo "  SCRIPTS  - Scripts directory (default: VAULT/scripts)";
	@echo "  PYTHON   - Python executable (default: python3)"
	@echo ""
	@echo "Targets:"
	@echo "  all           - Generate all documentation (default)";
	@echo "  doc...        - Generate all documentation";
	@echo "  diagram       - Generate Mermaid architecture diagram";
	@echo "  decision-log  - Generate curated decision log";
	@echo "  xref          - Generate cross-reference analysis";
	@echo "  check-isolated- Check for notes needing links";
	@echo "  check-links   - Verify vault structure";
	@echo "  clean         - Remove generated files";
	@echo "  help          - Show this help message"