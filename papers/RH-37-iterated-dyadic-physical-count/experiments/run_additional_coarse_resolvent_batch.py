"""Run RH-36's audited A2048 center certifier into the RH-37 archive."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
sys.path.insert(0, str(RH36 / "experiments"))

import run_physical_resolvent_batch as inherited  # noqa: E402


if __name__ == "__main__":
    inherited.ROOT = ROOT
    inherited.main()
