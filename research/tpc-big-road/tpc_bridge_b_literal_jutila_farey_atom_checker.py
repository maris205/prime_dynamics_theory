#!/usr/bin/env python3
"""Read-only exact checker for the TPC Bridge-B V24 atom compiler."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Callable, Iterable


sys.dont_write_bytecode = True


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


ROOT = Path(__file__).resolve().parents[2]
V19_PATH = ROOT / "research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py"
V19_CANONICAL_SHA256 = "e572bd9157ce4e733dc411ed8eb29df90d34be0ecf17023186f1648389ded519"
V23_PATH = ROOT / "research/tpc-big-road/tpc_bridge_b_prime_shell_jutila_checker.py"
V23_CANONICAL_SHA256 = "29ebf909a5c0c4209aba5ddb6eb76a3b91832a613578dadc6589272b855beb19"


CONTRACT = {
    "route_version": "BOLD_CHANNEL_V24",
    "artifact_status": "UNNUMBERED_WORKING_ARTIFACT",
    "literal_atomization_gate": "V24_LITERAL_DETERMINANT_JUTILA_FAREY_ATOMIZATION=PROVED_EXACT_L0",
    "lemma1_jutila_gate": "V24_BLOMER_LI_LEMMA1_JUTILA_INTERFACE=PROVED_SOURCE_BACKED",
    "claim_ceiling": "EXACT_L0_LITERAL_DETERMINANT_TO_JUTILA_MAIN_AND_FAREY_KLOOSTERMAN_ATOMIZATION_WITH_SOURCE_TRANSFER_FIREWALLS",
    "physical_h0": 2,
    "analytic_physical_binding": "x=2X",
    "physical_shell": "STRICT_x_OVER_2_LT_t_LE_x",
    "raw_row": "V19_COMBINED_RAW_MASTER_PLUS2_MINUS1",
    "residual": "LAMBDA_SHIFT2_MINUS_TENSOR_LOCAL_B",
    "determinant_prime_branch": "D=d_phys*r-T_occurrence-2",
    "channel_policy": "PRIME_AND_HYBRID_SEPARATE_EXACT",
    "outer_absolute_value": "ONCE_OUTSIDE_COMPLETE_REASSEMBLY",
    "exactly_once_cover": "ALL_LITERAL_OCCURRENCES_WITH_ORIGINAL_MULTIPLICITY",
    "typed_alphabet": "d_phys__q_J__d_J__c_F__b_F__u_F__t_F__ell_J__d_BL_ALL_DISTINCT",
    "jutila_source": "BLOMER_LI_2511_03294V1_SECTION_2_1_LEMMA_1",
    "jutila_qmes": "x_POWER_1_OVER_3",
    "jutila_qsrc": "2_QMES",
    "jutila_omega": "PRIME_QMES_LT_q_LE_2QMES",
    "jutila_L": "SUM_PHI_q_EQUALS_SUM_q_MINUS_1",
    "jutila_psi": "RANGE_0_1_SUPPORT_MINUS1_1_INTEGRAL1",
    "jutila_eta": "1/32",
    "jutila_delta": "QMES_POWER_MINUS_63_OVER_32_EQUALS_x_POWER_MINUS_21_OVER_32",
    "jutila_split": "EXACT_MAIN_PLUS_EXPLICIT_ERROR_BY_ONE_EQUALS_CHI_PLUS_ONE_MINUS_CHI",
    "jutila_is_exact_delta": False,
    "farey_source": "BLOMER_LI_2511_03294V1_PRINTED_MAX_FIXED_PLUS_REPAIRED_FROM_FAREY_GEOMETRY",
    "farey_level": "ALL_INTEGERS_1_LE_c_LE_C_NOT_PRIME_ONLY",
    "farey_arc": "ABS_z_LE_1_OVER_cC_WITH_EXACT_NEIGHBORS",
    "farey_interval": "OPEN_C_MINUS_c_CLOSED_MIN_1_OVER_cABSz_MINUS_c_COMMA_C_INTEGER",
    "farey_additive_sign": "CORRECTED_e_c_u_t_TIMES_e_c_SIGN_z_u_b_inverse",
    "farey_printed_formula": "V24_BLOMER_LI_LEMMA2_AS_PRINTED_MAX_FIXED_PLUS=STOP_SCOPED_LITERAL_FAREY_COUNTEREXAMPLES",
    "farey_corrected_identity": "V24_CORRECTED_SIGNED_FAREY_IDENTITY=PROVED_EXACT_L0_REPOSITORY_DERIVATION",
    "dependency_lock": "LITERAL_PATH_AND_CANONICAL_HASH",
    "rational_chi_first_line": "d_J_MU_q_OVER_d_J_HATPSI_DELTA_d_J_ell",
    "rational_chi_second_line": "MU_q_OVER_d_J_ell_CONGRUENT_b_d_J_MOD_c_PSI_ell_OVER_c_d_J_PLUS_z",
    "eq2_2_second_line_q_factor": "ABSENT",
    "prime_dj_branches": "d_J_1_SIGN_MINUS__d_J_q_SIGN_PLUS_INSIDE_CHI",
    "identity_kloosterman": "V24_BARE_FAREY_B_SUM_TO_COMPLETE_KLOOSTERMAN_BILINEAR=PROVED_EXACT_L0__S_D_SIGN_z_u_MOD_c",
    "signed_qcb_atom": "IDENTITY_MINUS_CHI_BEFORE_ANY_OUTER_ABSOLUTE",
    "bl_theorem_object": "GL3_HECKE_A_n_1_TIMES_DIVISOR_TAU",
    "bl_factorable_weight": "q_EQUALS_p_t__p_PRIME__t_UNRESTRICTED_SMOOTH",
    "bl_t_domain": "NATURAL_t_WITH_RHO_t_OVER_Q2_NOT_PRIME_RESTRICTED",
    "bl_poisson_requirement": "NO_ARITHMETIC_CONDITION_ON_t",
    "bl_native_clock": "Q1_x4_21_Q2_x8_21_Q_x4_7_C0_x19_42_C_x23_42_DELTA_x_MINUS1",
    "v24_prime_clock": "QMES_x1_3_DELTA_x_MINUS21_32",
    "bl_s2_at_v24_clock": "FIRST_TERM_AT_LEAST_x7_6_STOP",
    "direct_bl_transfer": "V24_DIRECT_BLOMER_LI_GL3_DIVISOR_TO_LITERAL_TPC_TRANSFER=STOP_SCOPED_COEFFICIENT_VORONOI_CLOCK_AND_REASSEMBLY_MISMATCH",
    "prime_only_factorability_splice": "V24_PRIME_ONLY_JUTILA_SHELL_AS_BLOMER_LI_FACTORIZABLE_WEIGHT=STOP_SCOPED_UNRESTRICTED_SMOOTH_t_REQUIRED_FOR_POISSON",
    "bp_relation": "LOCAL_d_phys_EQUALS_q_DOUBLE_POISSON_ONLY_NOT_BL_SIGMA",
    "signed_qcb_gate": "V24_SIGNED_q_c_b_COLLECTIVE_PHYSICAL_EMITTER=OPEN_NEW_CONSTRUCTION",
    "error_theorem_gate": "V24_PRIME_SHELL_JUTILA_ERROR_SIGNED_FAREY_KLOOSTERMAN_THEOREM=OPEN_NEW_THEOREM",
    "main_to_bp_gate": "V24_PRIME_SHELL_JUTILA_MAIN_TO_BP_COLLECTIVE_EMITTER=OPEN_NEW_THEOREM",
    "factorable_aux_gate": "V24_FACTORIZABLE_AUXILIARY_JUTILA_ENSEMBLE_WITH_LITERAL_PHYSICAL_REASSEMBLY=OPEN_NEW_CONSTRUCTION",
    "arithmetic_advance": False,
    "fixed_atom_credit": 0,
    "strict_1_over_400": "UNPAID",
    "L2": "NONE",
    "TPC_207_TRIGGER": False,
}


REGISTRY_ITEMS = (
    ("MAXIMUM_CLAIM", "EXACT_L0_LITERAL_DETERMINANT_JUTILA_FAREY_KLOOSTERMAN_ATOMIZATION_AND_SOURCE_TRANSFER_FIREWALL"),
    ("LITERAL_ATOMIZATION_GATE", "V24_LITERAL_DETERMINANT_JUTILA_FAREY_ATOMIZATION=PROVED_EXACT_L0"),
    ("LEMMA1_JUTILA_GATE", "V24_BLOMER_LI_LEMMA1_JUTILA_INTERFACE=PROVED_SOURCE_BACKED"),
    ("PHYSICAL_H0", "2"),
    ("PHYSICAL_X", "x_EQUALS_2X"),
    ("PHYSICAL_SHELL", "STRICT_x_OVER_2_LT_t_LE_x"),
    ("PHYSICAL_RAW_ROW", "V19_COMBINED_RAW_MASTER_PLUS2_MINUS1"),
    ("PHYSICAL_RESIDUAL", "LAMBDA_SHIFT2_MINUS_TENSOR_LOCAL_B"),
    ("PHYSICAL_DETERMINANT", "d_phys_r_MINUS_T_occurrence_MINUS_2"),
    ("PHYSICAL_CHANNELS", "PRIME_AND_HYBRID_SEPARATE"),
    ("OUTER_ABSOLUTE", "ONCE_AFTER_COMPLETE_SIGNED_REASSEMBLY"),
    ("EXACTLY_ONCE_COVER", "ORIGINAL_OCCURRENCE_MULTIPLICITY"),
    ("VARIABLE_TYPE_FIREWALL", "d_phys_q_J_d_J_c_F_b_F_u_F_t_F_ell_J_d_BL_DISTINCT"),
    ("JUTILA_SOURCE", "BLOMER_LI_V1_SECTION_2_1_LEMMA_1"),
    ("JUTILA_QMES", "x_POWER_1_OVER_3"),
    ("JUTILA_QSRC", "2_QMES"),
    ("JUTILA_WEIGHT", "PRIME_SHELL_INDICATOR"),
    ("JUTILA_L", "SUM_q_MINUS_1"),
    ("JUTILA_PSI", "RANGE_0_1_SUPPORT_MINUS1_1_INTEGRAL1"),
    ("JUTILA_DELTA", "QMES_MINUS63_OVER32_EQUALS_x_MINUS21_OVER32"),
    ("JUTILA_SPLIT", "EXACT_MAIN_PLUS_EXPLICIT_ERROR"),
    ("JUTILA_MAIN_ATOM", "q_a_z_WITH_1_OVER_DELTA_L"),
    ("FAREY_SOURCE", "BLOMER_LI_V1_PRINTED_LEMMA2_REPAIRED_FROM_FAREY_PARTITION"),
    ("FAREY_LEVEL", "COMPLETE_c_LE_C_NOT_PRIME_ONLY"),
    ("FAREY_ARC", "ABS_z_LE_1_OVER_cC"),
    ("FAREY_INTERVAL_I", "C_MINUS_c_TO_MIN_1_OVER_cABSz_MINUS_c_COMMA_C"),
    ("FAREY_ADDITIVE_ATOM", "c_inverse_e_c_ut_e_c_SIGN_z_u_b_inverse"),
    ("FAREY_PRINTED_LEMMA2", "V24_BLOMER_LI_LEMMA2_AS_PRINTED_MAX_FIXED_PLUS=STOP_SCOPED_LITERAL_FAREY_COUNTEREXAMPLES"),
    ("FAREY_CORRECTED_IDENTITY", "V24_CORRECTED_SIGNED_FAREY_IDENTITY=PROVED_EXACT_L0_REPOSITORY_DERIVATION"),
    ("FAREY_IDENTITY_KLOOSTERMAN", "V24_BARE_FAREY_B_SUM_TO_COMPLETE_KLOOSTERMAN_BILINEAR=PROVED_EXACT_L0__S_D_SIGN_z_u_c"),
    ("CHI_RATIONAL_FIRST_LINE", "d_J_MU_q_OVER_d_J_HATPSI"),
    ("CHI_RATIONAL_SECOND_LINE", "MU_q_OVER_d_J_CONGRUENCE_AND_PSI"),
    ("CHI_SECOND_LINE_Q_FACTOR", "ABSENT"),
    ("PRIME_DJ_BRANCHES", "dJ1_MINUS__dJq_PLUS_INSIDE_CHI"),
    ("SIGNED_QCB_ATOM", "IDENTITY_MINUS_CHI_COLLECTIVE_BEFORE_ABSOLUTE"),
    ("BL_DIRECT_SOURCE_OBJECT", "GL3_A_n_1_TIMES_TAU_m"),
    ("BL_FACTORIZABLE_WEIGHT", "q_EQUALS_p_t_WITH_SMOOTH_UNRESTRICTED_t"),
    ("BL_T_RESTRICTION", "PRIME_t_FORBIDDEN_BEFORE_POISSON"),
    ("BL_NATIVE_CHARACTER_SUM", "SIGMA_h_d_n1_n2_c_ONE_DIMENSIONAL_GL3_VORONOI_SUM"),
    ("BL_NATIVE_CHARACTER_BOUND", "c_POWER_1_PLUS_EPS_c2_HALF_SQRT_GCD_OVER_n1"),
    ("BL_NATIVE_CLOCK", "Q_x4_7_DELTA_x_MINUS1_C0_x19_42_C_x23_42"),
    ("V24_PRIME_CLOCK", "Q_x1_3_DELTA_x_MINUS21_32"),
    ("BL_S2_AT_V24_CLOCK", "FIRST_TERM_x7_OVER6_NOT_SAVING"),
    ("DIRECT_BL_TRANSFER", "V24_DIRECT_BLOMER_LI_GL3_DIVISOR_TO_LITERAL_TPC_TRANSFER=STOP_SCOPED_COEFFICIENT_VORONOI_CLOCK_AND_REASSEMBLY_MISMATCH"),
    ("PRIME_ONLY_FACTORIZABILITY_SPLICE", "V24_PRIME_ONLY_JUTILA_SHELL_AS_BLOMER_LI_FACTORIZABLE_WEIGHT=STOP_SCOPED_UNRESTRICTED_SMOOTH_t_REQUIRED_FOR_POISSON"),
    ("BP_LOCAL_RELATION", "d_phys_EQUALS_q_LOCAL_ISLAND_ONLY_NOT_BL_SIGMA"),
    ("SIGNED_QCB_COLLECTIVE_EMITTER", "V24_SIGNED_q_c_b_COLLECTIVE_PHYSICAL_EMITTER=OPEN_NEW_CONSTRUCTION"),
    ("ERROR_SIGNED_FAREY_KLOOSTERMAN_THEOREM", "V24_PRIME_SHELL_JUTILA_ERROR_SIGNED_FAREY_KLOOSTERMAN_THEOREM=OPEN_NEW_THEOREM"),
    ("MAIN_TO_BP_COLLECTIVE_EMITTER", "V24_PRIME_SHELL_JUTILA_MAIN_TO_BP_COLLECTIVE_EMITTER=OPEN_NEW_THEOREM"),
    ("FACTORIZABLE_AUXILIARY_ENSEMBLE", "V24_FACTORIZABLE_AUXILIARY_JUTILA_ENSEMBLE_WITH_LITERAL_PHYSICAL_REASSEMBLY=OPEN_NEW_CONSTRUCTION"),
    ("REQUIRED_BRANCH_REGISTRY", "ZERO_NONUNIT_ELL0_ELLNONZERO_MAJOR_MINOR_PRIME_HYBRID_AXES_TAILS"),
    ("REQUIRED_LOSS_LEDGER", "ONE_OVER_L_ONE_OVER_DELTA_SMOOTH_DUAL_TAIL_OUTER"),
    ("REQUIRED_REASSEMBLY", "ONE_OUTER_ABSOLUTE_EXACTLY_ONCE"),
    ("DEPENDENCY_PATH_LOCK", "LITERAL_V19_AND_V23_PATHS_WITH_CANONICAL_HASHES"),
    ("RELEASE_BOUNDARY", "ARITHMETIC_NO_FIXED_ATOM0_STRICT_UNPAID_L2_NONE_TPC207_FALSE"),
)


EXPECTED_REGISTRY_SHA256 = "6ce7f2c3d2eb3a2e30900aaa7285d8e99bca139711db04915bdd9453a0a1808e"


def canonical_lf_bytes(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_lf_hash(path: Path) -> str:
    return hashlib.sha256(canonical_lf_bytes(path.read_bytes())).hexdigest()


def registry_hash(items: Iterable[tuple[str, str]]) -> str:
    payload = "".join(f"{key}={value}\n" for key, value in items).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def literal_contract() -> dict[str, object]:
    return {
        "route_version": "BOLD_CHANNEL_V24",
        "artifact_status": "UNNUMBERED_WORKING_ARTIFACT",
        "literal_atomization_gate": "V24_LITERAL_DETERMINANT_JUTILA_FAREY_ATOMIZATION=PROVED_EXACT_L0",
        "lemma1_jutila_gate": "V24_BLOMER_LI_LEMMA1_JUTILA_INTERFACE=PROVED_SOURCE_BACKED",
        "claim_ceiling": "EXACT_L0_LITERAL_DETERMINANT_TO_JUTILA_MAIN_AND_FAREY_KLOOSTERMAN_ATOMIZATION_WITH_SOURCE_TRANSFER_FIREWALLS",
        "physical_h0": 2,
        "analytic_physical_binding": "x=2X",
        "physical_shell": "STRICT_x_OVER_2_LT_t_LE_x",
        "raw_row": "V19_COMBINED_RAW_MASTER_PLUS2_MINUS1",
        "residual": "LAMBDA_SHIFT2_MINUS_TENSOR_LOCAL_B",
        "determinant_prime_branch": "D=d_phys*r-T_occurrence-2",
        "channel_policy": "PRIME_AND_HYBRID_SEPARATE_EXACT",
        "outer_absolute_value": "ONCE_OUTSIDE_COMPLETE_REASSEMBLY",
        "exactly_once_cover": "ALL_LITERAL_OCCURRENCES_WITH_ORIGINAL_MULTIPLICITY",
        "typed_alphabet": "d_phys__q_J__d_J__c_F__b_F__u_F__t_F__ell_J__d_BL_ALL_DISTINCT",
        "jutila_source": "BLOMER_LI_2511_03294V1_SECTION_2_1_LEMMA_1",
        "jutila_qmes": "x_POWER_1_OVER_3",
        "jutila_qsrc": "2_QMES",
        "jutila_omega": "PRIME_QMES_LT_q_LE_2QMES",
        "jutila_L": "SUM_PHI_q_EQUALS_SUM_q_MINUS_1",
        "jutila_psi": "RANGE_0_1_SUPPORT_MINUS1_1_INTEGRAL1",
        "jutila_eta": "1/32",
        "jutila_delta": "QMES_POWER_MINUS_63_OVER_32_EQUALS_x_POWER_MINUS_21_OVER_32",
        "jutila_split": "EXACT_MAIN_PLUS_EXPLICIT_ERROR_BY_ONE_EQUALS_CHI_PLUS_ONE_MINUS_CHI",
        "jutila_is_exact_delta": False,
        "farey_source": "BLOMER_LI_2511_03294V1_PRINTED_MAX_FIXED_PLUS_REPAIRED_FROM_FAREY_GEOMETRY",
        "farey_level": "ALL_INTEGERS_1_LE_c_LE_C_NOT_PRIME_ONLY",
        "farey_arc": "ABS_z_LE_1_OVER_cC_WITH_EXACT_NEIGHBORS",
        "farey_interval": "OPEN_C_MINUS_c_CLOSED_MIN_1_OVER_cABSz_MINUS_c_COMMA_C_INTEGER",
        "farey_additive_sign": "CORRECTED_e_c_u_t_TIMES_e_c_SIGN_z_u_b_inverse",
        "farey_printed_formula": "V24_BLOMER_LI_LEMMA2_AS_PRINTED_MAX_FIXED_PLUS=STOP_SCOPED_LITERAL_FAREY_COUNTEREXAMPLES",
        "farey_corrected_identity": "V24_CORRECTED_SIGNED_FAREY_IDENTITY=PROVED_EXACT_L0_REPOSITORY_DERIVATION",
        "dependency_lock": "LITERAL_PATH_AND_CANONICAL_HASH",
        "rational_chi_first_line": "d_J_MU_q_OVER_d_J_HATPSI_DELTA_d_J_ell",
        "rational_chi_second_line": "MU_q_OVER_d_J_ell_CONGRUENT_b_d_J_MOD_c_PSI_ell_OVER_c_d_J_PLUS_z",
        "eq2_2_second_line_q_factor": "ABSENT",
        "prime_dj_branches": "d_J_1_SIGN_MINUS__d_J_q_SIGN_PLUS_INSIDE_CHI",
        "identity_kloosterman": "V24_BARE_FAREY_B_SUM_TO_COMPLETE_KLOOSTERMAN_BILINEAR=PROVED_EXACT_L0__S_D_SIGN_z_u_MOD_c",
        "signed_qcb_atom": "IDENTITY_MINUS_CHI_BEFORE_ANY_OUTER_ABSOLUTE",
        "bl_theorem_object": "GL3_HECKE_A_n_1_TIMES_DIVISOR_TAU",
        "bl_factorable_weight": "q_EQUALS_p_t__p_PRIME__t_UNRESTRICTED_SMOOTH",
        "bl_t_domain": "NATURAL_t_WITH_RHO_t_OVER_Q2_NOT_PRIME_RESTRICTED",
        "bl_poisson_requirement": "NO_ARITHMETIC_CONDITION_ON_t",
        "bl_native_clock": "Q1_x4_21_Q2_x8_21_Q_x4_7_C0_x19_42_C_x23_42_DELTA_x_MINUS1",
        "v24_prime_clock": "QMES_x1_3_DELTA_x_MINUS21_32",
        "bl_s2_at_v24_clock": "FIRST_TERM_AT_LEAST_x7_6_STOP",
        "direct_bl_transfer": "V24_DIRECT_BLOMER_LI_GL3_DIVISOR_TO_LITERAL_TPC_TRANSFER=STOP_SCOPED_COEFFICIENT_VORONOI_CLOCK_AND_REASSEMBLY_MISMATCH",
        "prime_only_factorability_splice": "V24_PRIME_ONLY_JUTILA_SHELL_AS_BLOMER_LI_FACTORIZABLE_WEIGHT=STOP_SCOPED_UNRESTRICTED_SMOOTH_t_REQUIRED_FOR_POISSON",
        "bp_relation": "LOCAL_d_phys_EQUALS_q_DOUBLE_POISSON_ONLY_NOT_BL_SIGMA",
        "signed_qcb_gate": "V24_SIGNED_q_c_b_COLLECTIVE_PHYSICAL_EMITTER=OPEN_NEW_CONSTRUCTION",
        "error_theorem_gate": "V24_PRIME_SHELL_JUTILA_ERROR_SIGNED_FAREY_KLOOSTERMAN_THEOREM=OPEN_NEW_THEOREM",
        "main_to_bp_gate": "V24_PRIME_SHELL_JUTILA_MAIN_TO_BP_COLLECTIVE_EMITTER=OPEN_NEW_THEOREM",
        "factorable_aux_gate": "V24_FACTORIZABLE_AUXILIARY_JUTILA_ENSEMBLE_WITH_LITERAL_PHYSICAL_REASSEMBLY=OPEN_NEW_CONSTRUCTION",
        "arithmetic_advance": False,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }


def literal_registry_items() -> tuple[tuple[str, str], ...]:
    return (
        ("MAXIMUM_CLAIM", "EXACT_L0_LITERAL_DETERMINANT_JUTILA_FAREY_KLOOSTERMAN_ATOMIZATION_AND_SOURCE_TRANSFER_FIREWALL"),
        ("LITERAL_ATOMIZATION_GATE", "V24_LITERAL_DETERMINANT_JUTILA_FAREY_ATOMIZATION=PROVED_EXACT_L0"),
        ("LEMMA1_JUTILA_GATE", "V24_BLOMER_LI_LEMMA1_JUTILA_INTERFACE=PROVED_SOURCE_BACKED"),
        ("PHYSICAL_H0", "2"),
        ("PHYSICAL_X", "x_EQUALS_2X"),
        ("PHYSICAL_SHELL", "STRICT_x_OVER_2_LT_t_LE_x"),
        ("PHYSICAL_RAW_ROW", "V19_COMBINED_RAW_MASTER_PLUS2_MINUS1"),
        ("PHYSICAL_RESIDUAL", "LAMBDA_SHIFT2_MINUS_TENSOR_LOCAL_B"),
        ("PHYSICAL_DETERMINANT", "d_phys_r_MINUS_T_occurrence_MINUS_2"),
        ("PHYSICAL_CHANNELS", "PRIME_AND_HYBRID_SEPARATE"),
        ("OUTER_ABSOLUTE", "ONCE_AFTER_COMPLETE_SIGNED_REASSEMBLY"),
        ("EXACTLY_ONCE_COVER", "ORIGINAL_OCCURRENCE_MULTIPLICITY"),
        ("VARIABLE_TYPE_FIREWALL", "d_phys_q_J_d_J_c_F_b_F_u_F_t_F_ell_J_d_BL_DISTINCT"),
        ("JUTILA_SOURCE", "BLOMER_LI_V1_SECTION_2_1_LEMMA_1"),
        ("JUTILA_QMES", "x_POWER_1_OVER_3"),
        ("JUTILA_QSRC", "2_QMES"),
        ("JUTILA_WEIGHT", "PRIME_SHELL_INDICATOR"),
        ("JUTILA_L", "SUM_q_MINUS_1"),
        ("JUTILA_PSI", "RANGE_0_1_SUPPORT_MINUS1_1_INTEGRAL1"),
        ("JUTILA_DELTA", "QMES_MINUS63_OVER32_EQUALS_x_MINUS21_OVER32"),
        ("JUTILA_SPLIT", "EXACT_MAIN_PLUS_EXPLICIT_ERROR"),
        ("JUTILA_MAIN_ATOM", "q_a_z_WITH_1_OVER_DELTA_L"),
        ("FAREY_SOURCE", "BLOMER_LI_V1_PRINTED_LEMMA2_REPAIRED_FROM_FAREY_PARTITION"),
        ("FAREY_LEVEL", "COMPLETE_c_LE_C_NOT_PRIME_ONLY"),
        ("FAREY_ARC", "ABS_z_LE_1_OVER_cC"),
        ("FAREY_INTERVAL_I", "C_MINUS_c_TO_MIN_1_OVER_cABSz_MINUS_c_COMMA_C"),
        ("FAREY_ADDITIVE_ATOM", "c_inverse_e_c_ut_e_c_SIGN_z_u_b_inverse"),
        ("FAREY_PRINTED_LEMMA2", "V24_BLOMER_LI_LEMMA2_AS_PRINTED_MAX_FIXED_PLUS=STOP_SCOPED_LITERAL_FAREY_COUNTEREXAMPLES"),
        ("FAREY_CORRECTED_IDENTITY", "V24_CORRECTED_SIGNED_FAREY_IDENTITY=PROVED_EXACT_L0_REPOSITORY_DERIVATION"),
        ("FAREY_IDENTITY_KLOOSTERMAN", "V24_BARE_FAREY_B_SUM_TO_COMPLETE_KLOOSTERMAN_BILINEAR=PROVED_EXACT_L0__S_D_SIGN_z_u_c"),
        ("CHI_RATIONAL_FIRST_LINE", "d_J_MU_q_OVER_d_J_HATPSI"),
        ("CHI_RATIONAL_SECOND_LINE", "MU_q_OVER_d_J_CONGRUENCE_AND_PSI"),
        ("CHI_SECOND_LINE_Q_FACTOR", "ABSENT"),
        ("PRIME_DJ_BRANCHES", "dJ1_MINUS__dJq_PLUS_INSIDE_CHI"),
        ("SIGNED_QCB_ATOM", "IDENTITY_MINUS_CHI_COLLECTIVE_BEFORE_ABSOLUTE"),
        ("BL_DIRECT_SOURCE_OBJECT", "GL3_A_n_1_TIMES_TAU_m"),
        ("BL_FACTORIZABLE_WEIGHT", "q_EQUALS_p_t_WITH_SMOOTH_UNRESTRICTED_t"),
        ("BL_T_RESTRICTION", "PRIME_t_FORBIDDEN_BEFORE_POISSON"),
        ("BL_NATIVE_CHARACTER_SUM", "SIGMA_h_d_n1_n2_c_ONE_DIMENSIONAL_GL3_VORONOI_SUM"),
        ("BL_NATIVE_CHARACTER_BOUND", "c_POWER_1_PLUS_EPS_c2_HALF_SQRT_GCD_OVER_n1"),
        ("BL_NATIVE_CLOCK", "Q_x4_7_DELTA_x_MINUS1_C0_x19_42_C_x23_42"),
        ("V24_PRIME_CLOCK", "Q_x1_3_DELTA_x_MINUS21_32"),
        ("BL_S2_AT_V24_CLOCK", "FIRST_TERM_x7_OVER6_NOT_SAVING"),
        ("DIRECT_BL_TRANSFER", "V24_DIRECT_BLOMER_LI_GL3_DIVISOR_TO_LITERAL_TPC_TRANSFER=STOP_SCOPED_COEFFICIENT_VORONOI_CLOCK_AND_REASSEMBLY_MISMATCH"),
        ("PRIME_ONLY_FACTORIZABILITY_SPLICE", "V24_PRIME_ONLY_JUTILA_SHELL_AS_BLOMER_LI_FACTORIZABLE_WEIGHT=STOP_SCOPED_UNRESTRICTED_SMOOTH_t_REQUIRED_FOR_POISSON"),
        ("BP_LOCAL_RELATION", "d_phys_EQUALS_q_LOCAL_ISLAND_ONLY_NOT_BL_SIGMA"),
        ("SIGNED_QCB_COLLECTIVE_EMITTER", "V24_SIGNED_q_c_b_COLLECTIVE_PHYSICAL_EMITTER=OPEN_NEW_CONSTRUCTION"),
        ("ERROR_SIGNED_FAREY_KLOOSTERMAN_THEOREM", "V24_PRIME_SHELL_JUTILA_ERROR_SIGNED_FAREY_KLOOSTERMAN_THEOREM=OPEN_NEW_THEOREM"),
        ("MAIN_TO_BP_COLLECTIVE_EMITTER", "V24_PRIME_SHELL_JUTILA_MAIN_TO_BP_COLLECTIVE_EMITTER=OPEN_NEW_THEOREM"),
        ("FACTORIZABLE_AUXILIARY_ENSEMBLE", "V24_FACTORIZABLE_AUXILIARY_JUTILA_ENSEMBLE_WITH_LITERAL_PHYSICAL_REASSEMBLY=OPEN_NEW_CONSTRUCTION"),
        ("REQUIRED_BRANCH_REGISTRY", "ZERO_NONUNIT_ELL0_ELLNONZERO_MAJOR_MINOR_PRIME_HYBRID_AXES_TAILS"),
        ("REQUIRED_LOSS_LEDGER", "ONE_OVER_L_ONE_OVER_DELTA_SMOOTH_DUAL_TAIL_OUTER"),
        ("REQUIRED_REASSEMBLY", "ONE_OUTER_ABSOLUTE_EXACTLY_ONCE"),
        ("DEPENDENCY_PATH_LOCK", "LITERAL_V19_AND_V23_PATHS_WITH_CANONICAL_HASHES"),
        ("RELEASE_BOUNDARY", "ARITHMETIC_NO_FIXED_ATOM0_STRICT_UNPAID_L2_NONE_TPC207_FALSE"),
    )


def validate_exact_mapping(candidate: object, expected: dict[str, object]) -> None:
    require(type(candidate) is dict, "contract is not an exact dict")
    assert_candidate = candidate
    require(set(assert_candidate) == set(expected), "contract key set changed")
    for key, value in expected.items():
        actual = assert_candidate[key]
        require(type(actual) is type(value), f"contract field {key} changed type")
        require(actual == value, f"contract field {key} changed")


def validate_contract(candidate: object) -> None:
    require(type(candidate) is dict, "contract is not an exact dict")
    payload = json.dumps(candidate, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    literal_digest = "b64c0ef8a8be96a73c2baea140008c4b924ef0ddb29bd32cc5f20dda9b3b53af"
    require(hashlib.sha256(payload).hexdigest() == literal_digest, "contract literal digest changed")
    validate_exact_mapping(candidate, literal_contract())


def validate_registry(candidate: object, expected_digest: object) -> None:
    expected = literal_registry_items()
    require(type(candidate) is tuple, "registry is not an exact tuple")
    require(len(candidate) == len(expected), "registry row count changed")
    require(candidate == expected, "registry semantic row changed")
    require(all(type(row) is tuple and len(row) == 2 for row in candidate), "registry row type changed")
    require(all(type(k) is str and type(v) is str for k, v in candidate), "registry scalar type changed")
    require(len({key for key, _ in candidate}) == len(candidate), "registry keys ceased to be unique")
    literal_digest = "6ce7f2c3d2eb3a2e30900aaa7285d8e99bca139711db04915bdd9453a0a1808e"
    require(type(expected_digest) is str, "registry digest type changed")
    require(expected_digest == literal_digest, "registry expected digest changed")
    require(registry_hash(candidate) == literal_digest, "registry digest mismatch")


def validate_source_lock_contract(
    candidate_root: object,
    candidate_v19_path: object,
    candidate_v19_digest: object,
    candidate_v23_path: object,
    candidate_v23_digest: object,
) -> None:
    literal_root = Path(__file__).resolve().parents[2]
    locks = (
        (
            literal_root / "research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py",
            "e572bd9157ce4e733dc411ed8eb29df90d34be0ecf17023186f1648389ded519",
        ),
        (
            literal_root / "research/tpc-big-road/tpc_bridge_b_prime_shell_jutila_checker.py",
            "29ebf909a5c0c4209aba5ddb6eb76a3b91832a613578dadc6589272b855beb19",
        ),
    )
    require(type(candidate_root) is type(literal_root) and candidate_root == literal_root, "repository root lock changed")
    require(type(candidate_v19_path) is type(locks[0][0]) and candidate_v19_path == locks[0][0], "V19 dependency path changed")
    require(type(candidate_v19_digest) is str and candidate_v19_digest == locks[0][1], "V19 dependency digest changed")
    require(type(candidate_v23_path) is type(locks[1][0]) and candidate_v23_path == locks[1][0], "V23 dependency path changed")
    require(type(candidate_v23_digest) is str and candidate_v23_digest == locks[1][1], "V23 dependency digest changed")
    for path, expected in locks:
        require(path.is_file(), f"dependency is absent: {path}")
        require(canonical_lf_hash(path) == expected, f"dependency canonical hash changed: {path}")


def validate_source_locks() -> None:
    validate_source_lock_contract(ROOT, V19_PATH, V19_CANONICAL_SHA256, V23_PATH, V23_CANONICAL_SHA256)


def validate_checker_ast() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), "checker uses assert")
    forbidden_modules = {"subprocess", "socket", "urllib", "requests", "http", "ftplib"}
    forbidden = {
        "write",
        "writelines",
        "write_text",
        "write_bytes",
        "touch",
        "unlink",
        "rename",
        "mkdir",
        "rmdir",
        "symlink_to",
        "hardlink_to",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            require(all(alias.name.split(".")[0] not in forbidden_modules for alias in node.names), "checker imports forbidden module")
        if isinstance(node, ast.ImportFrom) and node.module:
            require(node.module.split(".")[0] not in forbidden_modules, "checker imports forbidden module")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            require(node.func.id not in {"open", "exec", "eval", "compile"}, f"checker contains forbidden call {node.func.id}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            require(node.func.attr not in forbidden, f"checker contains write call {node.func.attr}")


def load_v19() -> ModuleType:
    literal_path = Path(__file__).resolve().parents[2] / "research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py"
    require(V19_PATH == literal_path, "V19 loader path changed")
    spec = importlib.util.spec_from_file_location("tpc_v19_locked", literal_path)
    require(spec is not None and spec.loader is not None, "cannot load V19 dependency")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def factorization(n: int) -> dict[int, int]:
    require(n >= 1, "factorization domain changed")
    result: dict[int, int] = {}
    p = 2
    remaining = n
    while p * p <= remaining:
        while remaining % p == 0:
            result[p] = result.get(p, 0) + 1
            remaining //= p
        p += 1
    if remaining > 1:
        result[remaining] = result.get(remaining, 0) + 1
    return result


def divisors(n: int) -> tuple[int, ...]:
    values = [1]
    for prime, exponent in factorization(n).items():
        values = [value * prime**power for value in values for power in range(exponent + 1)]
    return tuple(sorted(values))


def mobius(n: int) -> int:
    factors = factorization(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def validate_determinant_identity() -> int:
    checked = 0
    for integer in range(2, 201):
        lhs: dict[int, int] = {}
        for divisor in divisors(integer):
            coefficient = mobius(divisor)
            if coefficient == 0:
                continue
            for prime, exponent in factorization(integer // divisor).items():
                lhs[prime] = lhs.get(prime, 0) + coefficient * exponent
        lhs = {prime: value for prime, value in lhs.items() if value}
        factors = factorization(integer)
        expected = {next(iter(factors)): 1} if len(factors) == 1 else {}
        require(lhs == expected, f"determinant Mangoldt identity failed at {integer}")
        checked += 1
    return checked


def beta_fraction(v19: ModuleType, integer: int, analytic_x: int) -> Fraction:
    vector_items, _, _ = v19.raw_master_numerator(integer, analytic_x)
    vector = dict(vector_items)
    if not vector:
        return Fraction(0)
    factors = dict(v19.factorization(integer))
    require(set(vector) <= set(factors), "raw beta gained a nonphysical prime log")
    ratios = {Fraction(vector.get(prime, 0), exponent) for prime, exponent in factors.items()}
    require(len(ratios) == 1, "raw beta fixture is not a rational log direction")
    return next(iter(ratios))


def local_d7(integer: int) -> Fraction:
    residue = integer % 7
    if residue == 0:
        return Fraction(0)
    if residue == 5:
        return Fraction(-35, 36)
    return Fraction(7, 36)


def periodize(values: dict[int, Fraction], modulus: int) -> tuple[Fraction, ...]:
    return tuple(sum(value for integer, value in values.items() if integer % modulus == residue) for residue in range(modulus))


def circular_correlation(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    modulus = len(left)
    require(len(right) == modulus, "correlation modulus changed")
    return tuple(sum(left[a] * right[(a + shift) % modulus] for a in range(modulus)) for shift in range(modulus))


def units(modulus: int) -> tuple[int, ...]:
    return tuple(value for value in range(modulus) if math.gcd(value, modulus) == 1)


def group_ring_direct(
    beta: dict[int, Fraction], residual: dict[int, Fraction], modulus: int, frequency: int, sign: int
) -> tuple[Fraction, ...]:
    require(sign in (-1, 1), "Farey half-arc sign changed")
    result = [Fraction(0) for _ in range(modulus)]
    for t, beta_value in beta.items():
        for u, residual_value in residual.items():
            coefficient = beta_value * residual_value
            if coefficient == 0:
                continue
            for b in units(modulus):
                exponent = ((u - t) * b + sign * frequency * pow(b, -1, modulus)) % modulus
                result[exponent] += coefficient
    return tuple(result)


def group_ring_periodized(
    correlation: tuple[Fraction, ...], modulus: int, frequency: int, sign: int
) -> tuple[Fraction, ...]:
    require(sign in (-1, 1), "Farey half-arc sign changed")
    result = [Fraction(0) for _ in range(modulus)]
    for difference, coefficient in enumerate(correlation):
        for b in units(modulus):
            exponent = (difference * b + sign * frequency * pow(b, -1, modulus)) % modulus
            result[exponent] += coefficient
    return tuple(result)


def farey_sequence(level: int) -> tuple[Fraction, ...]:
    return tuple(sorted({Fraction(a, c) for c in range(1, level + 1) for a in range(c + 1) if math.gcd(a, c) == 1}))


def farey_interval(level: int, denominator: int, z: Fraction) -> tuple[int, ...]:
    require(z != 0, "finite Farey fixture excludes z=0")
    lower = level - denominator
    upper = min(Fraction(1, 1) / (denominator * abs(z)) - denominator, Fraction(level))
    return tuple(integer for integer in range(lower + 1, math.floor(upper) + 1))


def printed_max_farey_interval(level: int, denominator: int, z: Fraction) -> tuple[int, ...]:
    require(z != 0, "finite printed-Farey fixture excludes z=0")
    lower = level - denominator
    upper = max(Fraction(1, 1) / (denominator * abs(z)) - denominator, Fraction(level))
    return tuple(integer for integer in range(lower + 1, math.floor(upper) + 1))


def additive_detector(modulus: int, values: tuple[int, ...], inverse_b: int, sign: int) -> int:
    require(sign in (-1, 1), "Farey detector sign changed")
    return sum(modulus for value in values if (value + sign * inverse_b) % modulus == 0)


def weighted_additive_detector(modulus: int, values: tuple[int, ...], inverse_b: int, sign: int) -> int:
    require(sign in (-1, 1), "Farey weighted-detector sign changed")
    return sum(modulus * value for value in values if (value + sign * inverse_b) % modulus == 0)


def ell_support(q: int, c: int, b: int, d_j: int, delta: Fraction) -> tuple[int, ...]:
    bound = Fraction(c * d_j) * delta
    radius = math.floor(bound)
    return tuple(ell for ell in range(-radius, radius + 1) if (ell - b * d_j) % c == 0)


def validate_finite_fixture() -> dict[str, object]:
    v19 = load_v19()
    beta = {integer: beta_fraction(v19, integer, 166) for integer in range(84, 167)}
    residual = {integer: local_d7(integer) for integer in range(84, 167)}
    require(sum(value != 0 for value in beta.values()) == 30, "x166 beta support changed")
    require(sum(beta.values()) == Fraction(839, 42), "x166 beta mass changed")
    require(sum(value != 0 for value in residual.values()) == 71, "x166 local profile support changed")
    require(sum(residual.values()) == Fraction(-7, 36), "x166 local profile mass changed")

    expected_b5 = (Fraction(43, 3), Fraction(1, 2), Fraction(3), Fraction(1, 7), Fraction(2))
    expected_w5 = (Fraction(7, 12), Fraction(-7, 9), Fraction(7, 18), Fraction(7, 18), Fraction(-7, 9))
    expected_k5 = (
        Fraction(275, 36),
        Fraction(-943, 108),
        Fraction(53, 27),
        Fraction(821, 108),
        Fraction(-2669, 216),
    )
    b5 = periodize(beta, 5)
    w5 = periodize(residual, 5)
    k5 = circular_correlation(b5, w5)
    require(b5 == expected_b5, "mod-5 beta periodization changed")
    require(w5 == expected_w5, "mod-5 residual periodization changed")
    require(k5 == expected_k5, "mod-5 determinant correlation changed")
    require(sum(value != 0 for value in k5) == 5 and k5[0] == Fraction(275, 36), "mod-5 axes changed")

    b7 = periodize(beta, 7)
    w7 = periodize(residual, 7)
    k7 = circular_correlation(b7, w7)
    require(sum(value != 0 for value in k7) == 7, "mod-7 correlation lost full support")
    require(k7[0] == Fraction(407, 108), "mod-7 zero axis changed")
    require(sum(k5) == sum(k7) == Fraction(-839, 216), "periodized total changed")

    group_ring_checks = 0
    for modulus, correlation in ((5, k5), (7, k7)):
        for sign in (-1, 1):
            for frequency in range(modulus):
                require(
                    group_ring_direct(beta, residual, modulus, frequency, sign)
                    == group_ring_periodized(correlation, modulus, frequency, sign),
                    "signed complete Kloosterman periodization failed",
                )
                group_ring_checks += 1

    multiset = [0] * 5
    for b in units(5):
        multiset[(2 * b + 3 * pow(b, -1, 5)) % 5] += 1
    require(tuple(multiset) == (2, 0, 1, 1, 0), "Kloosterman exponent multiset changed")

    farey = farey_sequence(5)
    require(len(farey) - 1 == 10, "Farey edge count changed")
    require(sum((right - left for left, right in zip(farey, farey[1:])), Fraction(0)) == 1, "Farey lengths ceased to sum to one")
    for left, right in zip(farey, farey[1:]):
        require(right.numerator * left.denominator - left.numerator * right.denominator == 1, "Farey neighbor determinant changed")
    require(farey_interval(5, 3, Fraction(1, 30)) == (3, 4, 5), "corrected Farey long interval changed")
    require(farey_interval(5, 3, Fraction(1, 20)) == (3,), "corrected Farey short interval changed")
    require(farey_interval(5, 3, Fraction(-1, 30)) == (3, 4, 5), "Farey interval lost absolute-z symmetry")
    require(printed_max_farey_interval(1, 1, Fraction(1, 4)) == (1, 2, 3), "printed max counterexample changed")
    require(farey_interval(1, 1, Fraction(1, 4)) == (1,), "corrected min counterexample changed")

    negative_values = farey_interval(5, 3, Fraction(-1, 22))
    positive_values = farey_interval(5, 3, Fraction(1, 25))
    require(negative_values == (3, 4), "negative Farey neighbor interval changed")
    require(positive_values == (3, 4, 5), "positive Farey neighbor interval changed")
    require(additive_detector(3, negative_values, 1, -1) == 3, "negative Farey detector lost the left neighbor")
    require(additive_detector(3, negative_values, 1, 1) == 0, "printed fixed-plus detector ceased to be falsified")
    require(additive_detector(3, positive_values, 1, 1) == 3, "positive Farey detector lost the right neighbor")
    require(Fraction(additive_detector(3, negative_values, 1, -1), 3) == 1, "negative 1/c normalization changed")
    require(Fraction(additive_detector(3, positive_values, 1, 1), 3) == 1, "positive 1/c normalization changed")
    require(Fraction(weighted_additive_detector(3, negative_values, 1, -1), 3) == 4, "left-neighbor symbol changed")
    require(Fraction(weighted_additive_detector(3, positive_values, 1, 1), 3) == 5, "right-neighbor symbol changed")

    require(ell_support(5, 3, 2, 1, Fraction(1, 4)) == (), "dJ=1 ell support changed")
    require(ell_support(5, 3, 2, 5, Fraction(1, 4)) == (-2, 1), "dJ=q ell support changed")
    support_c7 = ell_support(7, 7, 1, 7, Fraction(1, 10))
    support_c5 = ell_support(7, 5, 1, 7, Fraction(1, 10))
    require(support_c7 == (0,), "ell=0 branch at c=q changed")
    require(0 not in support_c5, "ell=0 branch leaked to c not dividing dJ")

    factorable = (3, 6, 18)
    require(3 <= factorable[0] <= 6 and 4 <= factorable[1] <= 8, "factorable domain witness left its blocks")
    require(factorable[0] * factorable[1] == factorable[2], "factorable witness product changed")
    require(factorization(factorable[1]) != {factorable[1]: 1}, "unrestricted t witness became prime")
    require(not any(7 == p * t for p in range(2, 7) for t in range(2, 7)), "prime shell gained two nontrivial factors")

    require(Fraction(4, 21) + Fraction(8, 21) == Fraction(4, 7), "Blomer--Li factorable clock changed")
    require(Fraction(2) - Fraction(4, 7) - Fraction(19, 42) == Fraction(41, 42), "Blomer--Li endpoint exponent changed")
    require(Fraction(2) - Fraction(1, 3) - Fraction(1, 2) == Fraction(7, 6), "forced V24 error exponent changed")
    require(Fraction(1, 3) * Fraction(-63, 32) == Fraction(-21, 32), "prime Jutila delta clock changed")
    require(Fraction(11, 1536) - Fraction(1, 400) == Fraction(179, 38400), "strict margin changed")
    require(Fraction(1, 192) - Fraction(1, 400) == Fraction(13, 4800), "energy threshold changed")

    split_weights = {Fraction(-2): Fraction(1, 3), Fraction(0): Fraction(2, 5), Fraction(3): Fraction(-1, 7)}
    ledger = {Fraction(-2): Fraction(3), Fraction(0): Fraction(-5), Fraction(3): Fraction(7)}
    for determinant, coefficient in ledger.items():
        main = coefficient * split_weights[determinant]
        error = coefficient * (1 - split_weights[determinant])
        require(main + error == coefficient, "Jutila split ceased to be coefficientwise exact")

    return {
        "beta_support": 30,
        "beta_mass": "839/42",
        "local_profile_support": 71,
        "local_profile_mass": "-7/36",
        "mod5_correlation": [str(value) for value in k5],
        "mod5_support": 5,
        "mod7_support": 7,
        "mod5_zero_axis": "275/36",
        "mod7_zero_axis": "407/108",
        "group_ring_checks": group_ring_checks,
        "farey_edges": 10,
        "printed_max_count": 3,
        "corrected_min_count": 1,
        "negative_signed_detector": 3,
        "negative_fixed_plus_detector": 0,
        "negative_neighbor_denominator": 4,
        "positive_neighbor_denominator": 5,
        "factorable_witness": list(factorable),
    }


def changed_value(value: object) -> object:
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if type(value) is str:
        return value + "__MUTATED"
    raise CheckFailure("unsupported contract mutation type")


def wrong_type(value: object) -> object:
    if type(value) is bool:
        return 1
    if type(value) is int:
        return str(value)
    if type(value) is str:
        return False
    raise CheckFailure("unsupported contract type mutation")


def expect_rejected(call: Callable[[], None], label: str) -> None:
    try:
        call()
    except CheckFailure:
        return
    raise CheckFailure(f"mutation escaped: {label}")


def run_source_lock_mutations() -> int:
    attacks = (
        (ROOT.parent, V19_PATH, V19_CANONICAL_SHA256, V23_PATH, V23_CANONICAL_SHA256, "root"),
        (ROOT, V23_PATH, V19_CANONICAL_SHA256, V23_PATH, V23_CANONICAL_SHA256, "V19 path"),
        (ROOT, V19_PATH, V23_CANONICAL_SHA256, V23_PATH, V23_CANONICAL_SHA256, "V19 digest"),
        (ROOT, V19_PATH, V19_CANONICAL_SHA256, V19_PATH, V19_CANONICAL_SHA256, "coordinated V23 to V19"),
        (ROOT, V23_PATH, V23_CANONICAL_SHA256, V23_PATH, V23_CANONICAL_SHA256, "coordinated V19 to V23"),
        (str(ROOT), V19_PATH, V19_CANONICAL_SHA256, V23_PATH, V23_CANONICAL_SHA256, "root type"),
        (ROOT, V19_PATH, V19_CANONICAL_SHA256, V23_PATH, b"0" * 32, "digest type"),
    )
    for root, v19_path, v19_digest, v23_path, v23_digest, label in attacks:
        expect_rejected(
            lambda r=root, p19=v19_path, h19=v19_digest, p23=v23_path, h23=v23_digest: validate_source_lock_contract(
                r, p19, h19, p23, h23
            ),
            f"source lock {label}",
        )
    return len(attacks)


def run_contract_mutations() -> int:
    expected = literal_contract()
    validate_contract(expected)
    count = 0
    for key in expected:
        missing = dict(expected)
        del missing[key]
        expect_rejected(lambda candidate=missing: validate_contract(candidate), f"contract missing {key}")
        count += 1

        changed = dict(expected)
        changed[key] = changed_value(expected[key])
        expect_rejected(lambda candidate=changed: validate_contract(candidate), f"contract value {key}")
        count += 1

        typed = dict(expected)
        typed[key] = wrong_type(expected[key])
        expect_rejected(lambda candidate=typed: validate_contract(candidate), f"contract type {key}")
        count += 1

    extra = dict(expected)
    extra["UNKNOWN_FALSE_RELEASE"] = True
    expect_rejected(lambda: validate_contract(extra), "contract extra")
    count += 1

    coordinated = dict(expected)
    coordinated.update(
        {
            "signed_qcb_gate": "PROVED_FALSE_PROMOTION",
            "arithmetic_advance": True,
            "fixed_atom_credit": 1,
            "strict_1_over_400": "PAID",
            "L2": "PROVED",
            "TPC_207_TRIGGER": True,
        }
    )
    expect_rejected(lambda: validate_contract(coordinated), "coordinated false release")
    count += 1
    return count


def run_registry_mutations() -> int:
    expected = literal_registry_items()
    validate_registry(expected, EXPECTED_REGISTRY_SHA256)
    count = 0
    for index, (key, value) in enumerate(expected):
        missing = expected[:index] + expected[index + 1 :]
        expect_rejected(lambda candidate=missing: validate_registry(candidate, registry_hash(candidate)), f"registry missing {key}")
        count += 1

        changed = list(expected)
        changed[index] = (key, value + "__MUTATED")
        changed_tuple = tuple(changed)
        expect_rejected(lambda candidate=changed_tuple: validate_registry(candidate, registry_hash(candidate)), f"registry value {key}")
        count += 1

        replaced = list(expected)
        replaced[index] = (f"UNKNOWN_{index:02d}", value)
        replaced_tuple = tuple(replaced)
        expect_rejected(lambda candidate=replaced_tuple: validate_registry(candidate, registry_hash(candidate)), f"registry key {key}")
        count += 1

    extra = expected + (("UNKNOWN_EXTRA", "FALSE"),)
    expect_rejected(lambda: validate_registry(extra, registry_hash(extra)), "registry extra")
    count += 1
    expect_rejected(lambda: validate_registry(list(expected), registry_hash(expected)), "registry wrong container type")
    count += 1
    coordinated = list(expected)
    coordinated[-1] = ("RELEASE_BOUNDARY", "ARITHMETIC_YES_FIXED_ATOM1_STRICT_PAID_L2_PROVED_TPC207_TRUE")
    coordinated_tuple = tuple(coordinated)
    expect_rejected(lambda: validate_registry(coordinated_tuple, registry_hash(coordinated_tuple)), "registry coordinated false release")
    count += 1
    expect_rejected(lambda: validate_registry(expected, "0" * 64), "registry digest")
    count += 1
    duplicate = expected + (expected[0],)
    expect_rejected(lambda: validate_registry(duplicate, registry_hash(duplicate)), "registry duplicate")
    count += 1
    return count


def validate_result_semantics(result: dict[str, object]) -> None:
    require(result["claim_ceiling"] == literal_contract()["claim_ceiling"], "result claim changed")
    require(type(result["source_lock_mutations"]) is int and result["source_lock_mutations"] == 7, "source-lock attack count changed")
    require(result["signed_qcb_gate"] == "OPEN_NEW_CONSTRUCTION", "result gate promoted")
    require(result["factorable_aux_gate"] == "OPEN_NEW_CONSTRUCTION", "result auxiliary gate promoted")
    require(result["arithmetic_advance"] is False, "result arithmetic promoted")
    require(type(result["fixed_atom_credit"]) is int and result["fixed_atom_credit"] == 0, "result atom credit promoted")
    require(result["strict_1_over_400"] == "UNPAID", "result endpoint promoted")
    require(result["L2"] == "NONE", "result L2 promoted")
    require(result["TPC_207_TRIGGER"] is False, "result TPC207 promoted")


def run_check() -> dict[str, object]:
    validate_source_locks()
    validate_checker_ast()
    validate_contract(CONTRACT)
    validate_registry(REGISTRY_ITEMS, EXPECTED_REGISTRY_SHA256)
    determinant_checks = validate_determinant_identity()
    fixture = validate_finite_fixture()
    source_lock_mutations = run_source_lock_mutations()
    contract_mutations = run_contract_mutations()
    registry_mutations = run_registry_mutations()

    result: dict[str, object] = {
        "check": True,
        "route_version": "BOLD_CHANNEL_V24",
        "claim_ceiling": "EXACT_L0_LITERAL_DETERMINANT_TO_JUTILA_MAIN_AND_FAREY_KLOOSTERMAN_ATOMIZATION_WITH_SOURCE_TRANSFER_FIREWALLS",
        "contract_fields": len(literal_contract()),
        "contract_mutations": contract_mutations,
        "registry_rows": len(literal_registry_items()),
        "registry_mutations": registry_mutations,
        "registry_sha256": registry_hash(literal_registry_items()),
        "determinant_identity_checks": determinant_checks,
        "source_lock_mutations": source_lock_mutations,
        "fixture": fixture,
        "signed_qcb_gate": "OPEN_NEW_CONSTRUCTION",
        "factorable_aux_gate": "OPEN_NEW_CONSTRUCTION",
        "arithmetic_advance": False,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }
    validate_result_semantics(result)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run the fail-closed read-only checks")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.check:
        raise CheckFailure("explicit --check is required")
    print(json.dumps(run_check(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
