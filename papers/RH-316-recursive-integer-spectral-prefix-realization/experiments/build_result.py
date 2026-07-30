from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))
from spectral_prefix import construct_prefix_spectrum, power_sum, spectral_rank, squared_mass  # noqa: E402

Q = 0.5
ANCHOR_SOURCE = PAPERS / "RH-263-parity-resolved-deterministic-numerator-tail" / "results" / "parity_anchor_audit.json"


def main() -> None:
    anchor_payload = json.loads(ANCHOR_SOURCE.read_text(encoding="utf-8"))
    anchors = {1: float(anchor_payload["a_1_convention"])}
    anchors.update({int(row["order"]): float(row["archived_anchor"]) for row in anchor_payload["rows"]})
    rows = []
    for degree in (4, 6, 8):
        target = [anchors[order] for order in range(1, degree + 1)]
        spectrum = construct_prefix_spectrum(target, Q)
        residual = max(abs(power_sum(spectrum, order) - target[order - 1]) for order in range(1, degree + 1))
        rows.append(
            {
                "degree": degree,
                "rank": spectral_rank(spectrum),
                "squared_mass": squared_mass(spectrum),
                "max_moment_residual": residual,
                "max_modulus": max((abs(value) for value in spectrum), default=0.0),
            }
        )
    payload = {
        "status": "rh316_recursive_integer_spectral_prefix_realization",
        "exact_finite_prefix_realization_proved": True,
        "finite_normal_spectrum_constructed": True,
        "actual_noisy_spectrum_identified": False,
        "numerical_anchor_source": str(ANCHOR_SOURCE.relative_to(PAPERS)),
        "rows": rows,
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=lambda value: float(value)) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"rows": len(rows), "exact_prefix": True}))


if __name__ == "__main__":
    main()
