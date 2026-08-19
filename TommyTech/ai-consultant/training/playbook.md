# 🎓 AI Setup Consultant Playbook v1.0
**Author**: Tommy Chan | **Created**: 2026-08-17 | **Version**: 1.0 (Alpha)  
**Vault Path**: `E:/tommy vault/tommy vault/Read & Write/ai-consultant/training/playbook.md`

---

## 📘 Purpose
This playbook is your living document for troubleshooting common Hermes/Ollama setup issues. Start here when a client calls with errors — most problems have known fixes documented in these sections.

---

## 🚨 Section 1: Common Hermes Install Errors + Fixes

### Error 1: Model Load Failures (GPU/CPU Detection)
```text
Error Message: "Failed to load model: device not available"

Fix Steps:
1. Check GPU RAM → Run `nvidia-smi` (or Intel DCHX utility for integrated GPUs)
2. If CPU fallback needed → Change quantization bit depth from 8 to 4/6 in Ollama config
3. Verify PATH → Model file must be under allowed directories (no /tmp or user-writable paths)
4. Reboot terminal → GPU kernel driver may need restart after install

Notes: Hermes works on CPU but is ~3x slower. For entry-level hardware, recommend 6–8 GB RAM minimum.
```

### Error 2: Terminal Command Failures (MSYS/Winpty Issues)
```text
Error Message: "bash: cannot change to '/c/Users/...' : No such file or directory"

Fix Steps:
1. Convert MSYS path to native Windows → `/c/Users/tommy` becomes `C:/Users/tommy`
2. Never use `cd /d` in .bat files (Windows background rules)
3. Avoid background operators `&` or PowerShell cmdlets like `Get-ChildItem` in scripts
4. Quote all paths with spaces: `"C:/path/to/folder"`

Notes: See Windows Path Handling lesson — document every error pattern here.
```

### Error 3: TeamViewer Connection Refusal
```text
Error Message: "Permission denied to access remote machine"

Fix Steps:
1. Ensure client grants admin-level permission (not just 'limited' access)
2. If firewall blocks → Client must allow TeamViewer exception in Windows Defender Firewall
3. Verify client's antivirus software isn't quarantining TeamViewer (common with McAfee/Bitdefender)
4. Use AnyDesk as fallback if TeamViewer fails after 3 retries

Notes: Always use single session only. Never ask for password storage in browser.
```

### Error 4: Python Environment Conflicts
```text
Error Message: "pip cannot install hermes-toolkit: package already exists"

Fix Steps:
1. Remove old conda env → `conda remove --name hermes` (only if client agreed)
2. Or create clean virtualenv → `python3 -m venv .hermes-env`
3. Activate via source command → `source activate .hermes-env` (Windows path quoting!)
4. Verify Python version → Hermes requires 3.11+ (not bundled python)

Notes: Document which model load fails on client machine and suggest alternatives.
```

### Error 5: Ollama Service Won't Start (Windows Background Daemon)
```text
Error Message: "ollama service is not running"

Fix Steps:
1. Check process manager → `systeminfo | findstr /i ollama`
2. Or run standalone via terminal → `ollama serve &` (with correct permissions)
3. Inspect logs → Look at Ollama's output directory for crash dumps
4. If service fails again → Recommend restarting Windows or running as admin

Notes: Some enterprise firewalls block outbound connections to port 11434 (Ollama's listen port). Client may need port firewall exception.
```

---

## 📋 Section 2: Workflow Design Patterns + Prompt Templates

### Pattern A: Research → Script Generation Agent
**Use-Case**: Client wastes hours manually reading papers → writing boilerplate code.

```text
Prompt Template (Few-Shot Example):
-----------------------------------------
System Instruction: "I'm building a custom Python agent for automated research."

User Task → "Research latest news on LLM safety alignment and summarize findings."

Few-Shot Examples:
1. Input → https://arxiv.org/abs/2401.XXXXX
   Output → "The paper proposes X method with 92% accuracy on benchmark A..."

2. Input → "Explain this formula in English"
   Output → "The equation represents the loss function for fine-tuning large models using LoRA."
   
Final Step → "Generate Python script that scrapes these arXiv links and saves summaries to my Obsidian vault."
```

**Tools**: Ollama (research mode), Python requests/BeautifulSoup, file paths to client's Obsidian directory.

---

### Pattern B: WhatsApp Order Bot for Shopee Sellers
**Use-Case**: SMEs losing orders via delayed DM responses on Instagram/TikTok → auto-sync stock + notify customers.

```text
Prompts:
---------
"Monitor new Shopee orders → Extract product ID, quantity, delivery date.
Send WhatsApp broadcast to buyer with tracking number and expected delivery window (±2 days)."

Few-Shot Example:
Input → "Customer asked if order #123 is shipped"
Output → "Yes, your order has been dispatched! Tracking: 1A9B7C. Expected by 2026-08-25."
```

**Integrations**: WhatsApp Business API (if client pays for official business profile), or LINE/Telegram webhooks as cheaper alternatives.

---

### Pattern C: Customer Support Q&A Bot (Bahasa/Malay)
**Use-Case**: F&B kiosks, mall vendors handling routine inquiries → reduce queue times.

```text
System Prompt: "You're a helpful assistant for {Store Name}. Answer questions in Bahasa/Malay."
Knowledge Base → Client's FAQ PDF or Obsidian notes linked to store policies.

Few-Shot Example:
Input → "Berapa harga nasi goreng hari ini?"
Output → "Nasi goreng dengan ayam hanya MYR 5.50 / porsi. Dengan tambahan telur = MYR 6.00."
```

