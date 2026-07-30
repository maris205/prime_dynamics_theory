import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from variable_block import block_tail_bound  # noqa: E402


def main() -> None:
    rows = []
    for m in (4, 8, 16, 32, 64):
        rows.append({"m_sigma": m, "tail_R_0_8": block_tail_bound(m, 0.8, 1.0, 0.7**m, 1.1)})
    payload = {"status": "rh279_variable_rank_block_power_tail_criterion", "rows": rows,
               "uniform_variable_rank_certificate": False, "gate_A": False}
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"rows": len(rows)}))


if __name__ == "__main__":
    main()
