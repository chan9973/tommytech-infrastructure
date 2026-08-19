#!/usr/bin/env python3
"""
AI Model Benchmark — Laguna X vs Qwen3.5
Measures inference latency, token generation, code generation quality.
Saves results to Obsidian vault: ai-models/benchmark-results/
"""

import os, json, asyncio, time
from pathlib import Path
from typing import Dict, Any, Optional
import urllib.request

VAULT_ROOT = Path(r"E:\tommy vault\tommy vault\Read & Write")
RESULTS_DIR = VAULT_ROOT / "ai-models" / "benchmark-results"
RESULTS_FILE = RESULTS_DIR / "laguna-x-vs-qwen35-benchmarks.md"

# Test prompts matching your typical usage patterns
TEST_CASES: list[Dict[str, str]] = [
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

async def fetch_latencies(model: str) -> Dict[int, Dict[str, Any]]:
    """Run latency tests for a single model."""
    print(f"\n📊 Benchmarking: {model}")
    print("-" * 60)
    
    results: Dict[int, Dict[str, Any]] = {}
    
    for idx, case in enumerate(TEST_CASES, 1):
        case_id = f"T{idx:02d}"
        try:
            print(f"  [{case_id}] {case['category'].upper():12s} - {case['prompt'][:50]}...")
            
            # Warm-up
            print("    → Warm-up...")
            await generate_for_model(model, f"Warm-up: {'A' * 500}")
            
            # Actual benchmark
            latencies, tokens = await benchmark_single_prompt(model, case)
            if latencies and tokens:
                results[case['id']] = {
                    "latency_min": latencies[0]["total"],
                    "latency_max": max(latencies),
                    "latency_avg": sum(latencies) / len(latencies),
                    "tokens_generated": tokens[0],
                    "tokens_per_sec": round(tokens[0] / latency - min(latencies) if latency and latency[0]["total"] > 0 else 0, 2),
                    "latency_unit": "seconds"
                }
                print(f"    ✓ {latency[0]['total']:.2f}s / {tokens[0]} tokens")
                
        except Exception as e:
            print(f"    ⚠ ERROR: {e}")
            results[case['id']] = {"error": str(e)}
    
    return results

async def benchmark_single_prompt(model: str, case: Dict[str, str]) -> Optional[tuple[list, list]]:
    """Run multiple concurrent latency measurements for one prompt."""
    latencies: list = []
    tokens: list = []
    
    for trial in range(CONCURRENT_REQUESTS):
        start = time.perf_counter()
        response = await generate_for_model(model, f"Benchmark #{trial}: {case['prompt']}")
        end = time.perf_counter()
        
        generated = response.strip() if response else ""
        tokens_est = 0
        for word in generated.split():
            tokens_est += max(1, len(word) // 4)
        
        latencies.append({"total": end - start})
        tokens.append(tokens_est)
    
    return latencies, tokens if tokens else [0]

async def generate_for_model(model: str, prompt: str) -> str:
    """Generate text from model via Ollama API."""
    url = f"http://localhost:11434/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,  # Block for direct response
        "format": "json"
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result.get("response", "")

async def gather_benchmarks() -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Run concurrent benchmarks for all models."""
    models = ["lagunax:latest", "qwen3.5:latest"]
    
    print("=" * 70)
    print(f"AI MODEL BENCHMARK")
    print(f"Hardware: RTX 3060 (12GB VRAM) | RAM: 32GB | Concurrent: {CONCURRENT_REQUESTS}")
    print("=" * 70)
    
    all_results: Dict[str, Dict[str, Dict[str, Any]]] = {model: {} for model in models}
    
    # Run benchmarks for each model
    for model in models:
        print(f"\n\n🧪 Testing: {model}")
        print("-" * 60)
        all_results[model] = await fetch_latencies(model)
    
    return all_results

def generate_markdown_report(results: Dict[str, Dict[str, Dict[str, Any]]]) -> str:
    """Generate Obsidian-formatted benchmark report."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Create header section
    md = [
        f"# 📊 AI Model Benchmark Results",
        f"",
        f"**Generated:** {timestamp}  \n**Hardware:** RTX 3060 (12GB) | RAM: 32GB | Concurrent: {CONCURRENT_REQUESTS}",
        f"",
        f"## 🔍 Quick Comparison Table",
        f"| Model | Avg Latency | Min Latency | Max Latency | Best Use Case |",
        f"|-------|------------|------------|------------|---------------|"
    ]
    
    # Build comparison row for each model
    for model, cases in results.items():
        if cases:
            cases_sorted = sorted(cases.values(), key=lambda x: x.get("latency_avg", 0))
            if cases_sorted:
                best_case = cases_sorted[0]
                avg = best_case.get("latency_avg", 0)
                min_lat = best_case.get("latency_min", 0)
                max_lat = best_case.get("latency_max", 0)
                tokens = best_case.get("tokens_generated", 0)
                
                # Categorize performance
                if avg < 8:
                    perf = "⭐ Excellent"
                    category = "General / Agent"
                elif avg < 12:
                    perf = "⚡ Good"
                    category = "Task-specific"
                else:
                    perf = "🐢 Moderate"
                    category = "Basic queries"
                
                md.append(f"| {model.replace(':', '')} | {avg:.2f}s | {min_lat:.2f}s | {max_lat:.2f}s | {category} ({perf}) |")
                md.append(f"| {model.replace(':', '')} → Best: {best_case.get('category', 'N/A')} ({tokens} tokens) |")
    
    # Detailed results by prompt
    md.extend([
        "",
        f"## 📈 Detailed Results by Test Case",
        f"### Code Generation (`coding`)"
    ])
    
    for model, cases in results.items():
        for case_id, metrics in cases.items():
            if "error" not in metrics:
                category = next((c["category"] for c in TEST_CASES if c["id"] == int(case_id)), "N/A")
                md.append(f"#### {model.replace(':', '')} | T{case_id:02d} | {category}")
                md.append(f"- Average: {metrics['latency_avg']:.2f}s | Range: {metrics['latency_min']:.2f}s - {metrics['latency_max']:.2f}s")
                md.append(f"- Tokens: {metrics['tokens_generated']} | Tokens/sec: {metrics['tokens_per_sec']}")
    
    # Raw JSON for data analysis
    md.extend([
        "",
        "",
        f"## 📄 Raw Data (JSON)"
    ])
    md.append(json.dumps(results, indent=2))
    
    return "\n".join(md)

async def save_results(results: Dict[str, Dict[str, Dict[str, Any]]]) -> str:
    """Save benchmark report to Obsidian vault."""
    # Ensure directory exists
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate markdown
    report = generate_markdown_report(results)
    
    # Append to existing file if it exists
    if RESULTS_FILE.exists():
        print(f"\n📝 Appending to existing benchmarks file...")
        content = f"\n<!-- {time.strftime('%Y-%m-%d %H:%M:%S')} -->\n\n" + report
    else:
        print(f"\n📝 Creating new benchmarks file...")
        content = report
    
    # Write to vault
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Report saved to:")
    print(f"   - File: `{RESULTS_FILE}`")
    print(f"   - Size: {RESULTS_FILE.stat().st_size} bytes")
    
    return str(RESULTS_FILE)

def main():
    """Entry point."""
    asyncio.run(gather_benchmarks())

if __name__ == "__main__":
    print("\n🚀 Starting AI Model Benchmark...")
    print("Ensure Ollama is running: `ollama serve`")
    
    import sys
    if len(sys.argv) > 1:
        model = sys.argv[1]
        # Quick latency test for single model
        print(f"\n⚡ Quick latency test for: {model}")
        results = asyncio.run(fetch_latencies(model))
        for case_id, metrics in results.items():
            print(f"T{case_id:02d}: {metrics['latency_avg']:.2f}s avg ({metrics['tokens_generated']} tokens)")
    else:
        # Full benchmark
        import asyncio
        results = asyncio.run(gather_benchmarks())
        asyncio.run(save_results(results))
