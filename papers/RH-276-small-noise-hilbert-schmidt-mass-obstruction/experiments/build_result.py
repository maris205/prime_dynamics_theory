import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from hs_mass import ASYMPTOTIC_CONSTANT, explicit_lower_constant, hs_squared  # noqa: E402


def main() -> None:
    rows = []
    for sigma in (0.04, 0.02, 0.01, 0.005, 0.0025, 0.00125, 0.0005, 0.00025):
        value = hs_squared(sigma)
        scaled = sigma * value
        rows.append({"sigma": sigma, "hs_squared": value, "sigma_hs_squared": scaled,
                     "ratio_to_limit": scaled / ASYMPTOTIC_CONSTANT})
    payload = {"status": "rh276_small_noise_hilbert_schmidt_mass_obstruction",
               "asymptotic_constant": ASYMPTOTIC_CONSTANT,
               "explicit_unscaled_square_lower_constant": explicit_lower_constant(),
               "rows": rows, "raw_S2_zero_noise_convergence": False,
               "rank_growing_quotient_excluded": False, "gate_A": False}
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"rows": len(rows), "last_ratio": rows[-1]["ratio_to_limit"]}))


if __name__ == "__main__":
    main()
