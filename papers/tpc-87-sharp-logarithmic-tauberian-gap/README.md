# TPC-87: Sharp logarithmic Tauberian gap

This paper identifies the exact discrete gap between logarithmic and
ordinary cancellation.

For

```text
S_N = sum_{n <= N} a_n,
L_N = sum_{n <= N} a_n / n,
L_0 = 0,
```

the main identity is

```text
S_N = N L_N - sum_{m < N} L_m,

S_N / N = L_N - (1/N) sum_{m < N} L_m.
```

Hence ordinary cancellation is equivalent, with exactly the same
rate, to vanishing of the signed backward Cesaro defect of the
unnormalized logarithmic primitive `L_N`.

The paper keeps separate:

```text
L_N                  unnormalized logarithmic primitive
lambda_N = L_N / H_N normalized logarithmic mean
```

Convergence of `L_N` is sufficient for `S_N/N -> 0`, but boundedness
is not. For the bounded dyadic sequence

```text
a_n = (-1)^k on 2^k <= n < 2^(k+1),
```

one has:

- `|a_n| = 1`;
- `L_N = O(1)`;
- `lambda_N -> 0`;
- every growing Tao-shaped terminal window has normalized
  logarithmic cancellation;
- the ordinary means have subsequential limits `1/3` and `-1/3`.

Thus no structure-free Tauberian black box converts normalized
logarithmic cancellation into ordinary cancellation.

Two quantitative positive routes are proved:

1. terminal-half cancellation

   ```text
   omega_N(L)
     = max_{floor(N/2) <= m <= N} |L_N - L_m| -> 0;
   ```

2. vanishing dyadic logarithmic variation

   ```text
   V_k = sum_{2^k <= n < 2^(k+1)} |a_n| / n -> 0.
   ```

Both come with explicit geometric convolution bounds. A power bound
`omega_N(L) << N^(-eta)` for `0 < eta < 1` transfers to the ordinary
mean with the same power.

## Physical status

The exact identities, inequalities, and dyadic countermodel are L0.
Their faithful attachment to the literal growing fixed-`h0` affine
packet, including actual masks, prescribed origins, short fibers,
both polarizations, and complete outer reassembly, is an L1
certificate. Proving the required uniform terminal cancellation for
the actual growing Mobius family, over every prefix used by the
dyadic recursion, is an unproved L2 arithmetic task. The reciprocal
weight after translating a fiber must also be transferred by an
exact change of variables or a uniform partial-summation lemma.

The paper does not:

- specialize `h0` to `2`;
- prove a fixed-`h0` Chowla theorem;
- remove averaged-shift, almost-all-scale, or almost-all-origin
  exceptional quantifiers;
- control the bounded-length physical fibers;
- prove a determinant-energy lower bound;
- breach the sieve parity barrier;
- prove a prime-pair lower bound or the twin-prime conjecture.

Every physical route retains the strict endpoint rule

```text
Lambda_phys < 1/400.
```

This is independent of the determinant-flatness compatibility

```text
lambda_D <= 2 eta_Z.
```

A loss is counted in the ledger where it actually occurs and is not
charged twice. Equality or excess in the physical endpoint ledger is
a stop condition.

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

```text
sharp-logarithmic-tauberian-gap.pdf
```
