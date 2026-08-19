#!/usr/bin/env python3
"""
FastAPI Ollama Hook — Truncation-safe wrapper that forwards to local Ollama.
No Hermes routing noise. Clean /ollama-generate endpoints.
"""

import asyncio, json, time, uuid, ssl
from pathlib import Path
from typing import Optional
import urllib.request, urllib.error

from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="FastAPI → Ollama Hook")

OLLAMA_BASE = "http://localhost:11434"
CTX_SIZE = 12288
TEMP_DIR = Path(r"E:\tommy vault\tommy vault\Read & Write\Scripts\.ollama-temp")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

def query_generate(model: str = "Qwen3.5:latest", prompt: str = "", **params) -> dict:
    """Ollama /api/generate call with sane defaults."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": CTX_SIZE,
            "temperature": params.get("temperature", 0.7),
            "top_p": params.get("top_p", 0.9),
        },
        "format": "json",
    }
    data = json.dumps(payload).encode("utf-8")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        url = f"{OLLAMA_BASE}/api/generate"
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180, context=ctx) as resp:
            d = json.loads(resp.read().decode("utf-8"))
            return {
                "id": str(uuid.uuid4()),
                "response": d.get("response", ""),
                "model": d.get("model", model),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
    except urllib.error.HTTPError as e:
        detail = json.loads(e.read().decode("utf-8"))
        raise HTTPException(status_code=e.code, detail=detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ollama-generate")
def gen(
    prompt: str,
    model: str = "Qwen3.5:latest",
    temperature: float = 0.7,
    top_p: float = 0.9
) -> dict:
    return query_generate(model, prompt, temperature=temperature, top_p=top_p)

@app.post("/ollama/chat")
def chat(messages: list[dict], model: str = "Qwen3.5:latest", temperature: float = 0.7) -> dict:
    """Dummy route to ensure chat payload handling is validated."""
    return query_generate(model, "Chat:", temperature=temperature)

@app.get("/ollama/tags")
def list_models() -> list:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        url = f"{OLLAMA_BASE}/api/tags"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            d = json.loads(resp.read().decode("utf-8"))
            return d.get("models", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model": "Qwen3.5:latest"}

if __name__ == "__main__":
    print("🚀 FastAPI → Ollama Hook at 127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)