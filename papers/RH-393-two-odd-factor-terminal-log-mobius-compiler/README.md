# RH-393: Two-Odd-Factor Terminal-Log Möbius Compiler and the Multi-Shift Squarefree Landscape

RH-393 proves a terminal-logarithmic compiler for every fixed finite set of
distinct integer shifts. Coordinatewise-quadratic monomials with at most two
odd exponents are admitted: one- and two-odd channels cancel, while all-even
channels converge to exact phasewise multi-shift squarefree densities.

The frozen manuscript artifacts are `main.tex`, `references.bib`, `main.pdf`,
and `main.log`. The semantic publication PDF
`two-odd-factor-terminal-log-mobius-compiler-and-multi-shift-squarefree-landscape.pdf`
is byte-identical to `main.pdf`.

## Main theorem

For fixed `m,q`, pairwise-distinct integer shifts `a_i`, fixed periodic
coefficients, and every fixed terminal clock `1<=omega(X)<=X` with
`omega(X)->infinity`, write

```text
O(alpha)={i:alpha_i=1},  E(alpha)={i:alpha_i=2}.
```

For `alpha in {0,1,2}^m` with `|O(alpha)|<=2`, the normalized terminal sum
has limit

```text
sum_(r mod q) sum_(alpha in {0,2}^m)
  c_alpha(r) Theta_(q,r)(E(alpha)).
```

For the distinct set `B_p(E)={a_i mod p^2:i in E}`,
`nu_p=|B_p|`, and `tau_(p,E)(r)=#{b in B_p:b=r mod p}`,

```text
Theta_(q,r)(E)
 =q^-1 prod_(p not|q)(1-nu_p/p^2)
       prod_(p||q)(1-tau_(p,E)(r)/p)
       prod_(p^2|q) 1_(r mod p^2 notin B_p).
```

Residues are deduplicated modulo `p^2` before the modulo-`p` collision count.
Summing phases gives `kappa_E=prod_p(1-nu_p/p^2)`.

## Finite consequences and landscape

The admitted dimension is

```text
D_m=2^m+m*2^(m-1)+binom(m,2)*2^(m-2).
```

Thus `D_3=26`; only the signed-cube coefficient `c111` is excluded. For a
two-input truth table in the distinguished-current score, `c11=0` is the
alternating four-corner condition. Exactly `6*2^5=192` of 512 tables satisfy
it and have zero terminal limit. The remaining 320 tables are outside the
theorem only.

For a fixed distinct configuration `A` of size `m`,
`kappa_A=prod_p(1-|A mod p^2|/p^2)`. If `m<=3`, then
`kappa_A>=C_m=prod_p(1-m/p^2)>0`, with equality exactly when every nonzero
pairwise difference is squarefree. If `m>=4`, zero is attained exactly when
some prime-square residue system is completely covered. For every fixed
`m>=2`, `sup_A kappa_A=6/pi^2`, approached by primorial-square configurations
but never attained.

## Exact artifact

The 576 certificate rows are partitioned as `512+27+8+12+9+8`. They record
the truth-table census, all 27 three-variable monomials, dimension identities,
12 finite-CRT fixtures, nine landscape contracts, and eight analytic
interfaces. The builder-independent verifier rejects 32 semantic mutations.

The canonical certificate is 117,096 bytes with SHA-256
`f109da241722796418f39708b16fa162cce0b85a6e448998d3ede593b7bd697b`.
The stored result is 276,546 bytes with SHA-256
`69ebe2e157f5152d52aac5a478d1dd2ee2abde1dc672ad20941505d7e3a48aea`.
The closed Draft 2020-12 schema is 1,554,266 bytes with SHA-256
`88195a22d2d1ebecff8e8d4cdf860be2b2ef984b93aa94b86861a619369a4790`.

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

`make remote` performs strict local-lock verification only. All three rows
return `NETWORK_DISABLED`, `network_opt_in=false`, and `requests_made=0`.

## Immutable source closure

The closure is rebound to RH-392 commit
`9768c1cb5f56d959406c19119315afd542b6c30f`. It contains 117 Git objects
in groups `106+8+3`, with ordered group digests:

```text
cf36abdfa3a81f8781d86f1bb96747248eced62d2cd83a5e03de7de0c614bc28
5a20f8e8a65fbcf8add5b3c9bb5318527c94a349ca541236603efbcfa86ec8bf
8a69e04cbac166b36834f7b9e21e2cd8799f95d365330143ee261038c7da2863
```

The all-Git digest is
`2c187ec15a427ffb0b06a48679f8419be82152fe16ea914c2a86437549117220`.
Three ordered remote locks bring the closure to `117+3=120`, with logical
digest
`9315d7c01651ed8b4d94f98c3e4019ad11e28469ee6722903721db280b9f92eb`.

Tao's fixed nonparallel two-form theorem is inherited through RH-392. The
Johnston--Yang and Maynard objects are closure-only here. No remote payload is
vendored, and all five sealed payload identities are excluded from publication
members and the complete RH-393 tree.

## Release boundary

The fixed publication manifest contains 38 members; manifest and verification
report bring the release-stage set to 40. Gates cover frozen Stage-1 and
manuscript hashes, fresh result/schema/manifest/report equality, official
schema validation, 117+3 source identity, rights, three zero-request replays,
semantic-PDF identity, payload exclusion, and tree hygiene.

No claim is made for three or more odd factors, unrestricted three-coordinate
truth tables, growing data, ordinary Cesàro averages, effective rates,
pre-limit maxima, generic multishift capacity, operators, traces, or zeros.
Gates A--E remain false.
