"""Measure local models on this machine for JARVIS (ESR-0061 WP3c).

For each model: how long it takes to load, how fast it answers once loaded, and
how much of it ended up in graphics-card memory (Ollama's `/api/ps` reports the
total size and the part resident on the GPU) - alone, and with a small safety
classifier loaded beside it, which is what a Child profile needs (WP6 chooses
the real one; `llama-guard3:1b` stands in). A model that does not fit beside
the classifier shows as only partly GPU-resident, and its speed falls.

Run on each machine that will host JARVIS and record the table in
EIP-ESR0061-003:

    python scripts/measure_ollama.py --models qwen3.5:9b qwen3.5:4b --guard llama-guard3:1b

Uses only Ollama's local HTTP API; downloads nothing and changes nothing.
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
import time
import urllib.request

import psutil

PROMPT = (
    "You are JARVIS, a concise household assistant. In about 120 words, explain how a family of four can plan a "
    "week of healthy dinners on a modest budget."
)
GIB = 1024**3


def post(endpoint: str, path: str, body: dict, timeout: float = 600) -> dict:
    request = urllib.request.Request(
        f"{endpoint}{path}", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())


def get(endpoint: str, path: str) -> dict:
    with urllib.request.urlopen(f"{endpoint}{path}", timeout=10) as response:
        return json.loads(response.read())


def unload(endpoint: str, model: str) -> None:
    post(endpoint, "/api/generate", {"model": model, "keep_alive": 0, "stream": False})


def resident(endpoint: str) -> dict[str, tuple[float, float]]:
    """name -> (total GiB, GPU-resident GiB) for every loaded model."""

    return {
        item["name"]: (item["size"] / GIB, item.get("size_vram", 0) / GIB) for item in get(endpoint, "/api/ps")["models"]
    }


def generate(endpoint: str, model: str) -> dict:
    return post(
        endpoint,
        "/api/generate",
        {
            "model": model,
            "prompt": PROMPT,
            "stream": False,
            "think": False,
            "keep_alive": "10m",
            "options": {"num_ctx": 4096, "num_predict": 220},
        },
    )


def measure(endpoint: str, model: str, guard: str | None, runs: int) -> dict:
    for name in list(resident(endpoint)):
        unload(endpoint, name)
    time.sleep(1)
    started = time.monotonic()
    first = generate(endpoint, model)
    cold_seconds = time.monotonic() - started
    warm = [generate(endpoint, model) for _ in range(runs)]
    speeds = [r["eval_count"] / (r["eval_duration"] / 1e9) for r in warm if r.get("eval_duration")]
    total_alone, gpu_alone = resident(endpoint).get(model, (0.0, 0.0))
    result = {
        "model": model,
        "cold_start_s": round(cold_seconds, 1),
        "load_s": round(first.get("load_duration", 0) / 1e9, 1),
        "warm_tok_per_s": round(statistics.median(speeds), 1) if speeds else None,
        "warm_total_s": round(statistics.median(r["total_duration"] / 1e9 for r in warm), 1),
        "size_gb": round(total_alone, 1),
        "gpu_gb_alone": round(gpu_alone, 1),
        "ram_used_pct": psutil.virtual_memory().percent,
    }
    if guard:
        post(endpoint, "/api/generate", {"model": guard, "prompt": "hello", "stream": False, "keep_alive": "10m"})
        again = [generate(endpoint, model) for _ in range(runs)]
        both = resident(endpoint)
        speeds_with = [r["eval_count"] / (r["eval_duration"] / 1e9) for r in again if r.get("eval_duration")]
        total_with, gpu_with = both.get(model, (0.0, 0.0))
        result.update(
            warm_tok_per_s_with_guard=round(statistics.median(speeds_with), 1) if speeds_with else None,
            gpu_gb_with_guard=round(gpu_with, 1),
            gpu_pct_with_guard=round(100 * gpu_with / total_with) if total_with else None,
            guard_gpu_gb=round(both.get(guard, (0.0, 0.0))[1], 1),
            both_loaded=model in both and guard in both,
        )
    for name in list(resident(endpoint)):
        unload(endpoint, name)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--endpoint", default="http://localhost:11434")
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--guard", default=None, help="small safety model to co-load (stand-in for WP6's)")
    parser.add_argument("--runs", type=int, default=2)
    args = parser.parse_args()

    print(f"machine: {platform.system()} {platform.machine()}, {psutil.virtual_memory().total / GIB:.0f} GB RAM")
    print(f"ollama: {get(args.endpoint, '/api/version')['version']}")
    for model in args.models:
        print(json.dumps(measure(args.endpoint, model, args.guard, args.runs)), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
