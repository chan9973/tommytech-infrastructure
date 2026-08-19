#!/usr/bin/env python3
import requests, time

OLLAMA_BASE = "http://localhost:11434/api/generate"

# Warmup
print("Warming up...")
try:
    requests.post(OLLAMA_BASE, json={"model": "qwen3.5:latest", "prompt": "hi", "stream": False}, timeout=120)
    print("Ready.\n")
except Exception as e:
    print(f"Warmup skipped: {e}\n")

# Hermes Setup Checklist test
prompt = "You are a Hermes consultant. Walk me through verifying an Ollama installation on Windows MSYS2."
payload = {"model": "qwen3.5:latest", "prompt": prompt, "stream": False, "temperature": 0.1}

start = time.perf_counter()
resp = requests.post(OLLAMA_BASE, json=payload, timeout=120)
lat = (time.perf_counter() - start) * 1000

if resp.status_code == 200:
    data = resp.json()
    tokens = data.get("eval_count", 0)
    output = (data.get("response") or "")[:800]
    print("Status: OK")
    print(f"Latency: {round(lat, 2)}ms | Tokens: {tokens}")
    print("\nOutput preview:")
    print(output.replace("\n", " "))
else:
    print(f"HTTP {resp.status_code}: {resp.text[:200]}")
