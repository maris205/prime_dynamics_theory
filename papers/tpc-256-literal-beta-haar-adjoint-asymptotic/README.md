# TPC-256: Literal Beta Rank-Midpoint Asymptotics and Diagonal-Dominant Adjoint Phase

Status:

```text
PROVED_SOURCE_BACKED_L1_LITERAL_BETA_RANK_MIDPOINT_AND_DIAGONAL_DOMINANT_ADJOINT_ASYMPTOTIC
```

TPC-256 evaluates the literal V59 coefficient on the coefficient-independent
ordered-rank midpoint Haar direction.  For every sufficiently large real
clock `x`,

```text
<z_mid,beta>
 = [log(32/27)/sqrt(2)] sqrt(x)/log^2(x)
   + O(sqrt(x)/log^3(x))
 > 0.
```

The truncated Möbius divisor lane is not estimated through cancellation of
`mu`.  Instead, the density `1/d` cancels exactly between the two consecutive
rank children for each divisor layer before taking absolute values, leaving
`O(U/rho)=O(x^(-67/400))`.  The main term comes from the second-order
curvature of `Li` under the de la Vallée Poussin PNT.

TPC-255's exact adjoint identity then gives

```text
<z_mid,A_x beta>
 = -B_Q<z_mid,beta> + R_unit + R_hard + R_jump,

B_Q = (9/2+o(1)) x^(2/3)/log(x),
R_unit = O_epsilon(x^(5/6+epsilon)),
R_hard,R_jump = O_(psi,epsilon)(x^(55/48+epsilon)).
```

The diagonal exponent is `7/6=56/48`, so the two boundary lanes are smaller
by the fixed exponent `1/48`.  Consequently,

```text
<z_mid,A_x beta>
 = -[9 log(32/27)/(2sqrt(2))+o(1)] x^(7/6)/log^3(x)
```

in `C`.  Its real part is eventually negative, the scalar is eventually
nonzero, and its normalized phase tends to `-1`.  The scalar itself is not
claimed to be real, and no unqualified principal-argument limit to `+pi` is
claimed.

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-256-literal-beta-haar-adjoint-asymptotic/code/tpc256_literal_beta_haar_certificate.py --check
python -O -B papers/tpc-256-literal-beta-haar-adjoint-asymptotic/code/tpc256_literal_beta_haar_certificate.py --check
python -B papers/tpc-256-literal-beta-haar-adjoint-asymptotic/experiments/tpc256_independent_checker.py --check
python -O -B papers/tpc-256-literal-beta-haar-adjoint-asymptotic/experiments/tpc256_independent_checker.py --check
python -B papers/tpc-256-literal-beta-haar-adjoint-asymptotic/experiments/tpc256_beta_haar_asymptotic_stress.py --check
python -O -B papers/tpc-256-literal-beta-haar-adjoint-asymptotic/experiments/tpc256_beta_haar_asymptotic_stress.py --check
```

The producer verifies eight frozen provenance blobs, 19 source-claim markers,
64 exact rank clocks, 1,536 divisor layers, 90 complete unit rows, 8,814
pointwise unit-mask terms, and both boundary cardinality rules.  The
independent checker imports no producer code and rejects 112 deterministic
semantic mutations in 14 classes.  The stress program checks 192 families,
split into 96 integer and 96 noninteger real clocks.

The finite scaled values at `x=100000` and `x=1000000` are labelled
`NUMERICAL_OBSERVATION`.  They are reproducibility data only and receive no
asymptotic proof credit.

## Build

From `paper/`:

```bash
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
bibtex paper
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
```

## Claim firewall

```text
TPC256_ROUTE_ADVANCE = YES_LITERAL_ARITHMETIC
TPC256_ARITHMETIC_ADVANCE = YES_SCOPED_LITERAL_BETA_ADJOINT_HAAR_LANE
TPC256_LITERAL_BETA_HAAR_ASYMPTOTIC = PROVED_SOURCE_BACKED
TPC256_ADJOINT_NORMALIZED_COMPLEX_ASYMPTOTIC = PROVED_SOURCE_BACKED
TPC256_REAL_PART_EVENTUALLY_NEGATIVE = PROVED
TPC256_SCALAR_EVENTUALLY_NONZERO = PROVED
TPC256_NORMALIZED_PHASE_TO_MINUS_ONE = PROVED
TPC256_SCALAR_IS_REAL = NOT_CLAIMED
TPC256_UNQUALIFIED_PRINCIPAL_ARGUMENT_TO_PLUS_PI = NOT_CLAIMED
TPC256_FIXED_ATOM_CREDIT = 0
TPC256_L2 = NONE
TPC256_FULL_GATE_B = OPEN
TPC256_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC256_TWIN_PRIME_RESULT = NONE
```

The result is one literal ordered-rank Haar projection.  It does not control
the transverse/full-output component, couple that component to the physical
`w` lane, prove an `L2` theorem, close full Gate B, pay the global strict
`1/400` budget, or imply a twin-prime result.
