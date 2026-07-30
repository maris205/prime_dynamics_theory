import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from minrank import ideal_factor, minimal_rank  # noqa: E402


def main() -> None:
    rows = [{"N": n, "minimal_rank": minimal_rank(n), "factor_at_0_2": ideal_factor(n, 0.9, 0.2).real} for n in (1, 2, 5, 10, 15)]
    payload = {"status": "rh273_minimal_rank_pole_counterloop_uniqueness", "rows": rows,
               "noisy_spectral_identification": False, "gate_A": False}
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"rows": len(rows)}))


if __name__ == "__main__":
    main()
