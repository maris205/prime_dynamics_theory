"""Rigorous Schur-similarity tools for the stored complement pole count."""

from .certificate import (
    CircleClassification,
    SimilarityCertificate,
    classify_binary64_diagonal,
    combine_frobenius_bounds,
    sha256_array,
    similarity_certificate,
)

__all__ = [
    "CircleClassification",
    "SimilarityCertificate",
    "classify_binary64_diagonal",
    "combine_frobenius_bounds",
    "sha256_array",
    "similarity_certificate",
]
