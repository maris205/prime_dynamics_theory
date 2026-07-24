from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from controlled_viability import controlled_support_floor, directional_candidate  # noqa: E402


LAYERS = [
    {
        "number": 130, "directory": "RH-130-floor-free-semidefinite-directional-audit", "kind": "mixed",
        "result": "Floor-free semidefinite rank-four reconstruction and exact-Gram minimax.",
        "finite": "118/120 positive snapshots, 67/96 positive transfers, 0/24 complete chains.",
        "obstruction": "24 rank births and five further superunit transfers block naive composition.",
    },
    {
        "number": 131, "directory": "RH-131-singular-gram-support-rayleigh-theory", "kind": "constructive",
        "result": "Kernel compatibility, Moore--Penrose Rayleigh quotient, and sharp pseudovolume law.",
        "finite": "5,120 random/support tests with zero failures; rank births classified exactly.",
        "obstruction": "Kernel leakage makes the full-space quotient infinite.",
    },
    {
        "number": 132, "directory": "RH-132-canonical-partial-isometry-forcing-gauge", "kind": "constructive",
        "result": "Canonical polar partial isometry and trace-minimal positive forcing.",
        "finite": "4,096-case audit with zero failures; 22/24 birth strengths are subunit.",
        "obstruction": "Unmatched target range forces a nonzero additive term.",
    },
    {
        "number": 133, "directory": "RH-133-dyadic-packet-transport-gauge", "kind": "mixed",
        "result": "Model-derived dyadic packet gauge and exact-Gram lift.",
        "finite": "65 positive natural transfers versus 67 post-hoc optimal transfers.",
        "obstruction": "Principal angles alone do not control tail amplification; median loss is about 74-fold.",
    },
    {
        "number": 134, "directory": "RH-134-moving-frame-memory-tail-recurrence", "kind": "constructive",
        "result": "Exact memory-tail birth identity and moving-frame affine recurrence.",
        "finite": "330 transitions with zero identity/Loewner failures; raw old-tail factor below 0.003914.",
        "obstruction": "Boundary birth, not frame forcing, dominates every nonzero forcing update.",
    },
    {
        "number": 135, "directory": "RH-135-relative-metric-affine-tail-recurrence", "kind": "mixed",
        "result": "Sharp relative-metric coefficients and optimized affine fixed floor.",
        "finite": "Only 51/216 recurrent polar-gauge transitions are contractive.",
        "obstruction": "Target Gram amplification reaches 10^16.326 and defeats raw decay.",
    },
    {
        "number": 136, "directory": "RH-136-metric-balanced-packet-gauge", "kind": "constructive",
        "result": "Exact orthogonal metric minimax and contractivity-complete finite gauge family.",
        "finite": "183/216 transitions recovered; 132 more than polar, with all fixed floors subunit.",
        "obstruction": "33 transitions are noncontractive for every orthogonal gauge.",
    },
    {
        "number": 137, "directory": "RH-137-finite-horizon-young-tail-envelope", "kind": "constructive",
        "result": "Pointwise-optimal Young envelope and greedy finite-horizon control.",
        "finite": "31/33 long-run walls crossed; 328/330 transitions and 28/30 chains are safe.",
        "obstruction": "Two coarse target birth terms are already superunit.",
    },
    {
        "number": 138, "directory": "RH-138-outward-finite-directional-composition", "kind": "constructive",
        "result": "Two outward Loewner residuals and a normalized-base support certificate.",
        "finite": "All 330 residual pairs certify; 328 positive transitions and 28 positive chains.",
        "obstruction": "fp64 norm balls lose ten weak base directions; source-model intervals remain absent.",
    },
]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_layers(limit: int | None = None) -> list[dict[str, object]]:
    output = []
    for metadata in LAYERS[:limit]:
        directory = PAPERS / metadata["directory"]
        summary_path = directory / "results" / "summary.json"
        verification_path = directory / "results" / "archive_verification.json"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        verification = json.loads(verification_path.read_text(encoding="utf-8"))
        forbidden = {
            key: value for key, value in summary.get("program_boundary", {}).items()
            if key in {"riemann_hypothesis", "hilbert_polya_operator", "uniform_stage_A_closed"}
        }
        output.append({
            **metadata,
            "archive_status": summary["status"],
            "archive_verified": "verified" in verification["status"],
            "summary_sha256": sha(summary_path),
            "theorem_count": sum(bool(value) for value in summary.get("theorem", {}).values()),
            "forbidden_claim_values": forbidden,
            "audit": summary.get("audit", {}),
        })
    return output


