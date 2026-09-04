# TPC-375 theorem ledger

| Item | Status | Scope |
|---|---|---|
| inherited response-blind beta=2 panel | PROVED_EXACT_FINITE | three origins, three Q anchors |
| common full-window geometry | PROVED_EXACT_FINITE | all nine rows and four bands |
| nested cutoff masks | PROVED_EXACT_FINITE_PREDECLARED | `c=0,1,2,3` |
| band/complement identity | PROVED_EXACT_FINITE | every finite row |
| four-cutoff replay | NUMERICALLY_CERTIFIED_FINITE_SCOPED | 9 rows |
| failure-key census | NUMERICALLY_CERTIFIED_FINITE_SCOPED | counts `0,6,6,6` |
| minimal cutoff | NUMERICALLY_CERTIFIED_FINITE_SCOPED | first match `c=1` |
| selected-mode Rayleigh audit | NUMERICALLY_CERTIFIED_FINITE_SCOPED | all cutoffs |
| bandwidth holdout transfer | OPEN | next question |
| bandwidth/origin/window uniformity | OPEN | no growing theorem |
| arithmetic `L2` / fixed power | NO / 0 | no credit |
| Route-B closure / twin-prime result | OPEN / NONE | unchanged |

The rational anchor is inherited from TPC-374 and is not used for row or
cutoff selection.
