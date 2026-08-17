---
tags: [machine-learning, research, ai-local]
created: 2026-08-15
updated: 2026-08-15
status: optimized-for-hardware
---

# AI Models Library [[Read & Write/vault-index]]

> Curated collection of local AI models for different tasks and hardware. **Qwen3.5 Hermes** is currently my system optimizer — the best model for running Hermes locally on consumer hardware! See [[hardware-setup-guide]] for your current setup recommendations.

---

## 🏆 Current System Optimizer ⭐️

**Qwen3.5-Hermes** (edtorre/qwen3.5-hermes:latest) - My discovery as the best local model for running Hermes at home! Perfect efficiency without context window bottlenecks, handles tool orchestration brilliantly, and optimized specifically for my hardware constraints.

Read full notes: [[models/qwen3.5-hermes-mathematical-optimization]]

---

## 🎯 Entry Points

* **For Choosing Models**: [[AI-Models-Library]] 
* **For Your Hardware**: [[hardware-setup-guide]]
* **For Quick Reference**: [[use-case-matrix]]
* **For Advanced Topics**: [[optimization-tech]], [[context-window-challenges]]
* **For Qwen3.5 Notes**: [[models/qwen3.5-hermes-mathematical-optimization]]

---

## 🏗️ Vault Structure

```
ai-models/
├── vault-index.md     👈 Start here
├── AI-Models-Library.md
├── hardware-setup-guide.md
├── optimization-tech.md
├── context-window-challenges.md
├── use-case-matrix.md
└── models/
    ├── qwen3.5-hermes-mathematical-optimization.md   ⭐️ Current champion
    ├── gemma-3-27b.md
    ├── qwen-2.5-72b.md
    ├── codellama-34b-instruct.md
    ├── mistral-nemo-12b.md
    └── phi-3-mini.md
```

---

## 📚 Model Collection

| Model | Size | Context Window | Best For | VRAM Required (Q4_K_M) | Status |
|-------|------|----------------|----------|-------------------------|--------|
| **Qwen3.5-Hermes** | ~8B* | 128K+ | System orchestration, tools | ~5GB* | ⭐️ Production |
| Gemma-3-27B | 27B | 128K+ | Massive documents, research | ~16GB | Production |
| Qwen-2.5-72B | 72B | 32K | Complex reasoning | ~28GB | Production |
| Mistral-Nemo-12B | 12B | 128K | Balanced all-around | ~4.5GB | Available |
| Codellama-34B | 34B | 8K-32K | Code analysis | ~6.5GB | Available |
| Phi-3-mini | 3.8B | 128K | Fast chat, efficient | ~1.2GB | Production |

*\*: Actual parameters for Qwen3.5-Hermes vary depending on variant; optimized for my Hermes deployment*

---

## 🔬 Current Topic: Context Window Limitations

NetworkChuck's key insight that powers this entire library:

> **"The primary hidden bottleneck of running local AI models: context window limitations"**

### What This Means for You

*Small Default Context Windows (4K)* → models forget earlier conversation parts  
*VRAM & Compute Constraints* → consumer hardware struggles with large contexts beyond default  
*Optimization Solutions* → FlashAttention, KV cache quantization, paged cache enable massive contexts

### Practical Impact

- **Standard consumers**: Hit context walls quickly (4K default)  
- **Mid-tier setups**: 8K-32K practical, requires optimizations  
- **High-end hardware**: 64K-128K possible with proper techniques  

### Optimization Hierarchy

1. **FlashAttention v3** → Cuts VRAM usage 30-50%  
2. **KV Cache Quantization (q4-q8)** → Compress attention states  
3. **Paged Attention (vLLM)** → Dynamic memory management  
4. **Context Summarization** → Compress old turns intelligently  

### Why Qwen3.5 Hermes Solves This

Built-in optimizations specifically for local deployment:
- Adaptive context window management → Never exceeds hardware limits
- FlashAttention-compatible architecture → Efficient even on older GPUs  
- Smart KV cache eviction → Maintains quality without VRAM explosion
- Quantization-friendly design → Works beautifully at q4_k_m quantization

---

## 🚀 How to Get Started

1. **Check your hardware**: [[hardware-setup-guide]] for tier recommendations
2. **Try Qwen3.5 Hermes**: Currently my go-to model for local Hermes deployments
   3. Select a specialized model: See [[AI-Models-Library]] or [[use-case-matrix]]
4. **Start small**: Begin with Q4_K_M quantization for efficiency (Qwen3.5 excels here!)
5. **Read more**: Explore [[optimization-tech]] before buying new hardware
6. **Track performance**: Update model notes with your benchmarks

---

## 📝 Adding Your First Model

1. Create new file: `ai-models/models/your-new-model.md`
2. Copy template from existing model notes (see Qwen3.5 for example structure)
3. Use YAML frontmatter for tags (e.g., context window, hardware type)
4. Add your testing performance notes
5. Link to [[AI-Models-Library]] in main index

---

## 🔗 Related Vault Notes

* Machine learning basics: [[coding/deep-learning-fundamentals]], [[coding/python-async-tutorial]]
* Research examples: [[coding/research-synthesis-demo]]
* Git automation: [[coding/git-commands-reference]]
* Personal notes: [[memories/profile.md]], [[memories/facts]]

---

## ✨ My Top Pick: Qwen3.5-Hermes

Why I switched to this model for my Hermes system:

1. **Efficiency**: Handles tool orchestration without VRAM bottlenecks
2. **Speed**: Fast responses on consumer hardware (RTX 4090 or M-series)  
3. **Context**: Practical 8K-32K window despite 128K capability
4. **Optimized**: Fine-tuned for agent workflows, Obsidian linking, local-first priorities

*"I recently found Qwen3.5-Hermes is the best for my system to running Hermes locally!"* - Tommy Chan

---

*Last edited*: 2026-08-15  
*Current status*: Optimized for consumer hardware + FlashAttention v3
