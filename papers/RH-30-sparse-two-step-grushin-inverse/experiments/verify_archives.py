"""Strictly parse and cross-check the archived RH-30 result files."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def strict_json(path: Path) -> dict[str, object]:
    def reject(value: str):
        raise ValueError(f"non-finite JSON constant {value} in {path}")

    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    json_paths = sorted(RESULTS.glob("*.json"))
    parsed = {path.name: strict_json(path) for path in json_paths}
    canonical_names = (
        "stored_inverse_certificate_sigma_1e-2.json",
        "stored_inverse_certificate_sigma_4e-3.json",
    )
    checks = []
    current_source_hash = sha256(
        ROOT / "experiments" / "run_stored_inverse_certificate.py"
    )
    for name in canonical_names:
        data = parsed[name]
        checks.append(
            {
                "file": name,
                "status_is_closure": data["status"]
                == "rigorous_selected_arc_stored_model_closure",
                "residual_is_neumann_admissible": float(
                    data["residual_frobenius_upper"]
                )
                < 1.0,
                "lifted_budget_closes": float(data["lifted_inverse_two_norm_upper"])
                < float(data["lifted_inverse_budget_lower"]),
                "selected_arc_budget_closes": float(
                    data["selected_arc_inverse_two_norm_upper"]
                )
                < float(data["rh28_selected_arc_resolvent_budget_lower"]),
                "certificate_source_hash_matches": data["source_sha256"][
                    "run_stored_inverse_certificate.py"
                ]
                == current_source_hash,
            }
        )
    coarse = parsed["stored_inverse_certificate_sigma_1e-2.json"]
    crosscheck = parsed["stored_inverse_certificate_sigma_1e-2_chunk128.json"]
    chunk_difference = abs(
        float(coarse["lifted_inverse_two_norm_upper"])
        - float(crosscheck["lifted_inverse_two_norm_upper"])
    )
    all_passed = all(
        all(value for key, value in row.items() if key != "file") for row in checks
    ) and chunk_difference < 1.0e-7
    payload = {
        "status": "all_archives_verified" if all_passed else "archive_check_failed",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "strict_json_file_count": len(json_paths),
        "checks": checks,
        "coarse_chunking_lifted_bound_absolute_difference": chunk_difference,
        "coarse_chunking_tolerance": 1.0e-7,
        "manuscript_pdf_sha256": (
            sha256(ROOT / "sparse-two-step-grushin-inverse.pdf")
            if (ROOT / "sparse-two-step-grushin-inverse.pdf").exists()
            else None
        ),
    }
    if not all_passed:
        raise RuntimeError(json.dumps(payload, indent=2, sort_keys=True))
    output = RESULTS / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
