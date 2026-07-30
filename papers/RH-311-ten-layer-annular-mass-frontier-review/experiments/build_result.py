from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from annular_review import batch_status  # noqa: E402


def main() -> None:
    payload = {"status": "rh311_ten_layer_annular_mass_frontier_review"}
    payload.update(batch_status())
    payload.update(
        {
            "hilbert_polya_constructed": False,
            "riemann_zeros_identified": False,
            "von_mangoldt_trace_proved": False,
            "zeta_divisor_equality": False,
            "riemann_hypothesis_proved": False,
        }
    )
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "papers": len(payload["paper_numbers"]),
                "complete": payload["complete_count"],
            }
        )
    )


if __name__ == "__main__":
    main()
