# TPC-231 proof package

## Theorem A: first-resonance density

Let `P_Q` be the primes in `(Q,2Q)`, let `P(Q)=|P_Q|`, and let `E_3716(Q)` count the
primitive pairs `p<r` in `P_Q` satisfying `7p+3r=16Q`. Then

$$
E_{3716}(Q)\ll\frac{Q\log\log(3Q)}{(\log Q)^2},
\qquad
\frac{E_{3716}(Q)}{P(Q)}\longrightarrow0. \tag{1}
$$

More precisely, when `gcd(Q,21)=1`,

$$
E_{3716}(Q)\ll \mathfrak S_{3716}(Q)\frac{Q}{(\log Q)^2},
\quad
\mathfrak S_{3716}(Q)=C_{3716}
\prod_{\substack{\ell\mid Q\\\ell\ge5}}\frac{\ell-1}{\ell-2}. \tag{2}
$$

If `gcd(Q,21)>1`, the primitive edge set is empty by definition.

### Proof

Suppose `gcd(Q,21)=1`. Write `Q=3t+a`, `a in {1,2}`. The resonance equation modulo
three forces `p=3k+a`, and substitution gives

$$
L_1(k)=3k+a,\qquad L_2(k)=16t+3a-7k. \tag{3}
$$

Their determinant is `3(16t+3a)+7a=16Q`. TPC-229's endpoint inequalities place `k`
in an interval of length `2Q/35+O(1)` and ensure both form values lie in `(Q,2Q)`.

Let `nu_Q(ell)` count the residue classes modulo a prime `ell` on which
`L_1(k)L_2(k)=0`. Modulo two, both forms equal `k+a`, so `nu_Q(2)=1`. Modulo three,
`L_1=a` is nonzero and `L_2` has one root. Modulo seven, `L_2` is constant; it is
nonzero because three times that constant is `2Q mod 7`, while `L_1` has one root.
For `ell` outside `{2,3,7}`, both forms have one root, and those roots coincide if and
only if their determinant vanishes. Therefore

$$
\nu_Q(\ell)=1\quad(\ell\in\{2,3,7\}\text{ or }\ell\mid Q),
\qquad \nu_Q(\ell)=2\quad\text{otherwise}. \tag{4}
$$

In particular the pair is admissible. For squarefree `d`, the Chinese remainder
theorem and interval counting give

$$
\#\{k\in I_Q:d\mid L_1(k)L_2(k)\}
=\frac{|I_Q|\nu_Q(d)}d+O(\nu_Q(d)). \tag{5}
$$

Apply the standard Selberg upper-bound sieve of dimension two to (5), with a fixed
small power of `Q` as sieve level. This gives the first estimate in (2), uniformly in
`Q`; the interval remainder in (5) is the usual `O(2^{omega(d)})` remainder. Formula
(4) gives the displayed singular series: replacing a generic two-root Euler factor by
a one-root factor at `ell|Q` multiplies it by `(ell-1)/(ell-2)`. The fixed factors at
`2,3,7` are absorbed into the positive constant `C_3716`.

Finally,

$$
\frac{\ell-1}{\ell-2}
=\frac{\ell}{\ell-1}
\left(1+\frac1{\ell(\ell-2)}\right).
$$

The product of the second factors is absolutely convergent, while the first product is
at most `Q/phi(Q)<<log log(3Q)`. This proves the first assertion in (1). The prime
number theorem gives `P(Q)~Q/log Q`, proving the density limit. ∎

## Theorem B: fixed finite linear resonance families

Fix finitely many triples `(a_j,b_j,c_j)` with positive coprime `a_j,b_j` and nonzero
`c_j`. The total number of prime-shell solutions of

$$
a_jp+b_jr=c_jQ
$$

over all fixed indices `j` is `O(Q log log(3Q)/(log Q)^2)=o(P(Q))`.

### Proof

For one triple, either the congruence has no solutions, or every solution is
parameterized as `p=p0+b_j k`, `r=r0-a_j k`. The determinant is
`b_j r0+a_j p0=c_jQ`. Outside a fixed set of primes dividing the coefficients, the
two local roots coalesce only at primes dividing `c_jQ`. The same Selberg sieve used in
Theorem A yields the asserted bound, with a constant depending on the fixed triple.
An inadmissible local system contributes no large prime pairs. Sum over the fixed finite
set of triples. ∎

## Proposition: bounded-degree energy transfer

Let a collision energy have the form

$$
E_{AP}=D+2\Re\sum_{\{p,r\}\in E(G_Q)}c_{p,r}\langle u_p,u_r\rangle,
$$

where `|c_{p,r}|<=C`, the graph degree is at most `Delta`, and positive row masses
have fixed ratio at most `kappa`. If `M_inc` is the mass on incident vertices, then

$$
\frac{(D-E_{AP})_+}{D}
\le C\Delta\frac{M_{inc}}D
\le2C\Delta\kappa\frac{|E(G_Q)|}{P(Q)}. \tag{6}
$$

Indeed, `2|<u_p,u_r>|<=||u_p||^2+||u_r||^2`; summing charges each incident vertex at
most `Delta` times. The second inequality follows from at most `2|E|` incident
vertices and row comparability. Every fixed linear resonance equation has degree at
most two, hence a fixed finite family has fixed `Delta`. Theorem B makes the right
side `o(1)`.

## Corollary: mass obstruction

In the TPC-230 literal aligned first-resonance model,

$$
\frac{M(Q)}{D(Q)}\le8\frac{E_{3716}(Q)}{P(Q)}=o(1). \tag{7}
$$

Hence even perfect anti-alignment on every first-resonance edge cannot yield a fixed
positive proportional saving for all sufficiently large `Q`; in particular it cannot
pay strict `1/400`.

## Claim boundary

Theorems A and B are asymptotic arithmetic upper bounds and the corollary is exact in
the already-defined literal aligned model. They do not identify that model with actual
V59 source masses, do not control a resonance family whose depth grows with `Q`, and do
not prove cancellation or full Gate B. The finite scan is reproduction evidence only.
