from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from spectral_head import complementary_radius, modulus_head, rank_bound  # noqa: E402


def main() -> None:
    roots = np.asarray([0.9, -0.8, 0.6 + 0.2j, 0.6 - 0.2j, 0.5, 0.2, 0.0])
    head, tail = modulus_head(roots, 0.5)
    rows = [
        {
            "sigma": sigma,
            "head_rank_upper_q_half": rank_bound(sigma**-1, 0.5),
        }
        for sigma in (1e-2, 1e-3, 1e-4, 1e-6)
    ]
    payload = {
        "status": "rh284_canonical_modulus_complete_spectral_head",
        "cutoff": 0.5,
        "synthetic_head_count": int(head.size),
        "synthetic_tail_count": int(tail.size),
        "synthetic_tail_radius": complementary_radius(roots, 0.5),
        "threshold_tie_left_in_tail": bool(np.any(np.isclose(tail, 0.5))),
        "rows": rows,
        "canonical_relative_to_cutoff": True,
        "cutoff_intrinsic_to_dynamics": False,
        "counterloop_spectral_identification": False,
        "gate_A": False,
        "gates_B_to_E": False,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"head": int(head.size), "tail": int(tail.size)}))


if __name__ == "__main__":
    main()
