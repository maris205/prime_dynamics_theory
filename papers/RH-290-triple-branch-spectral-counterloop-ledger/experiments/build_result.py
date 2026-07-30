from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from triple_ledger import complete_count, coordinatewise_union, score  # noqa: E402


def main() -> None:
    spectral = (True, False, True, True, True)
    counterloop = (True, True, False, True, True)
    union = coordinatewise_union(spectral, counterloop)
    payload = {
        "status": "rh290_triple_branch_spectral_counterloop_ledger",
        "noisy_spectral_ledger": list(spectral),
        "graded_counterloop_ledger": list(counterloop),
        "spectral_score": score(spectral),
        "counterloop_score": score(counterloop),
        "coordinatewise_union": list(union),
        "coordinatewise_union_legal": False,
        "cross_branch_weighted_glue": False,
        "direct_weighted_complement_anchor_prefix": False,
        "weighted_full_trace_counterloop_anchor": False,
        "weighted_head_counterloop": False,
        "complete_count": complete_count([spectral, counterloop]),
        "gate_A": False,
        "gate_B": False,
        "gate_C": False,
        "gate_D": False,
        "gate_E": False,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"scores": [score(spectral), score(counterloop)], "complete": 0}))


if __name__ == "__main__":
    main()
