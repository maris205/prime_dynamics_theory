"""Build local and source-provenance manifests for Volume II."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    audit_path = ROOT / "results/volume_audit.json"
    audit = json.loads(audit_path.read_text())
    relatives = (
        ".gitignore", "Makefile", "README.md", "CROSSWALK.md",
        "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
        "experiments/build_volume_audit.py", "experiments/build_archive.py",
        "experiments/verify_archive.py", "tests/test_volume.py",
        "pyproject.toml", "requirements.txt", "main.pdf",
        "physical-riesz-cloud-trace-envelope-synthesis.pdf",
        "results/volume_audit.json",
        "results/atomic_index.tex",
    )
    paths = [ROOT / relative for relative in relatives]
    missing = [str(path.relative_to(ROOT)) for path in paths if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing required publication files: {missing}")
    dependency = {
        "status": "rh_volume_ii_sources_and_publication_artifacts_hashed",
        "external_inputs": audit["source_file_hashes"],
        "local_sources": {
            str(path.relative_to(ROOT)): sha(path)
            for path in paths
            if path.suffix in {".py", ".tex", ".md", ".toml", ".txt"}
            or path.name in {".gitignore", "Makefile"}
        },
        "publication_artifacts": {
            str(path.relative_to(ROOT)): sha(path)
            for path in paths
            if path.suffix == ".pdf" or path.name == "volume_audit.json"
        },
    }
    dependency_path = ROOT / "results/dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n")
    summary = {
        "status": "rh_volume_ii_physical_riesz_cloud_trace_envelope_archived",
        "series": audit["series"],
        "inventory": {
            "numbered_paper_count": audit["numbered_paper_count"],
            "review_anchor_count": len(audit["review_anchor_numbers"]),
            "source_file_hash_count": audit["source_file_hash_count"],
            "finite_review_item_total": audit["finite_review_item_total"],
        },
        "typed_assembly": audit["typed_assembly"],
        "fixed_order_trace_envelope_max_order": audit["fixed_order_trace_envelope_max_order"],
        "moving_noisy_all_order_trace_envelope_proved": audit["moving_noisy_all_order_trace_envelope_proved"],
        "no_over_extraction_coefficient_anchor_proved": audit["no_over_extraction_coefficient_anchor_proved"],
        "route_coordinate": audit["route_coordinate"],
        "gates": audit["gates"],
        "forbidden_claims": audit["forbidden_claims"],
        "result_hashes": {
            "results/volume_audit.json": sha(audit_path),
            "results/dependency_manifest.json": sha(dependency_path),
        },
    }
    (ROOT / "results/summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({"status": summary["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
