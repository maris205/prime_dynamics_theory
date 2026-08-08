# RH-389: Active-c11 Terminal-Log All-Clock Capacity

RH-389 proves an unconditional terminal-logarithmic capacity theorem for
active `c11` in every individually fixed periodic clock.  A pointwise
projection reduces all 512 lag-two truth tables to eight actions; an
injective predecessor charge then shows that every fixed clock has the
same absolute capacity.

The paper and semantic publication PDF are:

- `main.tex`, `references.bib`, and `main.pdf`;
- `active-c11-terminal-log-all-clock-capacity.pdf`, byte-identical to
  `main.pdf`.

## Main theorem

For a fixed integer `q>=1`, a fixed universally distance-two-safe
`q`-periodic table family `f`, and any function
`1<=omega(X)<=X` with `omega(X)->infinity`, define

    S_X^omega(q,f)
      = (log omega(X))^-1
        sum_(X/omega(X)<n<=X)
        mu(n) f_(n mod q)(mu_0(n-2),mu(n))/n.

Then the limit exists and equals

    L_q(f)=sum_(r mod q)
           [c02(r) delta_(q,r)+c22(r) theta_(q,r)].

The active `c11` channel vanishes by the determinant-two terminal-log
input frozen in TPC-137.  The other oscillatory channels vanish by Abel
transfer of their prefix cancellation.  With `A_q` the finite family of
safe tables,

    G_log(q):=max_(f in A_q)|L_q(f)|
             =6/pi^2-kappa_2/2

for every fixed `q`.  The constant action `{-1,0}` (table 36) attains the
positive value for every fixed clock; its input reflection (table 72)
attains the negative value.  Only after all fixed-clock limits are formed,

    sup_(fixed q>=1) G_log(q)=6/pi^2-kappa_2/2.

This is not a simultaneous growing-`q` or max-before-limit assertion.

## Exact artifact

The certificate has 602 rows:

    512 truth-table rows
      8 projected-action rows
     64 directed-compatibility rows
      8 predecessor-charge rows
      6 analytic-interface rows
      4 scope rows

Its epistemic role is `finite_reproduction_not_analytic_proof`.  The
canonical certificate is 208,648 bytes with SHA-256
`b31187db4ea284152b0c1cb895439e29cfa80a4e564c87814ee182f87be0a020`.
All 24 genuine semantic mutations are rejected by independent field-level
validation.  The `compare_fresh=false` path does not call the certificate,
group, or contract builders.

`results/result.json` is 489,106 bytes with SHA-256
`3c551568aab4e0965b2b0236d9f684e1f953dc36ecbc575e6e007c5f15bfd310`.
The recursively closed official Draft 2020-12 schema is 3,133,596 bytes
with SHA-256
`763d25bae19d35b36578619bd50aa79cc8121a73c543f8b051e54200e16445ec`.

## Reproduction

Install `requirements.txt`, then run:

    make result
    make schema
    make test
    make remote
    make pdf
    make archive

`PYTHON=...` may select another interpreter.  `make remote` invokes the
three frozen verifiers in default-offline mode and performs zero network
requests.  Network access is always explicit:

    make remote-network-jy
    make remote-network-maynard
    make remote-network-tao
    make remote-network

Retrieved bytes are never persisted in this publication tree.

## Source closure and redistribution boundary

The immutable closure contains 95 Git blobs: 77 inherited RH-388 rows,
eight RH-388 standard release files, two RH-388 remote-lock blobs, and
eight TPC-137 release files.  The ordered Git digest is
`b7ff5b520d5e926f19346a1ac6e49fbccf07c5fe24de60758179e9959e673353`.

Three ordered remote logical objects give 98 logical inputs in total.
Their logical digest is
`99a9e6d4372a081b028c28acba7de539850b4092b64063d9553ca261809e3e74`.
Johnston--Yang and Maynard are inherited closure-only objects, not RH-389
proof inputs.  TPC-137 is the full Mobius-correlation input; Tao's theorem
is its upstream Liouville provenance.  All five remote payload hashes are
absent from the publication members and the entire RH-389 tree.

## Claim boundary

RH-378 already recorded the same constant and witness for `q=1` under an
ordinary-Cesaro correlation hypothesis.  RH-389's new edge is the
unconditional terminal-log active-periodic theorem and the all-fixed-clock
charge.  There is no ordinary Cesaro theorem, growing or `X`-dependent
clock, uniform unbounded-clock limit, adaptive max-before-limit, `K_N`,
operator, trace, zero identification, or RH claim.  Gates A--E are false.
