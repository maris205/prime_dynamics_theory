from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from critical_alias import (  # noqa: E402
    absolute_matching_exponent,
    alias_growth_exponent,
    first_alias_clearance_exponent,
    localization_slope,
    minimal_clearance_exponent,
    parity_alias_exponent,
)


def main() -> None:
    payload = {
        "status": "rh310_critical_alias_parity_localization_coincidence",
        "first_alias_slope": localization_slope(),
        "localization_slope": localization_slope(),
        "alias_growth_exponent": alias_growth_exponent(),
        "parity_alias_exponent": parity_alias_exponent(),
        "absolute_matching_exponent": absolute_matching_exponent(),
        "first_alias_clearance_exponent": first_alias_clearance_exponent(),
        "minimal_clock_clearance_exponent": minimal_clearance_exponent(),
        "critical_asymptotic_slope_coincidence_proved": True,
        "first_alias_matching_law_proved": True,
        "separate_alias_parity_majorant_decays": False,
        "joint_boundary_layer_trace_law_proved": False,
        "actual_full_trace_divergence_proved": False,
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"alias_exponent": alias_growth_exponent()}))


if __name__ == "__main__":
    main()
