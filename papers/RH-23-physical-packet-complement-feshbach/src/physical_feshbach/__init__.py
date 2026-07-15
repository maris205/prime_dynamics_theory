"""Exact packet/complement block algebra for physical spectral targets."""

from .algebra import (
    DenseFeshbachData,
    EigenmodeClosure,
    dense_feshbach_data,
    eigenmode_closure,
    external_project,
    packet_project,
    reduced_matrix,
)
from .packets import (
    bright_history_trial,
    critical_bright_trial,
    label_resolved_trial,
    single_label_trial,
)

__all__ = [
    "DenseFeshbachData",
    "EigenmodeClosure",
    "bright_history_trial",
    "critical_bright_trial",
    "dense_feshbach_data",
    "eigenmode_closure",
    "external_project",
    "label_resolved_trial",
    "packet_project",
    "reduced_matrix",
    "single_label_trial",
]
