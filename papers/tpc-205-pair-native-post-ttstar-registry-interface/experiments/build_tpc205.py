#!/usr/bin/env python3
"""Materialize or primary-check the finite TPC-205 interface artifacts."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "tpc205_pair_native_registry_interface.py"


def load_contract():
    spec = importlib.util.spec_from_file_location(
        "tpc205_materialization_contract", CONTRACT
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to import the TPC-205 materialization contract")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if not __debug__:
        raise RuntimeError(
            "optimized Python disables assertions in imported upstream code; "
            "TPC-205 materialization fails closed"
        )
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    contract = load_contract()
    if not args.check:
        contract.materialize()
    result = contract.verify_active_artifacts()
    manifest = contract.verify_manifest() if args.check else None
    print(
        json.dumps(
            {
                "paper": 205,
                "materialized": not args.check,
                "check": True,
                "verdict": contract.VERDICT,
                "certificate": result,
                "manifest": manifest,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
