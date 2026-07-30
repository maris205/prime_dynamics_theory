from __future__ import annotations


def batch_status() -> dict[str, object]:
    spectral = (True, False, True, True, True)
    counterloop = (True, True, False, True, True)
    return {
        "spectral_ledger": spectral,
        "counterloop_ledger": counterloop,
        "spectral_score": sum(spectral),
        "counterloop_score": sum(counterloop),
        "complete_count": int(all(spectral)) + int(all(counterloop)),
        "weighted_cross_branch_glue": False,
        "gates": {letter: False for letter in "ABCDE"},
    }
