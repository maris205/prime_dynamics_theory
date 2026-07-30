import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fourier_defect import BETA, common_shift_moment  # noqa: E402


def main() -> None:
    rows = []
    for N in (15, 31, 63, 127, 255, 511):
        delta = (N + 1) ** -0.5
        m3 = common_shift_moment(N, 3, delta).real
        asym = -4 * BETA**3 * math.sqrt(N + 1) / math.pi
        rows.append({"N": N, "max_phase_error": delta, "third_moment": m3,
                     "leading_asymptotic": asym, "ratio": m3 / asym})
    payload = {"status": "rh274_fourier_defect_cloud_bridge_criterion", "beta": BETA,
               "rows": rows, "actual_cloud_nonbridge_proved": False, "gate_A": False}
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"rows": len(rows), "last_ratio": rows[-1]["ratio"]}))


if __name__ == "__main__":
    main()
