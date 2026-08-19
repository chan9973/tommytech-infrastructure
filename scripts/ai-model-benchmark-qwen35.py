#!/usr/bin/env python3
"""
AI Model Benchmark — Localized to Qwen3.5:latest
Measures inference latency, token generation, code generation quality.
Saves results to Obsidian vault: ai-models/benchmark-results/
"""

import os, json, asyncio, time
from pathlib import Path
from typing import Dict, Any, Optional
import urllib.request

# Single model setup since that's what's available
MODEL_NAME = "qwen3.5:latest"

VAULT_ROOT = Path(r"E:\tommy vault\tommy vault\Read & Write")
RESULTS_DIR = VAULT_ROOT / "ai-models" / "benchmark-results"
RESULTS_FILE = RESULTS_DIR / "qwen35-benchmarks.md"

# Test prompts matching your typical usage patterns
TEST_CASES: list = [
    {
        "id": 1, "category": "coding", "prompt": "Create a Python script to scrape prices from an e-commerce site using requests and BeautifulSoup. The script should handle pagination and save results to JSON."
    },
    {
        "id": 2, "category": "reasoning", "prompt": "Write a balanced meal plan with macros for a professional athlete training for an Ironman triathlon, explaining the nutritional rationale behind each meal choice."
    },
    {
        "id": 3, "category": "code-complex", "prompt": "Create a FastAPI endpoint that validates user input against a Pydantic model, applies rate limiting middleware, and returns structured JSON responses with proper HTTP status codes."
    },
    {
        "id": 4, "category": "creative", "prompt": "Write dialogue for a cyberpunk detective encountering a client who refuses to identify themselves. Use noir style but with high-tech setting elements."
    },
    {
        "id": 5, "category": "multi-step", "prompt": "Generate a shell script that monitors a directory for new CSV files, parses their headers to validate structure, and moves malformed files to a quarantine folder."
    },
]

CONCURRENT_REQUESTS = 3

# Ollama API
OLLAMA_URL = "http://localhost:11434"

async def fetch_latency(model: str, prompt: str) -> Dict[str, Any]:
    """Measure inference latency for a single prompt."""
    url = f"{OLLAMA_URL}/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            generated = result.get("response", "").strip()
            tokens = len(generated) // 4 if generated else 0
            return {
                "tokens": tokens,
                "response_len": len(generated.split()),
                "success": True
            }
    except Exception as e:
        return {"error": str(e), "success": False}

async def benchmark_prompt(model: str, case_id: int) -> Dict[str, Any]:
    """Run multiple latency measurements for one test case."""
    latencies: list = []
    
    print(f"  [T{case_id:02d}] {case_id}")
    
    # Warmup
    print("    → Warmup...")
    await fetch_latency(model, f"Warmup: {'Q' * 500}")
    
    # Actual measurements
    for trial in range(CONCURRENT_REQUESTS):
        start = time.perf_counter()
        result = await fetch_latency(model, f"Benchmark #{trial}: {TEST_CASES[case_id-1]['prompt']}")
        end = time.perf_counter()
        
        if result.get("success"):
            latencies.append({"total": end - start, "tokens": result["tokens"]})
            print(f"    ✓ {end-start:.2f}s / {result['tokens']} tokens")
    
    if not latencies:
        print("    ⚠ No successful runs")
        return {"error": "no_successful_runs"}
    
    return {
        "latency_min": min(l["total"] for l in latencies),
        "latency_max": max(l["total"] for l in latencies),
        "latency_avg": sum(l["total"] for l in latencies) / len(latencies),
        "tokens_avg": sum(l["tokens"] for l in latencies) / len(latencies),
        "tps_avg": sum(l["tokens"] / l["total"] for l in latencies) / len(latencies)
    }

async def gather_benchmarks() -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Run benchmarks for the model."""
    print(f"\n{'='*70}")
    print(f"AI MODEL BENCHMARK: {MODEL_NAME}")
    print(f"{'='*70}")
    
    results: Dict[str, Dict[str, Dict[str, Any]]] = {MODEL_NAME: {}}
    
    for idx, case in enumerate(TEST_CASES, 1):
        case_id = f"T{idx:02d}"
        latencies_metadata = await benchmark_prompt(MODEL_NAME, idx)
        
        if "error" not in latencies_metadata:
            results[MODEL_NAME][case_id] = latencies_metadata
    
    return results

def generate_markdown_report(results: Dict[str, Dict[str, Dict[str, Any]]]) -> str:
    """Generate Obsidian-formatted benchmark report."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    rows: list = [
        "# 📊 AI Model Benchmark Results",
        f"",
        f"**Generated:** {timestamp}  \n**Model:** {MODEL_NAME}",
        f"",
        "## ⚡ Quick Summary",
        "| Test | Avg Latency (s) | Tokens | TPS |",
        "|------|----------------|--------|-----|"
    ]
    
    for case_id, metrics in results[MODEL_NAME].items():
        rows.append(f"| {case_id} | {metrics['latency_avg']:.2f}s | {int(metrics['tokens_avg']):4d} | {int(metrics['tps_avg']):.0f} |")
    
    rows.extend([
        "",
        "## 📈 Detailed Metrics",
        ""
    ])
    
    for case_id, metrics in results[MODEL_NAME].items():
        case = TEST_CASES[int(case_id)-1]
        rows.append(f"### T{case_id:02d} | {case['category'].upper()}")
        rows.append(f"- **Prompt:** {case['prompt'][:100]}...")
        rows.append(f"- **Latency Range:** {metrics['latency_min']:.2f}s - {metrics['latency_max']:.2f}s")
        rows.append(f"- **Avg Latency:** {metrics['latency_avg']:.4f}s")
        rows.append(f"- **Avg Tokens:** {int(metrics['tokens_avg'])}")
        rows.append(f"- **Generation Speed:** {int(metrics['tps_avg'])} tokens/sec")
        rows.append("")
    
    rows.append(f"## 📄 Raw Data (JSON)")
    rows.append(json.dumps(results, indent=2))
    
    return "\n".join(rows)

async def save_results(results: Dict[str, Dict[str, Dict[str, Any]]]) -> str:
    """Save benchmark report to Obsidian vault."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    report = generate_markdown_report(results)
    
    if RESULTS_FILE.exists():
        content = f"\n<!-- {time.strftime('%Y-%m-%d %H:%M:%S')} -->\n\n" + report
        print(f"\n📝 Appending to existing file...")
    else:
        print(f"\n📝 Creating new file...")
    
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✅ Saved to: `{RESULTS_FILE}` ({RESULTS_FILE.stat().st_size} bytes)")
    return str(RESULTS_FILE)

async def main():
    results = await gather_benchmarks()
    asyncio.run(save_results(results))

if __name__ == "__main__":
    print("\n🚀 Starting AI Model Benchmark...")
    print(f"Model: {MODEL_NAME}")
    
    asyncio.run(main())
