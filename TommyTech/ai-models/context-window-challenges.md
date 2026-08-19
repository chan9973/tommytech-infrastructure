# Context Window Challenges & Solutions

> The invisible bottleneck in local AI running — explained and solved.

---

## The Problem (Small Context Default)

Local AI models typically default to **4K tokens**:
- **Why?** Consumer hardware VRAM constraints
- **Result**: Models quickly forget conversation history after ~10-20 turns

### Real World Impact

```markdown
Example Conversation:
You: "Here's my resume..." (context: 500 tokens)
AI: "Can you summarize skills?" 
Me: [adds more context] (context: 2000 tokens now)
System: "Context nearly full..."
You: "Wait, what did it forget?"
Model: "[forgets earlier messages]"
```

**The Hidden Bottleneck**: Even if your GPU *can* handle larger contexts, the software defaults conservatively to protect against VRAM overflow.

---

## The Hardware Reality (VRAM Limits)

### Context Size = VRAM Consumption

| GPUs       | Base Model 7B | + 32K Context | Notes                           |
|------------|---------------|---------------|---------------------------------|
| RTX 3060 (12GB) | 5.5 GB        | Limited (~8K total context) | FlashAttention helps            |
| RTX 4090 (24GB)| 15.8 GB       | 20-64K        | Can handle large contexts        |
| Mac Studio (96GB RAM) | 40+ GB    | 128K+        | Unified memory = VRAM equivalent |

### The Scaling Problem

Expanding context isn't linear:
- 8K tokens → modest VRAM increase
- 32K tokens → **2x** the overhead
- 128K tokens → **4-6x** the base cost (depends on quantization)

---

## Optimization Solutions (FlashAttention + More)

### 1️⃣ FlashAttention (v1/v2/v3)

**What it does**: Splits attention computation, processes in chunks, recomputes.

**Results**:
- **50% VRAM reduction** on large contexts
- **2x-4x speedup** depending on model size
- Makes 64K context practical on consumer hardware

**Best paired with**: Quantized models + efficient cache management

---

### 2️⃣ KV Cache Paged Attention (vLLM/TGI)

**What it does**: Memory-managed approach to KV cache storage.

Think of it like an OS memory manager, but for model attention states.

**Benefits**:
- Enables much larger contexts without VRAM overflow
- Dynamically allocates/evicts cache pages
- Can handle 128K+ tokens on single GPU

---

### 3️⃣ KV Cache Quantization

**What it does**: Compresses the key-value cache (attention internals).

**Trade-offs**:
- q4 quantization → ~50% VRAM savings, negligible accuracy loss
- q6 quantization → ~35% VRAM savings, still excellent performance
- q8/FP16 → no compression (but fastest)

---

## 🔧 Practical Implementation

### Recommended Hardware+Software Stack

**Option A: Consumer GPU (NVIDIA)**
```python
# vLLM with paged attention + FlashAttention v2
pip install vllm[flash-attn]

vllm --model ... \
      --dtype "auto" \
      --trust-remote-code \
      --max-num-seqs 16 \
      --gpu-memory-utilization 0.75
```

**Option B: Apple Silicon Mac**
```python
# Use llama.cpp or mlx (native unified memory)
# M2/M3 Ultra treats total RAM as poolable VRAM
```

---

## 📊 Model Recommendations by Resource Budget

### Very Limited GPU (<10GB VRAM)
- Phi-3-mini **Q4_K_M** + FlashAttention v3
- 8K context default (acceptable for most chat)
- Enable smart summarization to extend effectively

### Mid-Tier GPU (12-24GB)
- Mistral-Nemo-12B **Q5_K_M** + FlashAttention v2
- Gemma-3-27B **Q4_K_M** (best context efficiency)
- 32K context realistic, 64K possible with optimizations

### High-End GPU/NVIDIA/Apple M-Series (≥24GB VRAM)
- Llama-3.1-8B **Q8_0** + FlashAttention v3
- Qwen-72B **Q5_K_M** for maximum reasoning on documents
- 128K context achievable

---

## 🎯 The Context Window Trade-Off Triangle

### Small Context (4K)
✅ Fast, cheap in VRAM  
❌ Forgets history after ~10-20 turns  
**Use cases**: Chat, quick Q&A, simple coding help

### Medium Context (8K-32K)
✅ Good balance for most use cases  
✅ Reasonable VRAM  
❌ Still constrained by hardware budget  
**Use cases**: Document analysis up to 15-20 pages, code review of small projects

### Large Context (64K-128K)
✅ Handles entire codebases/books  
✅ Multi-hour conversation memory  
✅ Complex multi-document workflows  
❌ Expensive in VRAM  
**Requires**: Quantization + FlashAttention + Paged Attention

---

## 🧪 Testing Your Current Setup

Ask these diagnostic questions:
```prompt
"Read my first message from 10 turns ago and quote it directly."
→ Models that struggle with long contexts will fail or hallucinate
```

**Better test**:
1. Send a lengthy context intro (~2K tokens)
2. Ask for summaries, tasks, etc.
3. Watch if quality degrades as conversation continues

---

## 📝 Tracking Your Model Performance

Create notes like:

```markdown
---
tags: [ai-model, benchmark]
model: [[qwen-q3]]
context-tested: true
context-size: 8K
performance-degraded-after: 12K tokens
recommended-max-context: 32K
---
```

---

## 🔗 Related Notes

- [[hardware-setup-guide]] - Your current hardware capabilities
- [[optimization-tech]] - Memory management techniques
- [[gemma-3-27b]] - The new king of context efficiency
- [[chunking-strategies]] - Divide and conquer for long docs
