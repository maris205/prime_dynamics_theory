#!/usr/bin/env python3
"""Materialize or primary-check the TPC-204 finite crosswalk artifacts.

The authoritative materialization contract lives in the adjacent module.
The separately shipped ``tpc204_independent_checker.py`` imports neither this
builder nor that module and supplies the common-mode check.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKER = HERE / "tpc204_source_locked_production_registry_crosswalk.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("tpc204_materialization_contract", CHECKER)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to import the TPC-204 materialization contract")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if not __debug__:
        raise RuntimeError(
            "optimized Python disables assertions in imported upstream code; "
            "TPC-204 materialization fails closed"
        )
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    checker = load_checker()
    if not args.check:
        checker.materialize()
    result = checker.verify_active_artifacts()
    print(
        json.dumps(
            {
                "paper": 204,
                "materialized": not args.check,
                "check": True,
                "verdict": "FIRST_MISMATCH_CERTIFIED_NOT_TESTABLE",
                "certificate": result,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