def viability_audit(smoke: bool) -> dict[str, object]:
    rng = np.random.default_rng(139)
    sample_count = 128 if smoke else 4096
    failures = 0
    minimum_margin = float("inf")
    for _ in range(sample_count):
        tail_upper = float(rng.uniform(0.0, 0.98))
        base_lower = float(10.0 ** rng.uniform(-8.0, -0.1))
        floor = controlled_support_floor(tail_upper, base_lower)
        tails = rng.uniform(0.0, tail_upper, size=32)
        bases = base_lower * (1.0 + rng.random(32) * 9.0)
        margin = min(directional_candidate(x, a) for x, a in zip(tails, bases)) - floor
        minimum_margin = min(minimum_margin, margin)
        failures += margin < -1e-14
    n = np.arange(2.0, 4098.0)
    tail_obstruction = np.min((1.0 - np.sqrt((1.0 - 1.0 / n) ** 2)) ** 4)
    base_obstruction = np.min(1.0 / n)
    return {
        "sample_count": sample_count,
        "viability_floor_failure_count": failures,
        "minimum_viability_margin": minimum_margin,
        "tail_gap_obstruction_terminal": float(tail_obstruction),
        "base_liminf_obstruction_terminal": float(base_obstruction),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    layers = load_layers(3 if args.smoke else None)
    viability = viability_audit(args.smoke)
    forbidden_failures = sum(
        bool(value) for layer in layers for value in layer["forbidden_claim_values"].values()
    )
    archive_failures = sum(not layer["archive_verified"] for layer in layers)
    summary = {
        "reviewed_upstream_layer_count": len(layers),
        "total_layer_count_including_review": len(layers) + 1,
        "constructive_layer_count": sum(layer["kind"] == "constructive" for layer in layers) + (0 if args.smoke else 1),
        "mixed_layer_count": sum(layer["kind"] == "mixed" for layer in layers),
        "archive_verification_failure_count": archive_failures,
        "forbidden_claim_failure_count": forbidden_failures,
        **viability,
        "floor_free_complete_chain_count": layers[0]["audit"].get("positive_chain_count") if layers else None,
        "metric_balanced_contractive_count": next((layer["audit"].get("balanced_contractive_feasible_count") for layer in layers if layer["number"] == 136), None),
        "finite_safe_chain_count": next((layer["audit"].get("greedy_safe_chain_count") for layer in layers if layer["number"] == 137), None),
        "outward_positive_chain_count": next((layer["audit"].get("positive_support_chain_count") for layer in layers if layer["number"] == 138), None),
    }
    payload = {
        "status": "rh139_ten_layer_controlled_viability_review",
        "layers": layers, "audit_summary": summary,
        "revised_frontier": {
            "mathematical_exact_matrix_frontier": [
                "eventual_uniform_controlled_tail_gap",
                "positive_normalized_base_liminf",
            ],
            "validated_common_assembly_addition": ["source_model_exact_or_interval_enclosure"],
            "independent_assembly_addition": ["all_level_outward_radii_and_residual_guards"],
            "removed_as_unnecessary": ["subunit_affine_coefficient_at_every_step"],
        },
        "theorem_boundary": {
            "controlled_viability_eventual_support_theorem": True,
            "tail_gap_and_base_liminf_architecture_sharp": True,
            "ten_layer_archive_reviewed": not args.smoke,
            "eventual_uniform_tail_gap_proved_for_model": False,
            "positive_normalized_base_liminf_proved_for_model": False,
            "source_model_interval_enclosure_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "RH-130--RH-138 replace the old per-step contraction obligation by a weaker controlled-viability packet: an eventual uniform subunit envelope is enough even when isolated metric bases exceed one. Within the directional candidate architecture, this tail gap and a positive normalized-base liminf are both sharp and irreducible. The finite reference route is now outwardly closed on 28/30 chains; the all-level frontier is source enclosure, controlled viability, and base liminf, with all-level outward radii added for independent assemblies.",
    }
    name = "ten_layer_review_smoke.json" if args.smoke else "ten_layer_review.json"
    output = ROOT / "results" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
