import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))
from shell_transport import neumann_resolvent_bound, normalizer_lower  # noqa: E402


def main() -> None:
    audit = json.loads((PAPERS / "RH-259-extended-quotient-block-power-diagnostic/results/extended_quotient_audit.json").read_text())
    payload = {
        "status": "rh278_positive_noise_s2_analytic_shell_transport",
        "archived_interval": [0.00125, 0.04],
        "row_normalizer_lower_on_interval": normalizer_lower(0.04),
        "example_resolvent_bound_M10_delta0_04": neumann_resolvent_bound(10.0, 0.04),
        "finite_contractive_power_12_count": sum(row["quotient_power_12_operator_norm"] < 1 for row in audit["endpoint_rows"]),
        "finite_endpoint_count": len(audit["endpoint_rows"]),
        "positive_noise_local_package": True,
        "zero_noise_uniform_package": False,
        "gate_A": False,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"finite": payload["finite_endpoint_count"], "local": True}))


if __name__ == "__main__":
    main()
