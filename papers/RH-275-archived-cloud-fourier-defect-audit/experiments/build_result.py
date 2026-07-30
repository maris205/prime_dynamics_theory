import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))
from cloud_audit import audit_csv  # noqa: E402


def main() -> None:
    source = PAPERS / "RH-15-parity-extracted-bulk-scattering/results/outer_resonance_cloud.csv"
    rows = audit_csv(source)
    payload = {
        "status": "rh275_archived_cloud_fourier_defect_audit",
        "source": str(source.relative_to(PAPERS)), "row_count": len(rows), "rows": rows,
        "minimum_N_times_mean_root_error": min(r["N_times_mean_root_error"] for r in rows),
        "maximum_N_times_mean_root_error": max(r["N_times_mean_root_error"] for r in rows),
        "minimum_maximum_moment_error": min(r["maximum_pre_alias_moment_error"] for r in rows),
        "maximum_maximum_moment_error": max(r["maximum_pre_alias_moment_error"] for r in rows),
        "asymptotic_nonconvergence_proved": False,
        "upstream_interval_certified": False,
        "gate_A": False,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"rows": len(rows), "min_scaled_error": payload["minimum_N_times_mean_root_error"]}))


if __name__ == "__main__":
    main()
