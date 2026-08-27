# TPC-276 — Signed-gain margin recovery and the strict endpoint budget

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

For the actual TPC-275 packet decomposition, the exact signed gain
`r=D/G` upgrades the diagonal margin by `m^2=r m_D^2`; a conditional growing
bound `r>=b x^gamma` therefore contributes `gamma/2` to the endpoint budget.
The 12-row transfer has `r>1` everywhere, three signed rows above the quarter
threshold and five above the eighth threshold, but finite data provide zero
fixed-power credit.

## What is new

- an exact algebraic bridge from signed packet energy to the actual correlation
  margin;
- a strict conditional compiler with effective-loss budget
  `sigma-eta_eff>1/400`, where `eta_eff=max(0,eta_D-gamma/2)`;
- an exact finite-to-asymptotic firewall for signed gain promotion;
- independent rational transfer of all 12 TPC-275 rows and threshold counts;
- an explicit distinction between finite threshold recovery and a growing
  source-level theorem.

## Claim ceiling

```text
PROVED_CONDITIONAL = SIGNED_GAIN_STRICT_ENDPOINT_BUDGET_COMPILER
PROVED_EXACT_FINITE = SIGNED_GAIN_MARGIN_IDENTITY_PLUS_NO_POWER_PROMOTION
NUMERICALLY_CERTIFIED = 12_ROW_SIGNED_MARGIN_TRANSFER
OPEN = SOURCE_LEVEL_SIGNED_GAIN, ARITHMETIC L2, FULL GATE B
FIXED_POWER_CREDIT = 0
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc276_signed_gain_endpoint_budget_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc276_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc276_budget_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  TPC-275 is the frozen
parent certificate; the Session-named `propose.md` and evaluator files remain
absent in this checkout, with the local theorem ledger and fail-closed checker
providing the available fallback authority.
