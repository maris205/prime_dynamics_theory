# TPC-216 Paper Plan

## Title

Direct-Sum Row-Energy Envelope and the Cauchy Bottleneck

## Research question

After TPC-215 removes fixed-power amplification from complete-period
reduced-frequency clustering, how large can the literal V46 divisor direct-sum
row energy be before any finite-window cross-frequency or prime-shell
reassembly is attempted?

## Main theorem

Let

```text
H=x^(21/32), Q=x^(1/3), Y0=H/(4Q), U=x^(133/400),
Q_x={q prime: Q<q<=2Q}, P=#Q_x,
D_x={Y0<d<=U: mu(d)^2=1}.
```

For sufficiently large `x`, so that `4Q<H` and `U<Q`, split the literal
coefficient-free emitter as `B_d=sum_q B_(d,q)`.  The fixed-q integer cutoff
is injective modulo `d`, and a shell Cauchy inequality gives

```text
||B_d||_2^2 <= 4 ||psi||_infty^2 P^2 d Q/H.
```

Using `P<=2Q` and `|c_d|^2=(log d)^2/d^2`,

```text
L^(-1) E_direct
  <= C_psi (Q^3/H) (log U)^3
  = x^(11/32+o(1)).
```

The statement is a complete-period direct-sum envelope, not a physical
finite-window estimate and not an arithmetic cancellation theorem.

## Adversarial control

Use the exact rational fixture

```text
d=5, Q-scale=100, H=500,
q={101,131,151,181}, psi(t)=(1+t^2)^(-2).
```

Every `q` is `1 mod 5`, every cutoff is one, and all fixed-q rows have support
`{1,4}`.  Their combined norm is therefore larger than the sum of individual
norms.  The exact coherence ratio is recorded as a rational number and is
labeled `FINITE_STRUCTURAL_ADVERSARY`; it is not V46 asymptotic evidence.

## Claim ceiling

```text
PROVED_STRUCTURAL_L1 = fixed-q no-collision and complete-period direct-sum envelope
NUMERICALLY_CERTIFIED = exact finite aligned-support fixture
NUMERICAL_OBSERVATION = decimal display of the exact fixture ratio
HEURISTIC = none needed
CONJECTURE = none needed
OPEN = finite-window Gram, prime-shell reassembly, arithmetic cancellation
REFUTED_SCOPED = free q-orthogonality shortcut
ARITHMETIC_ADVANCE = NO
```

## Route decision

This is a Route-B structural advance.  It supplies the next quantitative
envelope after TPC-215, but it does not pay the strict `1/400` endpoint and does
not create fixed-atom credit.

## Next theorem edge

The next useful question is whether the complete-period direct-sum envelope can
be coupled to a source-locked arithmetic or finite-window bound without
discarding the literal Mobius signs and four-packet reassembly.
