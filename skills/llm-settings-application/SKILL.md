---
name: llm-settings-application
title: Applying LLM Model Settings
description: Apply model generation parameters across Ollama, KoboldCpp, text-gen-webUI, and Silly Tavern backends.
category: mlops
tags: [ollama, koboldcpp, text-generation-webui, sillytavern, model-settings, parameters, cli]
---

# LLM Settings Application

## Trigger
Use when user wants to apply specific model generation parameters (temperature, top_p, top_k, penalties, context window) to a running LLM backend.

## Standard Parameter Profiles

### Thinking Mode (General Tasks)
- temperature: 1.0
- top_p: 0.95
- top_k: 20
- min_p: 0.0
- presence_penalty: 0.0
- repetition_penalty: 1.0
- num_ctx: 16384 (min 8k)
- smoothing_factor: 1.5 (where supported)

### Thinking Mode (Precise Coding)
- temperature: 0.6
- top_p: 0.95
- top_k: 20
- min_p: 0.0
- presence_penalty: 0.0
- repetition_penalty: 1.0
- num_ctx: 16384
- smoothing_factor: 1.5 (where supported)

### Instruct Mode (Non-Thinking)
- temperature: 0.7
- top_p: 0.80
- top_k: 20
- min_p: 0.0
- presence_penalty: 1.5
- repetition_penalty: 1.0
- num_ctx: 16384
- smoothing_factor: 1.5 (where supported)

## Backend-Specific Application

### Ollama (API)
```json
POST http://localhost:11434/api/chat
Content-Type: application/json

{
  "model":"MODEL_NAME:latest",
  "stream":false,
  "think":true,
  "options":{
    "temperature":1.0,
    "top_p":0.95,
    "top_k":20,
    "min_p":0.0,
    "presence_penalty":0.0,
    "repeat_penalty":1.0,
    "num_ctx":16384
  },
  "messages":[{"role":"user","content":"PROMPT"}]
}
```

### Ollama (CLI)
```bash
# Thinking mode
ollama run --reasoning -p temperature=1.0 -p top_p=0.95 -p top_k=20 -p presence_penalty=0.0 -p num_ctx=16384 MODEL_NAME:latest

# Instruct mode
ollama run -p temperature=0.7 -p top_p=0.8 -p presence_penalty=1.5 -p num_ctx=16384 MODEL_NAME:latest
```

### KoboldCpp
Set `Smooth_F=1.5` via UI: Settings → Samplers → Advanced

### text-generation-webui
Set via UI: Parameters → lower right (Smoothing=1.5)

### Silly Tavern
Set via UI: "Smoothing" parameter slider (1.5)

## Notes
- **Ollama does NOT support `smoothing_factor`** — specific to KoboldCpp / text-gen-webUI / Silly Tavern
- **Model name case matters** in Ollama — verify via `curl localhost:11434/api/tags`
- **Streaming**: Use `stream:true` for long generations; non-streaming may timeout
- **Thinking mode**: Use `"think":true` (API) or `--reasoning` (CLI) in Ollama

## Verification Steps
1. Query `/api/tags` to confirm model availability
2. Apply settings via API with test prompt
3. Check response metadata (eval_count, eval_duration)
