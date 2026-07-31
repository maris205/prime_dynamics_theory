# RH-325: Moving-order Duhamel composition criterion

This paper separates two composition problems that were still conflated after
RH-324.

For Markov kernels `P_j` and affine reference kernels `Q_j`, retaining the
whole coordinate path gives the exact hybrid-term norms

```text
int incoming_(j-1)(dx) * ||P_j(x,.) - Q_j(x,.)||_1.
```

Their sum, plus the entrance-law error, bounds the complete path-law error;
every endpoint marginal is smaller by contraction.  Therefore, if the number
of legs is `O(k)`, every transported row error is `O(sigma)`, and phases are
matched, the unweighted Markov error is

```text
O(k*sigma) = o(k*R^(-2k))
```

on the natural first-alias clock.

Two sharp obstructions delimit this criterion:

1. A two-state example has zero local error at the original seed but maximal
   error after a preceding transport.  Same-seed marginal accuracy is not a
   composable hypothesis.
2. For `P_n = I` and
   `Q_n = (1-1/n)I + (1/n)S_n`, with `S_n` the cyclic shift, the maximum
   Markov-row error and retained uniform path error are `2/n`, the uniform
   endpoint error is zero, but the trace gap is exactly one.  No
   dimension-free Markov-to-trace bound exists.

For a bounded trace observation and bounded intermediate products, the exact
operator Duhamel identity gives a separate weighted criterion.  If its
stability weight grows like `sigma^(-gamma)` while every local operator error
is `O(sigma)`, the sharp sufficient window is

```text
gamma < 1 - log(1.4)/log(lambda)
      = 0.3503698834605293...
```

The RH-18 quarter-power conditioning exponent would leave
`0.1003698834605293...` of power slack if it were also an applicable upper
bound.  RH-18 proves only a lower bound, so this comparison does not close the
actual trace estimate.

RH-324 controls only one physical leg.  The second critical leg, all-leg phase
transport, observation norms, parity, the neighboring shell, and the joint
first-alias trace law remain open.  Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf moving-order-duhamel-composition-criterion.pdf
```
