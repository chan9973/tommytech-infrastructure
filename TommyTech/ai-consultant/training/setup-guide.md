# Python Environment Setup Guide for Hermes AI Consultant 🐍
**Author**: Tommy Chan | **Created**: 2026-08-17 | **Status**: Ready to Use  

---

## ✅ Option A: Virtual Environment with Pip (RECOMMENDED — You Have Python 3.14!)

Your system already has:
- Python 3.14.7 installed (`python3` or `python3.14`)
- Python 3.11.15 via pip legacy install (`python3.11`)

### Step-by-Step Commands for `.venv` Environment

**1. Create Virtual Environment in Obsidian Vault:**
```bash
cd "E:/tommy vault/tommy vault/Read & Write/ai-consultant"
python3 -m venv .venv
```

**2. Activate Virtual Environment:**

_In Git Bash / MSYS:_
```bash
source .venv/bin/activate
# or: . .venv/bin/activate  (alias this line at end of ~/.bashrc for convenience)
```

_Or in PowerShell:_
```powershell
.\.venv\Scripts\Activate.ps1
```

_Or in Command Prompt:_
```cmd
.\.venv\Scripts\activate.bat
```

Once activated, prompt shows: `(venv) C:\...`

### Step 3: Upgrade Pip + Install Hermes Toolkit (if available) or Your Agents' Core Packages

```bash
pip install --upgrade pip setuptools wheel

# Install your main agent dependencies — use these initial packages for starters
pip install hermes-tools  # Official Hermes CLI (or equivalent package from GitHub)
pip install transformers torch sentencepiece accelerate peft trl bitsandbytes auto-gptq  
# For running models locally (Ollama uses its own runtime, but you can load models via Python APIs for customization)

# Install agent orchestration libraries  
pip install langchain langsmith vector_database  # Or LiteLLM if cross-provider agents needed

# Add utility tools:
pip install pandas requests playwright obsidian-mdx python-dateutil
```

**4. Verify Environment:**
```bash
python --version     # Should show Python 3.11+ (default venv picks newest in PATH with python3)
pip list             # Show all installed packages
hermes --help        # Or your agent's CLI name if you've cloned repo locally
```

**5. Save Dependencies for Future Reference:**
```bash
pip freeze > .venv/requirements.txt   # Keep this file synced with Git or local backup
```

---

## 📦 Option B: Conda Environment (Install Miniconda First — OPTIONAL)

If you want to use conda for heavy ML dependencies (CUDA, PyTorch), install miniconda:

**1. Download Miniconda:**
→ https://docs.conda.io/en/latest/miniconda.html (Select "Windows installer")

**2. Install during wizard:**
- Accept default install path (`C:/Users/.../miniconda3`)
- Put in PATH: Yes (check "Add to PATH")
- Anaconda Navigator: No (unless you want GUI tools)

**3. Create Hermes-specific Environment:**
```bash
conda create -n py311 python=3.11 pytorch torchvision torchaudio pytorch-cuda -c pytorch -c conda-forge -y
conda activate py311
pip install hermes-tools
```

> ⚠️ Miniconda installs ~600 MB to your hard drive. If you're just building agents without GPU training on-the-fly, pip-only environment is sufficient for now.

---

## 🧪 Quick Test: Your Hermes Workflow Script

Create `test_hermes.py` in `ai-consultant/`:

```python
"""Test script to validate Hermes tool or agent installation."""
import hermes_tools as ht  # or whatever your local repo exports

print("🎯 Hermes Environment Status Check:")
print(f"Python version: {ht.__version__}")  
try:
    print("\n✅ Running basic command demo:")
    result = ht.run_command("echo 'Hermes workflow running locally!'")
    print(result)
except ImportError as e:
    print(f"\n❌ Hermes not installed yet. Run: pip install hermes-tools")
```

Run test script (must be inside activated venv):
```bash
python test_hermes.py
```

---

## 📁 Project Folder Structure with `.venv` Included

Your AI consultant directory now looks like this:

```text
E:/tommy vault/tommy vault/Read & Write/ai-consultant/
├── .venv/                       ← Hidden virtual environment (created via pip)
│   ├── bin/                     # Windows activation scripts
│   └── python.exe               # Points to your venv's Python (usually 3.11+ default)
├── .requirements.txt            # Your locked package versions (generated after installs)
├── test_hermes.py              # Quick validation script above
├── client-templates/           # Case-study PDFs + agent config examples
│   ├── client-001/
│   │   ├── agent-config.yml
│   │   └── workflow-diagram.png
│   └── client-002/
│       └── ...
└── outreach/
    ├── scripts.md              # DM + LinkedIn pitch templates (as discussed earlier)
    └── contacts.csv            # Prospect tracking spreadsheet
```

---

## 🔒 Security & GDPR/PDPA Note for Remote Sessions

All environments run **locally** on client machines or yours (no cloud exfiltration). When using TeamViewer/AnyDesk sessions:

- **Never** install new packages via pip inside remote session without consent
- **Always** run `pip freeze` to show what's installed before installing agent dependencies during setup meetings
- **Export credentials carefully**: Keep `.env` files with API keys out of Git repo if sharing code
- For clients using your local models: Share only compiled workflow YAMLs + model paths, never raw context logs

---

## 🎯 Next Steps Checklist

[ ] Activate venv on your machine: `source .venv/bin/activate`
[ ] Run `pip install hermes-tools` (or equivalent package name from official guide)
[ ] Create test script at `ai-consultant/test_hermes.py`
[ ] Generate `.requirements.txt` via `pip freeze > .venv/requirements.txt`
[ ] Open in Obsidian and link to `playbook-formatted.md` for documentation
[ ] Export PDF version of both this guide + playbook for client handovers

---

## 💬 Questions / Adjustments?

- Want to pin specific Python version (3.12 vs 3.14)? Run: `.venv/bin/python --version` first
- Need CUDA GPU support? Install PyTorch with `-c pytorch-cuda=12.1` flag if you have NVIDIA cards  
- Using Ollama-only? Skip PyTorch—just install your agent orchestration libs (`langchain`, `litellm`)
