#!/usr/bin/env python3
"""
Direct Hermes-to-Ollama test harness (no external hooks needed).
"""

import json, urllib.request, urllib.error

OLLAMA = "http://127.0.0.1:11434"

def test(path, model="Qwen3.5:latest", prompt="ok", timeout=30):
    url = f"{OLLAMA}{path}"
    data = {"model": model, "prompt": prompt, "stream": False}
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            resp = json.loads(r.read().decode("utf-8"))
        return r.status, resp or {}
    except urllib.error.HTTPError as e:
        return e.code, {"error": str(e.reason), "text": e.read()}

def main():
    print("=== Hermes ↔ Ollama Hook Health Check ===\n")

    tests = [
        ("/api/generate", "Basic generate"),
        ("/api/chat", "Chat API (Ollama-native mode)"),
        ("/api/tags", "List installed models"),
    ]

    for path, name in tests:
        status, response = test(path)
        preview = response.get("response", response.get("model", "unknown"))[:60] if isinstance(response, dict) else type(response).__name__
        print(f"[{status:3d}] {name:15} → path={path}")
        if isinstance(response, dict) and "response" in response:
            print(f"         model={response.get('model', 'N/A'):15} | resp={preview}")
        elif "error" in response:
            print(f"         ⚠ Error: {response['error']}")
        else:
            print(f"         ℹ Response type: {preview}")
        print()

if __name__ == "__main__":
    main()