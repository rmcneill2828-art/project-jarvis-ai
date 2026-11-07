"""Measure the Child and Guest safety checker on this computer (ESR-0061 WP6d,
EIP-ESR0061-006 Section 6.8).

    python scripts/measure_moderation.py --sentences PATH [--chat-model qwen3.5:4b]

Uses the real classifier through the product's own `ModerationService` (on
the processor, fixed context), against a running Ollama. It reports:

* the first check (which loads the classifier), then the median and worst of
  20 checks of different sentences (every other line of the set);
* the median and worst check of five different typical replies (about 1,300
  characters each);
* the chat model's answer time with the classifier loaded beside it (first
  answer, which loads the model, then the median of three);
* what each model occupies (`/api/ps`: size and the part on the graphics card);
* how many of a fixed set of sentences the checker gets right, **as a fact,
  not a promise**.

The sentence file is kept **outside the public repository** on purpose: a
list of sentences the checker misses would be a list of ways past it. Each
line is `unsafe<TAB>sentence` or `safe<TAB>sentence`; `#` starts a comment.
The output never prints a sentence, only its line number.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from jarvis.interfaces.moderation import DEFAULT_CLASSIFIER_MODEL, ModerationService
from sentinel.ollama_provider import DEFAULT_NUM_CTX

DEFAULT_ENDPOINT = "http://localhost:11434"
TYPICAL_REPLY = (
    "Volcanoes form where hot, melted rock called magma rises from deep inside the Earth. "
    "Pressure builds up as gas in the magma cannot escape, and when the rock above gives way the magma "
    "bursts out as lava, ash and gas. Some volcanoes erupt gently, with lava flowing slowly down their sides, "
    "while others explode violently. "
) * 4
CHAT_QUESTIONS = (
    "Why is the sky blue? Answer in two sentences.",
    "Give me three tips for revising for a maths test.",
    "What is photosynthesis? Answer briefly.",
)


def read_sentences(path: Path) -> list[tuple[int, str, str]]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        label, _, sentence = line.partition("\t")
        if label not in ("safe", "unsafe") or not sentence.strip():
            msg = f"line {number}: expected 'safe' or 'unsafe', a tab, then the sentence"
            raise ValueError(msg)
        rows.append((number, label, sentence.strip()))
    return rows


def timed(action):
    start = time.perf_counter()
    result = action()
    return time.perf_counter() - start, result


def _post(endpoint: str, path: str, body: dict, timeout: float = 600.0) -> dict:
    request = urllib.request.Request(
        f"{endpoint}{path}", data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())


def _get(endpoint: str, path: str) -> dict:
    with urllib.request.urlopen(f"{endpoint}{path}", timeout=30) as response:
        return json.loads(response.read())


def loaded(endpoint: str) -> None:
    for model in _get(endpoint, "/api/ps").get("models", []):
        print(
            f"Loaded: {model.get('name')}: {model.get('size', 0) / 2**30:.2f} GiB in all, "
            f"{model.get('size_vram', 0) / 2**30:.2f} GiB on the graphics card"
        )


def summary(seconds: list[float]) -> str:
    return f"median {statistics.median(seconds):.2f} s, worst {max(seconds):.2f} s (n={len(seconds)})"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sentences", type=Path, required=True)
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--chat-model", default="qwen3.5:4b")
    args = parser.parse_args(argv)

    rows = read_sentences(args.sentences)
    service = ModerationService(args.endpoint, timeout_seconds=120.0)

    print(f"Classifier: {DEFAULT_CLASSIFIER_MODEL}; chat model: {args.chat_model}; endpoint {args.endpoint}")
    digest = hashlib.sha256(args.sentences.read_bytes()).hexdigest()
    print(f"Sentence set: {len(rows)} sentences, SHA-256 {digest}")
    first, _ = timed(lambda: service.check_input("Hello, how are you?"))
    print(f"First check (loads the classifier): {first:.2f} s")

    # Every other sentence, so the sample takes safe and unsafe alike whatever
    # order the file is in (WP6d review, Low).
    sample = rows[::2][:20]
    latencies = [timed(lambda sentence=sentence: service.check_input(sentence))[0] for _, _, sentence in sample]
    print(f"Message checks, 20 different sentences: {summary(latencies)}")

    # A different opening each time, so Ollama's prompt cache cannot answer
    # a repeat (WP6d review, Low): each is a fresh check of a typical reply.
    openings = ("Good question!", "Here is how it works.", "Let me explain.", "Great thing to ask.", "Sure.")
    replies = [
        timed(lambda opening=opening: service.check_output("How do volcanoes erupt?", f"{opening} {TYPICAL_REPLY}"))[0]
        for opening in openings
    ]
    print(f"Reply checks, about {len(TYPICAL_REPLY)} characters, each different: {summary(replies)}")

    chat_times = []
    for question in CHAT_QUESTIONS:
        seconds, _ = timed(
            lambda question=question: _post(
                args.endpoint,
                "/api/chat",
                # The product's own chat options (sentinel/ollama_provider.py).
                {
                    "model": args.chat_model,
                    "messages": [{"role": "user", "content": question}],
                    "stream": False,
                    "think": False,
                    "options": {"num_ctx": DEFAULT_NUM_CTX},
                },
            )
        )
        chat_times.append(seconds)
    print(
        f"Chat answers with the classifier loaded: first {chat_times[0]:.2f} s, "
        f"then median {statistics.median(chat_times[1:]):.2f} s of {len(chat_times) - 1}"
    )

    loaded(args.endpoint)

    right = {"safe": 0, "unsafe": 0}
    totals = {"safe": 0, "unsafe": 0}
    missed: list[int] = []
    unchecked: list[int] = []
    for number, label, sentence in rows:
        verdict = service.check_input(sentence)
        totals[label] += 1
        if verdict.unavailable:
            unchecked.append(number)
        elif verdict.allowed == (label == "safe"):
            right[label] += 1
        else:
            missed.append(number)
    print(
        f"Sentence set: unsafe stopped {right['unsafe']} of {totals['unsafe']}; "
        f"safe allowed {right['safe']} of {totals['safe']}"
    )
    print(f"Wrong (line numbers only): {missed or 'none'}; not checked: {unchecked or 'none'}")
    loaded(args.endpoint)
    return 0


if __name__ == "__main__":
    sys.exit(main())
