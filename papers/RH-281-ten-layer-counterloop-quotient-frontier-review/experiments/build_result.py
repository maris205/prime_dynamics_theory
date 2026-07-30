import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))
from frontier_review import PAPER_NUMBERS, counterloop_vector, spectral_vector  # noqa: E402


def main() -> None:
    rows = []
    for number in PAPER_NUMBERS[:-1]:
        matches = list(PAPERS.glob(f"RH-{number}-*/results/result.json"))
        rows.append({"number": number, "result_present": len(matches) == 1})
    payload = {
        "status": "rh281_ten_layer_counterloop_quotient_frontier_review",
        "paper_numbers": list(PAPER_NUMBERS), "rows": rows,
        "spectral_obligation_vector": list(spectral_vector()),
        "counterloop_obligation_vector": list(counterloop_vector()),
        "spectral_complete_count": 0, "counterloop_complete_count": 0,
        "macro_gates": {letter: False for letter in "ABCDE"},
        "hilbert_polya_operator": False, "riemann_zero_identification": False,
        "zeta_divisor_equality": False, "rh_implication": False,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"rows": len(rows), "all_present": all(row["result_present"] for row in rows)}))


if __name__ == "__main__":
    main()
