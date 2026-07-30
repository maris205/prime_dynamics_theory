import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))
from dual_ledger import COUNTERLOOP_VECTOR, SPECTRAL_VECTOR, complete  # noqa: E402


def load(number: int) -> dict:
    matches = list(PAPERS.glob(f"RH-{number}-*/results/result.json"))
    if len(matches) != 1:
        raise RuntimeError(f"missing unique RH-{number} result")
    return json.loads(matches[0].read_text())


def main() -> None:
    sources = {str(number): load(number)["status"] for number in range(272, 280)}
    payload = {
        "status": "rh280_dual_counterloop_spectral_ledger",
        "source_statuses": sources,
        "spectral_vector": list(SPECTRAL_VECTOR),
        "counterloop_vector": list(COUNTERLOOP_VECTOR),
        "spectral_satisfied": sum(SPECTRAL_VECTOR),
        "counterloop_satisfied": sum(COUNTERLOOP_VECTOR),
        "spectral_complete": complete(SPECTRAL_VECTOR),
        "counterloop_complete": complete(COUNTERLOOP_VECTOR),
        "positive_noise_local_quotient": True,
        "small_noise_uniform_quotient": False,
        "complete_certificate_count": 0,
        "macro_gates": {letter: False for letter in "ABCDE"},
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"spectral": payload["spectral_satisfied"], "counterloop": payload["counterloop_satisfied"]}))


if __name__ == "__main__":
    main()
