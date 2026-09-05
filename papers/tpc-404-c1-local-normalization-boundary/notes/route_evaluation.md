# Route evaluation

The exact local identities are a valid finite continuation of TPC-403.  The
observed normalized coefficients stay near `1.36e-2` across four selected
profiles, so the raw CRT coefficient ratio does not by itself establish a
normalized growing obstruction.  The official evaluator files are absent from
the checkout; this evaluation is fail-closed under the local proof package and
TPC_HANDOFF claim ceiling.

Route A: no arithmetic advance and no fixed-power credit.

Route B: the local finite normalization boundary is proved, but source
reassembly and any growing normalized estimate remain open.

`ROUND2_CLUE=TEST_C1_LOCAL_NORMALIZATION_SCALE_LADDER`.
