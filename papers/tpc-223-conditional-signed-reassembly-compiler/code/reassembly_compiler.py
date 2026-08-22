#!/usr/bin/env python3
"""Exact rational exponent compiler for the TPC-223 conditional interface."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


STRICT_THRESHOLD = Fraction(1, 400)


@dataclass(frozen=True)
class Ledger:
    """The finite exponent data supplied to the conditional compiler."""

    baseline: Fraction
    ap_saving: Fraction
    polarized_saving: Fraction
    structural_loss: Fraction

    def __post_init__(self) -> None:
        for name in ("baseline", "ap_saving", "polarized_saving", "structural_loss"):
            value = getattr(self, name)
            if not isinstance(value, Fraction):
                raise TypeError(f"{name} must be a Fraction")
        if self.ap_saving < 0 or self.polarized_saving < 0:
            raise ValueError("channel savings must be nonnegative")
        if self.structural_loss < 0:
            raise ValueError("structural loss must be nonnegative")

    @property
    def weakest_channel_saving(self) -> Fraction:
        return min(self.ap_saving, self.polarized_saving)

    @property
    def effective_saving(self) -> Fraction:
        return self.weakest_channel_saving - self.structural_loss

    @property
    def ap_exponent(self) -> Fraction:
        return self.baseline - self.ap_saving

    @property
    def polarized_exponent(self) -> Fraction:
        return self.baseline - self.polarized_saving

    @property
    def compiled_exponent(self) -> Fraction:
        return max(self.ap_exponent, self.polarized_exponent) + self.structural_loss

    @property
    def target_exponent(self) -> Fraction:
        return self.baseline - STRICT_THRESHOLD

    @property
    def strict_margin(self) -> Fraction:
        return self.effective_saving - STRICT_THRESHOLD

    @property
    def status(self) -> str:
        if self.strict_margin > 0:
            return "STRICT_PASS"
        if self.strict_margin == 0:
            return "BORDERLINE"
        return "NO_STRICT_SAVING"

    def as_record(self, name: str, *, assumptions_declared: bool = True) -> dict[str, object]:
        """Return a JSON-safe record without converting claims into arithmetic facts."""

        return {
            "name": name,
            "baseline": str(self.baseline),
            "ap_saving": str(self.ap_saving),
            "polarized_saving": str(self.polarized_saving),
            "structural_loss": str(self.structural_loss),
            "ap_exponent": str(self.ap_exponent),
            "polarized_exponent": str(self.polarized_exponent),
            "compiled_exponent": str(self.compiled_exponent),
            "target_exponent": str(self.target_exponent),
            "weakest_channel_saving": str(self.weakest_channel_saving),
            "effective_saving": str(self.effective_saving),
            "strict_threshold": str(STRICT_THRESHOLD),
            "strict_margin": str(self.strict_margin),
            "status": self.status,
            "conditional_inputs": {
                "ap_dispersion": "CONDITIONAL_ASSUMPTION",
                "polarized_cross_correlation": "CONDITIONAL_ASSUMPTION",
                "literal_reassembly_interface": "CONDITIONAL_ASSUMPTION",
            },
            "assumptions_declared": assumptions_declared,
        }


def compile_ledger(
    baseline: Fraction,
    ap_saving: Fraction,
    polarized_saving: Fraction,
    structural_loss: Fraction,
) -> Ledger:
    """Construct one exact ledger; the theorem is conditional on its inputs."""

    return Ledger(baseline, ap_saving, polarized_saving, structural_loss)


def fraction(text: str) -> Fraction:
    """Parse the restricted rational format used by certificates."""

    return Fraction(text)


def compiler_identity_holds(ledger: Ledger) -> bool:
    """Check the max/min exponent identity used in the proof."""

    return ledger.compiled_exponent == ledger.baseline - ledger.effective_saving


def strict_gate_holds(ledger: Ledger) -> bool:
    """Return the strict, not weak, endpoint condition."""

    return ledger.effective_saving > STRICT_THRESHOLD


def canonical_ledgers() -> tuple[tuple[str, Ledger], ...]:
    """The release fixtures: strict, borderline, failed, and missing-channel cases."""

    return (
        (
            "strict_endpoint",
            compile_ledger(
                Fraction(5, 3), Fraction(1, 100), Fraction(1, 80), Fraction(1, 1200)
            ),
        ),
        (
            "borderline_endpoint",
            compile_ledger(
                Fraction(5, 3), Fraction(1, 400), Fraction(1, 400), Fraction(0)
            ),
        ),
        (
            "failed_endpoint",
            compile_ledger(
                Fraction(5, 3), Fraction(1, 500), Fraction(1, 400), Fraction(0)
            ),
        ),
        (
            "missing_polarized_saving",
            compile_ledger(
                Fraction(5, 3), Fraction(1, 100), Fraction(0), Fraction(1, 1200)
            ),
        ),
        (
            "loss_dominates",
            compile_ledger(
                Fraction(5, 3), Fraction(1, 100), Fraction(1, 80), Fraction(1, 100)
            ),
        ),
    )
