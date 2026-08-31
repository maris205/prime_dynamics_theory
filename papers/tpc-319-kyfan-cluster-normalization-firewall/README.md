# TPC-319 — Ky Fan cluster masses and the normalization firewall

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-319 extends the TPC-318 top-eigenvalue audit to Ky Fan cluster masses
\(F_k=\sum_{j\le k}\lambda_j\) for \(k=1,2,4,8,16\).  On the same
`X=640,1280,2560`, `Q={24,36,54,80}`, `s={1,2}` panel, all 80 adjacent
normalized comparisons strictly decrease while all 80 unnormalized comparisons
strictly increase.  The exact normalization identity explains the coexistence:
the unnormalized ratios lie between `1` and `2`, so division by the doubled source
count reverses the observed direction.

The top signal is genuinely clustered on part of the panel.  The relative edge-gap
census is below `0.01` for 10/24 rows at `k=1`, 5/24 at `k=2`, 2/24 at `k=4`,
4/24 at `k=8`, and 13/24 at `k=16`.  This is a finite diagnostic, not a canonical
eigenvector theorem.

## Claim firewall

```text
PROVED_EXACT = finite PSD/Ky-Fan variational identities and normalization-flip lemma
NUMERICALLY_CERTIFIED_FINITE = 24 rows; 80 normalized decreases; 80 unnormalized increases
NUMERICAL_OBSERVATION = finite cluster gaps, effective-rank ranges, and slope ranges
OPEN = uniform normalization law; stable arithmetic eigenspace; signed reassembly;
       fixed-power credit; full Gate B; twin-prime endpoint
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The finite error model uses the safe uniform literal-entry bound `|K|<=160`, forward
and reverse shell order, dual symmetric eigensolver paths, residuals, and a Weyl
entrywise guard.  It does not turn finite observations into an asymptotic theorem.

The complete package is `PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`,
`notes/`, `code/`, `experiments/`, `results/`, and `paper/`.  Canonical outputs are
[results/tpc319_certificate.json](results/tpc319_certificate.json) and
[paper/paper.pdf](paper/paper.pdf).

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc319_kyfan_cluster_normalization.py --write
python -B code/tpc319_kyfan_cluster_normalization.py --check
python -O -B code/tpc319_kyfan_cluster_normalization.py --check
python -B experiments/tpc319_independent_checker.py --check
python -O -B experiments/tpc319_independent_checker.py --check
python -B experiments/tpc319_cluster_stress.py
python -O -B experiments/tpc319_cluster_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc319_kyfan_cluster_checker.py --check
```
