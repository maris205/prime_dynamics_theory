"""Build the deterministic RH-353 result artifact."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from boundary_completion_gap import result_status  # noqa: E402


def result_payload() -> dict[str, object]:
    return result_status()


def main() -> None:
    output = ROOT / "results" / "result.json"
    output.write_text(
        json.dumps(result_payload(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
