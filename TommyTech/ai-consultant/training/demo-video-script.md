# 🎥 AI Setup Consultant — Demo Video Script v1.0  
**Author**: Tommy Chan | **Created**: 2026-08-17 | **Status**: Production Ready  

---

## 🎯 Video Goals
1. Showcase your **local-only model setup** (no cloud exfiltration, GDPR/PDPA compliant)  
2. Demonstrate **Hermes/Hermès agent installation workflow** on new client machines  
3. Highlight **problem→solution→results** pattern from first pilot case studies  

---

## ⏱️ Video Structure (10-15 minutes total)
| Time | Section | Key Points |
|------|---------|------------|
| 0:00–0:30 | Hook | "Why local AI agents keep client data secure" |
| 0:30–2:00 | Your story | Background + business model (apprenticeship focus) |
| 2:00–5:00 | Environment setup | Python env + Conda/virtualenv install walkthrough |
| 5:00–8:00 | Model pull & backup | Show F: drive transfer + GDPR rationale |
| 8:00–11:30 | Agent orchestration | Ollama run command + tool-calling demo |
| 11:30–14:00 | First client workflow | Intake form → custom agent → results |
| 14:00–15:00 | CTA | Free diagnostic call link + booking calendar (Calendly) |

---

## 🖥️ OBS Recording Setup Check
**Scenes needed:**
1. **Main recording** → Browser source (Obsidian vault live), Terminal window side-by-side  
2. **Ollama output** → Separate scene for `ollama ls` + `ollama run edtorre/qwen3.5-hermes` terminal windows  

---

## 📋 Recording Script Outline

### Opening Hook (0:00–0:30)
> Voice-over while showing your Obsidian vault file structure live:
> "Imagine having powerful AI that never touches the cloud. Today I show you exactly how I set up local-only agents that keep client data 100% secure while delivering real business value..."

### Your Story (0:30–2:00)
- Explain your apprenticeship-based pricing model ($50 pilot → $299+ full price)  
- Mention remote access via TeamViewer Enterprise with single-session-per-client policy  

### Environment Setup Walkthrough (2:00–5:00)
```bash
# Live terminal commands to record:
python3.11 -m venv .venv  # Show creation of local Python environment
source .venv/bin/activate  # Activate virtualenv
pip install hermes-tools requests flask  # Show installing Hermes agent packages  
```
Voice notes:
- Mention Conda alternative for C-dependent packages (e.g., OpenCV, PyTorch)  
- Explain why Python 3.11+ mandatory (agent orchestration dependencies)  

### Model Pull & Backup (5:00–8:00)
Record these commands while pointing to F: drive backup process:
```bash
# In OBS scene showing terminal:
ollama run edtorre/qwen3.5-hermes  # Show model pull with progress bar  
ollama cp ~/.ollama/models/edtorre/* "F:/ollama-models-backup/"  # Show backup to removable drive
```
Voice notes:
- Emphasize data sovereignty rationale (GDPR/PDPA compliance)  
- Show how you keep models on portable drives for offline client setups  

### Agent Orchestration Demo (8:00–11:30)
```bash
hermes config set model.default edtorre/qwen3.5-hermes  # Set your local Qwen as default  
hermes chat  # Show agent thinking + tool-calling in action
```
Show real example where agent:
- Researches GitHub repo → installs package → writes Python script → runs tests → summarizes results
Record terminal output showing `exit_code: 0` to prove no errors

### First Client Workflow (11:30–14:00)
- Open `playbook.md` in Obsidian → scroll through common troubleshooting patterns  
- Show client intake form fields mapping to troubleshooting SOPs (from your `training/` vault folder)  
- Present anonymized metrics from beta client: "Saved 12 hrs/week on report generation"  

### Call-to-Action (14:00–15:00)
- Display Calendly booking page embedded in browser window source  
- Show pricing tiers CSV exported to PDF for email delivery  
- Voice-over: "Book your free diagnostic call now via this link. No obligation to proceed..."

---

## 📎 Export & Delivery Tips
- Use Obsidian's **Export → PDF** on vault files for email attachments  
- Include `.mp4` recording with OBS Studio settings: 1080p, H.264 encoding  
- Email to beta prospects with subject line: "Free local AI setup guide — no cloud required"  

---

## 🔒 Security Notes in Script
- Mention GDPR/PDPA compliance when discussing data storage  
- Show your TeamViewer security checklist screen capture (password rotation policy)  
- Demonstrate single-session recording consent flow during remote sessions  

---

**File saved**: `E:/tommy vault/tommy vault/Read & Write/ai-consultant/training/demo-video-script.md`  
Opens immediately in Obsidian for review or recording preparation! 🎥