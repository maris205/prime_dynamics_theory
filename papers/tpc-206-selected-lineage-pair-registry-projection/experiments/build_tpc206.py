#!/usr/bin/env python3
"""Thin fail-closed wrapper for the TPC-206 materialization contract."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "tpc206_selected_lineage_pair_registry.py"


def load_contract():
    spec = importlib.util.spec_from_file_location("tpc206_contract", CONTRACT)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to import TPC-206 contract")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if not __debug__:
        raise RuntimeError("TPC-206 builder fails closed under optimized Python")
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
                "paper": 206,
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
