"""The models JARVIS will recommend and download for local conversation
(ESR-0061 WP3c, EIP-ESR0061-003 6.9).

This is a table, kept apart from the logic that reads it so a model can be
added, removed or re-tuned without touching code. It is a Python module rather
than a JSON file only so the packaged sidecar needs no extra data-file
packaging step.

**It is also the allow-list for downloads**: JARVIS asks Ollama to pull a model
only if its tag is an entry here, so no other name can be fetched through the
app.

Every entry was checked against Ollama's registry on 8 October 2026: the tag
exists, its size is the sum of its manifest's layers, and the licence layer
reads Apache License 2.0 (the Qwen3.5 family). Choosing one family keeps the
licence question to one answer. `min_budget_gb` is the memory a machine must be
able to give the model - GPU memory, or a share of unified or system memory,
see `BUDGET_RULES` - before JARVIS recommends it; the figures come from the
measurements recorded in EIP-ESR0061-003.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CatalogModel:
    tag: str
    label: str
    download_bytes: int
    min_budget_gb: float
    license: str
    note: str


# Largest first. The last entry is the floor: it is recommended, with a warning,
# to a machine below every other entry's minimum.
MODELS: tuple[CatalogModel, ...] = (
    CatalogModel(
        tag="qwen3.5:9b",
        label="Qwen3.5 9B (best answers)",
        download_bytes=6_550_000_000,
        min_budget_gb=9.0,
        license="Apache-2.0",
        note="Best answers. Needs a graphics card with about 10 GB or more, or a Mac with 24 GB or more. On an 8 GB card it runs fast but cannot sit beside the safety model a Child profile needs.",
    ),
    CatalogModel(
        tag="qwen3.5:4b",
        label="Qwen3.5 4B (balanced)",
        download_bytes=3_320_000_000,
        min_budget_gb=4.5,
        license="Apache-2.0",
        note="Good answers on an 8 GB graphics card or a 16 GB Mac, with room left beside it for voice and safety models.",
    ),
    CatalogModel(
        tag="qwen3.5:2b",
        label="Qwen3.5 2B (light)",
        download_bytes=2_680_000_000,
        min_budget_gb=2.8,
        license="Apache-2.0",
        note="For smaller machines. Faster, with simpler answers.",
    ),
    CatalogModel(
        tag="qwen3.5:0.8b",
        label="Qwen3.5 0.8B (smallest)",
        download_bytes=1_320_000_000,
        min_budget_gb=0.0,
        license="Apache-2.0",
        note="Runs almost anywhere; answers are basic.",
    ),
)


@dataclass(frozen=True)
class BudgetRules:
    """How much of a machine's memory counts towards running a model."""

    # A graphics card's memory counts in full: the model must fit on it, or
    # part runs on the processor and answers slow sharply.
    gpu_fraction: float = 1.0
    # Apple Silicon shares one pool between the model, macOS, the voice models
    # and the safety model, so only half of it counts for the model (16 GB gives
    # 8, which selects the 4B model; 24 GB gives 12, which selects the 9B). To
    # be confirmed on the household Mac at Mac visit 1.
    unified_memory_fraction: float = 0.5
    # With no supported graphics card the model runs on the processor from
    # system memory: slow, so the budget is deliberately small and capped.
    cpu_fraction: float = 0.125
    cpu_cap_gb: float = 6.0
    # Free disk space needed beyond the download itself, as a fraction of it.
    disk_headroom_fraction: float = 0.2


BUDGET_RULES = BudgetRules()
