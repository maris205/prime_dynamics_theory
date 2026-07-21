"""Flag-adapted Schur--Stein metric algebra for RH-59."""

from .algebra import (
    FlagMetricFamily,
    LocalLyapunovBlock,
    PacketSteinCertificate,
    block_slices,
    build_flag_metric,
    comparison_contraction_log_upper,
    evaluate_packet_certificate,
    packet_log_upper_objective,
    scaled_comparison_prefix,
    scaled_normalized_prefix,
)

__all__ = [
    "FlagMetricFamily",
    "LocalLyapunovBlock",
    "PacketSteinCertificate",
    "block_slices",
    "build_flag_metric",
    "comparison_contraction_log_upper",
    "evaluate_packet_certificate",
    "packet_log_upper_objective",
    "scaled_comparison_prefix",
    "scaled_normalized_prefix",
]
