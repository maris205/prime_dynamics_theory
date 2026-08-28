# TPC-294 theorem ledger

| ID | statement | status | evidence / boundary |
|---|---|---|---|
| T294.1 | $R(a)=1+2\sum_{i<j}a_i a_jG_{ij}/\operatorname{tr}G$ | `PROVED_EXACT_FINITE` | diagonal expansion |
| T294.2 | common-denominator exhaustive sign search is global modulo reversal | `PROVED_EXACT_FINITE` | finite enumeration lemma |
| T294.3 | Gram sign quotient is nonnegative | `PROVED_EXACT_FINITE` | squared-norm identity |
| T294.4 | all 18 frozen rows have a weighted sign minimum below one | `NUMERICALLY_CERTIFIED_FINITE` | canonical rational payload + independent replay |
| T294.5 | all 18 all-positive vectors have quotient above one | `NUMERICALLY_CERTIFIED_FINITE` | same payload |
| T294.6 | weighted and unit-edge max-cut optima differ on all 18 rows | `NUMERICALLY_CERTIFIED_FINITE` | exact label/value comparison |
| T294.7 | weighted minimizers belong to the native source image | `OPEN` | not tested in this paper |
| T294.8 | a growing weighted-shell contraction theorem | `OPEN` | finite grid only |
| T294.9 | arithmetic $L^2$, fixed power, Gate B, twin-prime endpoint | `OPEN` | no credit paid |

## Reproducibility locks

The producer locks the TPC-293 code/result and frozen TPC-268 engine.  The
independent checker repeats those locks and does not import the TPC-294
producer.  The result JSON is canonical and carries a SHA-256 payload digest.
