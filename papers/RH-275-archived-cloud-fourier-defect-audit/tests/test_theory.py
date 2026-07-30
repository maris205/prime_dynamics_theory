from pathlib import Path
from cloud_audit import audit_csv


def test_archived_rows_and_metrics():
    root = Path(__file__).resolve().parents[2]
    rows = audit_csv(root / "RH-15-parity-extracted-bulk-scattering/results/outer_resonance_cloud.csv")
    assert len(rows) == 7
    assert [row["N"] for row in rows] == [3, 3, 4, 5, 5, 6, 7]
    assert min(row["N_times_mean_root_error"] for row in rows) > 0.3
