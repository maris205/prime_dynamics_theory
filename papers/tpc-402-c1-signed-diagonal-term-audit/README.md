# TPC-402: signed diagonal-deletion term audit

TPC-402 continues TPC-401 by retaining the sign law as an explicit finite
modeling choice and proving the induced off-diagonal coefficient formula
`M_sigma(u,v)=T_uv[-A_sigma+b_sigma(u)+b_sigma(v)]`. Exact `Fraction`
arithmetic checks both all-plus and alternating-index laws over 240 sampled
off-diagonal rows (120 per law), corresponding to 209280 exact prime
comparisons across six TPC-400 origins, five positions per origin, and the
872-prime shell. The anchor boundary remains outside the hypothesis because
`N=13,Q=8,p=11` admits a divisible off-diagonal difference.

The result is `PROVED_EXACT_FINITE` analytic structure. It does not identify
the alternating signs with an arithmetic character, pay arithmetic `L2`, or
close Route-B. The required project layout and `paper/paper.pdf` are present.

```bash
python -B papers/tpc-402-c1-signed-diagonal-term-audit/code/tpc402_c1_signed_diagonal_term_audit.py --check
python -B papers/tpc-402-c1-signed-diagonal-term-audit/experiments/tpc402_independent_checker.py --check
python -B papers/tpc-402-c1-signed-diagonal-term-audit/experiments/tpc402_adversarial_certificate_stress.py --check
```

`ARITHMETIC_ADVANCE=NO`, `FIXED_POWER_CREDIT=0`, `FULL_GATE_B=OPEN`, and
`ROUND2_CLUE=TEST_C1_SIGNED_DIAGONAL_TERM_GROWING_OBSTRUCTION`.
