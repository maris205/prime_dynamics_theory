"""Arb-backed norm intervals for exact stored binary64 vectors."""

from __future__ import annotations

import numpy as np
from flint import arb, ctx

from .algebra import NormInterval


def arb_vector_norm_interval(values: np.ndarray, *, precision: int = 160) -> NormInterval:
    """Enclose the exact Euclidean norm of a stored real or complex vector."""

    vector = np.asarray(values).reshape(-1)
    previous = ctx.prec
    ctx.prec = int(precision)
    try:
        total = arb(0)
        if np.iscomplexobj(vector):
            for value in vector:
                real = arb(float(np.real(value)))
                imag = arb(float(np.imag(value)))
                total += real * real + imag * imag
        else:
            for value in vector:
                scalar = arb(float(value))
                total += scalar * scalar
        norm = total.sqrt()
        lower = float(np.nextafter(float(norm.lower()), -np.inf))
        upper = float(np.nextafter(float(norm.upper()), np.inf))
    finally:
        ctx.prec = previous
    return NormInterval(lower=lower, upper=upper)
