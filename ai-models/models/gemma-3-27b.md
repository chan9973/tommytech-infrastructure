---
tags: [ai-model, #context/128k, #hardware/gpu-nvidia]
created: 2026-08-15
status: production
performance-notes: "Best-in-class context efficiency"
---

# Gemma 3 (27B) ⭐️ Context King

> Cutting-edge large context model with exceptional VRAM efficiency. Google's latest gem pushes the boundaries of what local hardware can handle.

---

## Model Overview

- **Parameters**: 27 billion
- **Context Window**: Up to **128,000 tokens** (industry-leading)
- **Developer**: Google (open weights with licensing)
- **Quantization Targets**: Q4_K_M or Q5_K (recommended)

---

## Hardware Requirements

**Minimum VRAM (Q4 quantized)**:
- NVIDIA GPU: 16GB+ (RTX 3070 Ti or better)
- Apple Silicon: M2 Pro (48GB unified RAM minimum)

**Recommended VRAM (Q5_K_M + FlashAttention v3)**:
- NVIDIA: RTX 4080/4090 (20-24GB) ✓ Optimal
- Apple Mac Studio: M2 Ultra 96GB+ unifies

---

## Why It's Special for Local AI

### 1. Massive Context, Reasonable VRAM Usage
Despite its 128K window capability, Gemma 3's memory management is brilliant:
- Uses FlashAttention aggressively under the hood
- Smart KV cache eviction keeps effective costs low
- Practical max context: ~76K tokens on mid-tier hardware

### 2. Context Efficiency Comparison

| Model            | Same Prompt Quality @ 100K Tokens |
|------------------|-----------------------------------|
| Standard models  | Need 4x VRAM                      |
| Qwen-2.5-72B Q6_K| Similar quality, higher overhead  |
| **Gemma 3**      | **Best balance of power/cost** ✓  |

---

## Use Cases Where It Shines

### ✅ Perfect For
- Reading entire technical books (10K+ tokens each)
- Analyzing multi-hour call transcripts
- Legal document review (contracts + evidence)
- Coding sessions with complex context needs
- Research tasks requiring full paper + data context

### ⚠️ Consider Lower Models For
- Simple chat/conversation (3B-8B models faster)
- Very lightweight coding help (Codellama lighter)

---

## Performance Benchmarks (on RTX 4090 Q5_K_M)

| Task                    | Speed           | Notes              |
|-------------------------|-----------------|--------------------|
| Chat responsiveness     | ~25 tokens/s    | Smooth, real-time |
| Context fill (128K)     | Starts at ~10  | Gradual slowdown  |
| Code generation         | ~28 tokens/s    | Strong quality     |
| Summarizing books       | ~15 tokens/s    | Maintains quality  |

---

## Optimization Stack Required

To fully leverage its 128K capability:
```python
# Recommended setup
from llama_cpp import Llama

llm = Llama(
    model_path="path/to/gemma3-q5-k_m.gguf",
    n_gpu_layers=-1,           # Enable GPU offloading
    flash_attn=True,           # Essential for large context
    n_ctx=65536,               # Set to your hardware limit (~76K)
    use_mlock=False,           # Let system manage VRAM
)
```

---

## Quantization Guide

**q4_k_m**: 
- VRAM efficient: ~4.5B parameters × 2 = ~16GB needed
- Best for daily use, slight accuracy trade-off

**q5_k_m**:
- Sweet spot: balance
- Additional ~5% VRAM but much better quality

**q6_k / q8_0**:
- Only for high-end GPUs (4090+)
- Training/fine-tuning tasks only

---

## 🔗 Related Notes

- [[optimization-tech]] - FlashAttention setup guide
- [[context-window-challenges]] - Understanding context limits
- [[models/quantization-guide]] - Quantization deep dive

---

## 📝 Testing Results (Community)

*Add your own observations here:*
```markdown
- Pros: Handles enormous documents gracefully
- Cons: Slightly higher latency than smaller models at small contexts
- Tip: Use smart summarization for multi-hour transcripts
- Warning: On 16GB VRAM, max practical context is ~50K not 128K
```
