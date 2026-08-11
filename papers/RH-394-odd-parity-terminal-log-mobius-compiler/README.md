# RH-394: Odd-Parity Terminal-Log Möbius Compiler and the Complete Three-Shift Table Law

RH-394 proves a fixed-data terminal-logarithmic compiler for
coordinatewise-quadratic Möbius monomials whose odd-exponent support has size
zero, two, or any positive odd integer. Every admitted nonempty odd channel
cancels. The all-even channels converge to exact phasewise squarefree
densities.

The frozen manuscript artifacts are `main.tex`, `references.bib`, `main.pdf`,
and `main.log`. The semantic publication PDF
`odd-parity-terminal-log-mobius-compiler-and-complete-three-shift-table-law.pdf`
is byte-identical to `main.pdf`.

## Main theorem

Fix `m,q`, pairwise-distinct integer shifts `a_i`, fixed `q`-phase
coefficients, and any terminal clock `1<=omega(X)<=X` with
`omega(X)->infinity`. For `alpha in {0,1,2}^m`, write

```text
O(alpha)={i:alpha_i=1},  E(alpha)={i:alpha_i=2}.
```

The compiler admits exactly

```text
|O(alpha)| in {0,2} union {positive odd integers}.
```

The normalized terminal sum has limit

```text
sum_(r mod q) sum_(alpha in {0,2}^m)
  c_alpha(r) Theta_(q,r)(E(alpha)).
```

For the distinct set `B_p(E)={a_i mod p^2:i in E}`,
`nu_p=|B_p|`, and the post-deduplication collision count
`tau_(p,E)(r)=#{b in B_p:b=r mod p}`,

```text
Theta_(q,r)(E)
 =q^-1 prod_(p not|q)(1-nu_p/p^2)
       prod_(p||q)(1-tau_(p,E)(r)/p)
       prod_(p^2|q) 1_(r mod p^2 notin B_p).
```

Thus `Theta_(q,r)(empty)=1/q`, and summing phases gives
`kappa_E=prod_p(1-nu_p/p^2)`.

## Table laws and exact counts

The admitted dimension is

```text
D'_m=2^m+binom(m,2)*2^(m-2)+(3^m-1)/2.
```

For a table `f` on `{-1,0,+1}^m`, let `h_S` be its Boolean restriction to
support stratum `S`. The table is covered exactly when the antipodally even
part `h_S^+` has Fourier degree at most two on every stratum. Its limit is

```text
sum_(r mod q) sum_(U subset [m]) Pi_(q,r)(U) average_signs(f_(r,U)),
Pi_(q,r)(U)=sum_(W subset [m]\U)(-1)^|W| Theta_(q,r)(U union W).
```

Here `Pi>=0` and `sum_U Pi_(q,r)(U)=1/q`. Since `D'_3=27`, every fixed
three-shift ternary table is covered; all `2^(27q)` sign-table phase families
have the exact law. For `m=4`, only `c1111` is missing. Exactly
`binom(16,8)*2^65` sign tables per phase satisfy `c1111=0`.

For a distinguished-current score `g(x,z)=z*f(x)`, eligibility is equivalent
to Fourier degree at most one for the odd part of every input stratum. Set

```text
M_0=2, M_1=4,
M_k=2^(2^(k-1))+2k+4*binom(k,2)*2^(2^(k-2))  (k>=2),
B_d=prod_(k=0)^d M_k^binom(d,k).
```

All `B_d^q` fixed phase families cancel. In particular,
`B_2=512` and `B_3=36,700,160`.

## Exact finite artifact

The 658 certificate rows have partition
`81+17+512+8+8+8+8+8+8`. They record all four-variable monomials, the
signed-four-cube histogram, all two-input current tables, dimension rows,
stratum tests, current counts, phase inversion, analytic interfaces, and
firewalls. The builder-independent false verifier rejects 32 named semantic
mutations.

The canonical certificate is 108,636 bytes with SHA-256
`3c72e7fbb74a35e8b84a1e75ed56b05ea04892a522d8b4a89c51ba21cedf8998`.
The stored result is 241,215 bytes with SHA-256
`935de4967e504e5c32f6d27980ec044c3cffccfbab534440730470de8b1ae610`.
The closed Draft 2020-12 schema is 1,172,382 bytes with SHA-256
`8129ae146b30ca617e8536c15101eee6e12965ac9a87a6c41be9eb472cf16cb3`.

## Reproduction

Install `requirements.txt`, then run:

```text
make result
make schema
make test
make test-optimized
make remote
make pdf
make archive
```

`make remote` performs strict local-lock verification only. All four rows
return `NETWORK_DISABLED`, `network_opt_in=false`, and `requests_made=0`.

## Immutable source closure

The direct predecessor is RH-393 commit
`6fed36f44183a2794a3a814493ff602c5dc9314b`. The release-bound Git closure
has 128 objects in groups `117+8+3`, with digests

```text
bdf6c835c5871a9ed9b62cb32ff5b02c0c0a4dd72a0728ae13939144c5e0560d
588f23297c3bd3f6efd707acd112e70be652e86f4ea007da3f9704e8820795ac
e379426b2ac1167a49e7014f133cd701c73b6be60889b807efdd20b43db08439
```

The all-Git digest is
`90f427889b714a7544e4eb68e6df565e32dab4114e656d99f7a24074a7a56951`.
Four ordered remote lock objects bring the closure to `128+4=132`, with
logical digest
`07c9ed6c0c79d77098e19d8102b4267ea4af637ae2d72148c412cc626af738ac`.

Tao--Teräväinen is the new direct odd-parity input. Tao 2016 is inherited
two-point provenance; Johnston--Yang and Maynard are closure-only. The ordered
redistribution flags are `false,false,true,false`. No external PDF is
vendored, and all six sealed payload identities are excluded from publication
members and the complete RH-394 tree.

## Release boundary

The publication manifest contains 39 members; manifest and verification
report bring the release-stage set to 41. Gates cover frozen Stage-1 and
manuscript hashes, fresh result/schema/manifest/report equality, official
Draft 2020-12 validation, 128+4 source identity, rights, four zero-request
replays, semantic-PDF identity, six-payload exclusion, and whole-tree hygiene.

No result is claimed for even odd-support size at least four, unrestricted
tables once `m>=4`, growing data, effective rates, ordinary Cesàro averages,
prelimit maxima, graph-coupled capacity, operators, traces, or zeros. Gates
A--E remain false.
