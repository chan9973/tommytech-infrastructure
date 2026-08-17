# AI Models Hub [[knowledge-map]]

> A curated library of local AI models optimized for different tasks and hardware constraints.

---

## 🗂️ Overview

This hub tracks AI models organized by:
- **Use Case**: chat, coding, document analysis, creative generation
- **Context Window**: 4K / 8K / 32K / 128K+ tokens
- **Hardware Requirements**: VRAM needs and optimization strategies
- **Optimization Tech**: FlashAttention, KV cache, quantization levels

---

## 📁 Folders

- `models/` - Individual model notes
- `hardware-guide.md` - Hardware recommendations
- `performance-notes.md` - Benchmark comparisons
- `optimization-tech.md` - Advanced techniques (FlashAttention, etc.)
- `use-case-matrix.md` - Which model for which task?

---

## 🔍 Quick Index

*Add new models by creating files in `/models/` folder following the template.*

```
[[models/gemma-3-27b]] - 128K context, optimal VRAM efficiency
[[models/qwen-2.5-72b]] - Strong reasoning, 32K default
[[models/codellama-34b-instruct]] - Coding specialist, 4096 tokens
[[models/mistral-large]] - General purpose, 32K context
```

---

## 🎯 By Context Window

### Small Context (<16K)
- Fast chat assistants
- Quick Q&A sessions
- [[models/phi-3-mini]] - Ultra-efficient for local hardware

### Medium Context (16K-32K)
- Document analysis up to ~20 pages
- Codebase exploration
- [[models/mistral-nemo-12b]] - Balanced performance/cost

### Large Context (64K+)
- Full book summarization
- Legal/medical document review
- [[models/gemma-3-27b]] - Cutting-edge context efficiency
- [[models/qwen-2.5-72b]] - Strong reasoning on large documents

---

## 🏷️ Tags

Use tag prefixes:
- `#hardware/cpu` - CPU-only optimized models
- `#hardware/gpu-macos` - Apple Silicon compatible
- `#hardware/gpu-nvidia` - CUDA accelerated
- `#context/4k` - Small window defaults
- `#context/128k` - Massive context support
- `#tech/flashattention-3` - Latest memory optimization

---

## 📝 Adding Models

Create template notes in `/models/` with:
```markdown
---
tags: [ai-model, {{context-size}}, {{hardware-type}}]
created: {{date}}
status: [[evaluating]] / [[tested]] / [[production]]
performance-notes: "See performance-notes.md"
---

## Model Overview

{{model-description}}

## Hardware Requirements

- Recommended GPU VRAM: ...
- Minimum RAM: ...
- Optimized for: {{cpu/gpu/cpu-gpu}}

## Context Window

- Maximum: {{size}} tokens
- Realistic sweet spot: {{practical-size}} tokens

## Use Cases

- Chat: ✅ / ❌
- Code generation: ✅ / ❌
- Long documents: ✅ / ❌
- Creative writing: ✅ / ❌
```

---

## 📊 Compare Models

Use this note for direct comparisons, benchmarking, and selecting the right model for your needs.
