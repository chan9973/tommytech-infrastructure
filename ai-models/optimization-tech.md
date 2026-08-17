# Optimization Techniques Index

> Advanced methods to maximize performance on limited hardware.

---

## 🔥 GPU Memory Management

### FlashAttention (Speed & VRAM Savings)
**v1**: Basic attention splitting
- **Benefit**: 20-40% faster inference, 30% less VRAM
- **Best for**: General LLM inference

**v2**: Improved attention splitting algorithm
- **Benefit**: Additional 15-25% speed improvement
- **Best for**: Long context windows (16K-128K)

**v3 (Latest)**: Dynamic key-value cache optimization
- **Benefit**: Best memory efficiency, 50% VRAM savings on large models
- **Best for**: Production deployments, multi-turn conversations

---

### KV Cache Optimizations

**PagedAttention (vLLM/TGI)**
- Breaks KV cache into "pages" like operating system memory management
- **Benefit**: 50-70% VRAM reduction, enables larger context windows
- **Best for**: Serving multiple requests or large contexts

**KV Cache Quantization**
- Compress attention weights from FP16 to INT4/INT8
- **Benefit**: Save VRAM for loading larger models
- **Accuracy loss**: Negligible (<0.5% perplexity increase)

**Low-Rank Adaptation (LoRA) Caching**
- Store KV cache as low-rank decomposition: A×B matrices
- **Tradeoff**: 2x speedup, slight accuracy tradeoff

---

## 📉 Quantization Levels Guide

### Full Precision (FP16/FP32)
- **VRAM Usage**: ~2x the model size
- **Use when**: Training, fine-tuning, critical tasks
- **Example**: 7B model → 14GB VRAM

### INT8
- **VRAM Usage**: ~1.5x model size
- **Loss**: Minimal (imperceptible in most use cases)
- **Common suffix**: `-q8_0`, `-q8`

### Q4_K_M (Most Popular for Local Use!)
- **VRAM Usage**: ~4-4.5x parameters (7B → ~16GB for 7B model)
- **Accuracy**: Excellent for chat, coding, analysis
- **Best for**: Most local deployment scenarios
- **Common suffix**: `-q4_k_m`, `-q4`

### Q5_K_M / Q6_K
- Compromise between space and precision
- When you need higher accuracy than q4 but don't want q8 overhead

---

## 💡 Context Window Optimization

### 1. Drop/Forget Less Important Tokens
Models naturally forget early tokens. Techniques to help:
- **Attention Sink**: Train attention weights to decay on old tokens
- **Token Dropping**: Remove less important messages before context fills
- **Summarization**: Auto-compress old turns into summaries

### 2. Smart Chunking
For long documents/books:
```markdown
[[Chunking-for-long-contexts]] - See detailed guide
```

---

## 🧠 Advanced Techniques

### Sparse Attention
Only attend to truly relevant tokens, not all history.
- **Benefit**: Can extend effective context beyond nominal limits
- **Complexity**: Requires model modifications

### Selective State Models (SSMs)
Hybrid approach between transformers and RNNs:
- **Benefit**: Linear time/memory scaling with context
- **Examples**: Mamba, Jamba models

---

## 📊 When to Upgrade vs Optimize

### Optimize Hardware Use First
1. Try different quantizations (q4 → q5 → q6)
2. Enable FlashAttention v3
3. Add paged attention (vLLM or TGI backend)
4. Use context summarization
5. Consider model distillation for specific tasks

### Then Upgrade Hardware When
- Still hitting VRAM limits after all optimizations
- Need consistent responses within <20% time budget
- Working with models that can't be quantized (training tasks)
- Context window requirements keep growing beyond 128K

---

## 🔬 Benchmark Your Setup

Track performance in your Obsidian:
```markdown
---
model: [[current-model]]
benchmark-date: {{date}}
tokens-per-second: {{tps}}
vram-used: {{GB}}
tokens-per-second-at-full-context: {{tps-max}}
---
```