**Training**: Start with 10 core Q&A pairs, expand as client provides more feedback.

---

## 🔒 Section 3: Security Checklist (GDPR/PDPA Compliance)

Before each session, confirm with client:

- [ ] All processing runs locally → no data leaves machine without explicit consent
- [ ] Client grants admin access via TeamViewer/AnyDesk only for session duration
- [ ] No scraping or reverse engineering allowed without written permission
- [ ] If client requires audit trail → Record session video and share encrypted backup link post-delivery

**What NOT to Do**:
- ❌ Never store client's API keys or credentials in your own machine
- ❌ Never forward logs to third-party analytics (avoid Google Analytics on landing page)
- ❌ Never monetize client data unless contract signed + revenue shared 70/30

---

## ⚡ Section 4: Performance Optimization Tips

### Tip A: Quantization Bit Depth Selection
```text
Client Has → CPU Laptop (No GPU):
  Recommend → Quantized GGUF models (q4_0 / q5_k_m for best balance)

Client Has → Mid-Range NVIDIA GPU:
  Recommend → fp16 model (fastest throughput), switch to q8_0 if memory limit reached

Warning → Higher bit depth = more accurate but slower on CPU-bound tasks. Test with client's hardware first.
```

### Tip B: Model Swapping Under Load (Enterprise Tiers)
```text
Pattern → Run multiple agents concurrently?

Solution → Use Ollama's `ollama serve` multi-model feature:
  - Agent #1 handles web research on GPU thread 1
  - Agent #2 writes Python scripts on CPU core 3–5
  - Auto-switch models based on latency thresholds (e.g., >200ms triggers next model)

Trade-Off → Requires ~2x RAM headroom. For single-user clients, warn about resource contention.
```

### Tip C: Obsidian Wiki Link Optimization
```text
Pattern → Client's vault lives on separate drive (E:/vault/)

Solution → Mount as local symlink during installation:
  - `mkdir "E:/tommy vault/tommy vault/Read & Write/ai-consultant/portfolio/case-studies"`
  - Document path in client handover doc with relative paths vs. UUID-based links

Risk → Network instability if mounted on remote drive. Recommend direct disk I/O for large media files.
```

---

## 📈 Section 5: Weekly Learning Goals (Track Progress)

### Week 1 Goal → Mastery of Tool Installation + Basic Config
- [ ] Install Hermes on own machine without external help
- [ ] Record demo video (`demo-01.mp4`) showing 2 agents in action
- [ ] Document all errors encountered + solutions found (update playbook.md)

### Week 2 Goal → Workflow Design Patterns + Prompt Optimization
- [ ] Build custom agent for client's specific task (research/coding/support)
- [ ] Refine prompt after first 3 sessions → output quality improved by X%
- [ ] Create handover doc template (PDF + video walkthrough)

### Week 3 Goal → Performance Tuning + Security Hardening
- [ ] Tune latency thresholds for client workflows
- [ ] Conduct security audit on a pilot client's deployment
- [ ] Draft case study with metrics ("Time saved per week: X hrs", "Revenue impact: Y%")

### Long-Term Goal (Month 3+) → Enterprise Features + Retainer Models
- [ ] Multi-user config + admin console setup demo
- [ ] Draft SLA terms for ongoing support retainers
- [ ] Build referral partnership pitch deck for system integrators

---

## 📚 Section 6: Resources + Further Reading

### Official Docs
- Hermes Project: GitHub repository → https://github.com/nousresearch/hermes-agent
- Ollama Models Hub: https://ollama.ai/library (quantized model files)

### Community Support
- r/LocalLLaMA Reddit community (weekly posts about tooling)
- LocalLLaMA Discord server (voice channels for troubleshooting)
- HuggingFace Spaces → "AI Agent" curated demos

### Tools You'll Use Daily
- OBS Studio (free video recording → no audio needed for client sessions)
- Teamviewer/AnyDesk Pro (business plan → encrypted remote access only)
- Python scripts installed via conda/pip → verify version compatibility first

---

## 📝 Appendix A: Template Handover Doc Structure

```markdown
# Hermes Setup Handover — Client Name

## ✅ Installation Checklist
- [ ] Ollama service running on startup (verified via `ollama list`)
- [ ] Python environment activated and functional
- [ ] Custom agents tested with real task (client's own data)

## 📖 How to Use Your Agents
1. Run command → `hermes run research` for web search + summarization
2. Or type prompt directly → `hermes interact "Explain this code"`
3. See docs folder → Troubleshooting guide included below

## 🔍 Troubleshooting Common Issues
- "Model load failed" → Check GPU vs CPU settings (see playbook Section 1)
- "Port 11434 blocked" → Windows Firewall exception needed on port 443
- etc. → See full troubleshooting table in main playbook

## 📞 Support Contact
- Email: [your-email@] (response time within 24 hrs)
- Slack/Discord channel link if client wants community access

## 📎 Attachments
- Recorded session video (encrypted backup available upon request)
- Additional prompt templates for advanced workflows
```

---

**Last Updated**: 2026-08-17 09:00 | **Next Review**: After first 5 clients served  
**Notes**: This playbook grows organically → add client-specific edge cases here as they arise. Version increments when new patterns emerge.