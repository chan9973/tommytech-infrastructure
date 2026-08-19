# Hardware Setup Guide

> Your local hardware requirements for running AI models at home.

---

## 💻 Recommended Hardware Tiers

### Entry-Level Local AI Setup ($500-800 budget)
- **GPU**: RTX 3060 (12GB) or RX 7900 GRE (16GB)
- **VRAM**: Minimum 12GB
- **RAM**: 32GB minimum, 64GB recommended
- **Best for**: 8GB parameter models, small context windows
- **Examples**: Phi-3-mini, Qwen-1.5-1.8B

---

### Mid-Range Local AI Setup ($1000-2000)
- **GPU**: RTX 4070 Ti Super (16GB) or dual RTX 3090s
- **VRAM**: 24+ GB total
- **RAM**: 64GB
- **Best for**: Up to 30B parameter models, medium context
- **Examples**: Mistral-Nemo-12B (quantized), Llama-3.1-8B

---

### High-End/Prosumer Local AI Setup ($3000+)
- **GPU**: RTX 4090 (24GB) or Mac Studio with M2 Ultra
- **VRAM**: 24GB+ on GPU / up to 192GB unified RAM on Apple
- **RAM**: 64GB minimum, 96GB preferred
- **Best for**: 70B parameter models, large document analysis
- **Examples**: Llama-3.1-70B (q8), Gemma-3-27B

---

### CPU-Only Setup (Limited but functional)
- **Best for**: Ultra-small models (<5B params) or experimentation
- **Performance**: 10-50x slower than GPU equivalents
- **Use when**: No GPU available, education/demo purposes
- **Examples**: Phi-3-mini-int4 (~5 tokens/sec on modern CPU)

---

## 🍎 Apple Silicon Notes

M2/M3 Ultra Macs use unified memory that pools across all components:
- Total RAM = Available VRAM (not like discrete GPU)
- M2 Ultra 192GB → Treat as 192GB VRAM for AI
- Excellent price/performance for creative AI workloads
- Use for: Image generation, medium models, local LLMs

---

## 📋 Quick Reference

### Model Size vs Hardware (Rule of Thumb)
| GPU VRAM | Parameter Range | Context Window | Example Models |
|----------|-----------------|-----------------|----------------|
| 6-8 GB    | 3-8B params     | 4K-32K          | Phi-3, Llama-3-8B (q4) |
| 12-16 GB  | 7-30B params    | 8K-32K          | Mistral-Nemo, CodeLlama-34B (q5) |
| 24GB+     | 30-70B params   | 32K-128K        | Gemma-3-27B, Qwen-72B (quantized) |

---

## ⚡ Optimization First!

Before upgrading hardware, try:
1. **Quantization**: q4_k_m → q5_k_m → q8 for your use case
2. **FlashAttention**: Reduces VRAM and speeds up inference
3. **Paged Attention**: Better context management
4. **KV Cache Quantization**: Save 50-70% VRAM at low accuracy loss

---

## 🔍 Hardware Detection Note

```markdown
---
tags: [hardware, hardware/cpu, ai-model]
model: [[qwen-q3]] # Track your current setup
last-tested: {{date}}
---
```
