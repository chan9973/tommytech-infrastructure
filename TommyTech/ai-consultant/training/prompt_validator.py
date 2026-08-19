#!/usr/bin/env python3
# Prompt Validator: Runs playbook templates against local Ollama and logs real metrics.
import json, time, requests

OLLAMA_BASE = "http://localhost:11434/api/generate"

def run_test(name: str, prompt: str, **params) -> dict:
    payload = {"model": "qwen3.5:latest", "prompt": prompt, "stream": False, **params}
    start = time.perf_counter()
    try:
        resp = requests.post(OLLAMA_BASE, json=payload, timeout=120)
    except Exception as e:
        return {"name": name, "status": "error", "message": str(e)}
    lat = (time.perf_counter() - start) * 1000
    if resp.status_code != 200:
        return {"name": name, "status": "http_error", "code": resp.status_code}
    data = resp.json()
    return {
        "name": name,
        "status": "ok",
        "latency_ms": round(lat, 2),
        "tokens": data.get("eval_count", 0),
        "output": (data.get("response") or "")[:300]
    }

def warmup():
    print("Warming up Ollama (model load)...")
    try:
        requests.post(OLLAMA_BASE, json={"model": "qwen3.5:latest", "prompt": "hi", "stream": False}, timeout=120)
        print("Warmup complete.\n")
    except Exception as e:
        print(f"Warmup failed (proceeding anyway): {e}\n")

def main():
    warmup()
    tests = [
        ("Research Summarizer",
         "Research: LLM hallucination resistance in safety-critical domains. Return: 4-sentence bullet summary + 1 citation format.",
         {"temperature": 0.2}),
        ("Bahasa Q&A Bot",
         "Explain how to reset a router in simple Bahasa. Tone: friendly, instructional, no jargon.",
         {"temperature": 0.5}),
        ("Hermes Setup Checklist",
         "You are a Hermes consultant. Walk me through verifying an Ollama installation on Windows MSYS2.",
         {"temperature": 0.1}),
    ]

    print("\n=== VALIDATION RESULTS ===")
    for name, prompt, params in tests:
        res = run_test(name, prompt, **params)
        print(f"\n● {res.get('name', 'unknown')}: {res.get('status', 'N/A')}")
        if res.get("latency_ms") is not None:
            print(f"  Latency: {res['latency_ms']}ms | Tokens: {res.get('tokens', 'N/A')}")
        if res.get("output"):
            print(f"  Output preview: {res['output'].replace(chr(10), ' ')[:200]}...")
        if res.get("message"):
            print(f"  Error: {res['message']}")

if __name__ == "__main__":
    main()