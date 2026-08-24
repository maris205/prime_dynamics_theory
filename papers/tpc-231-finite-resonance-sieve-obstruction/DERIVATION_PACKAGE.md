# TPC-231 derivation package

## 1. Exact two-form parameterization

Assume `gcd(Q,21)=1` and write `Q=3t+a`, where `a` is `1` or `2`. Reduction of
`7p+3r=16Q` modulo three gives `p=a (mod 3)`, so `p=3k+a` and

$$
r=16t+3a-7k.
$$

The coefficient determinant is

$$
3(16t+3a)+7a=16Q. \tag{D1}
$$

TPC-229's endpoint theorem restricts the parameter to an interval of length
`2Q/35+O(1)`.

## 2. Local root law

Let `nu_Q(ell)` be the number of `k mod ell` for which one of the two forms vanishes.

- At `ell=2`, the forms coincide and have one root.
- At `ell=3`, the first form is the nonzero constant `a` and the second has one root.
- At `ell=7`, the second form is a nonzero constant because three times that constant
  is `2Q mod 7`; the first has one root.
- Away from `2,3,7`, both forms have one root, and the roots coincide exactly when
  `ell|16Q` by (D1).

Hence

$$
\nu_Q(\ell)=
\begin{cases}
1,&\ell\in\{2,3,7\}\text{ or }\ell\mid Q,\\
2,&\text{otherwise}.
\end{cases} \tag{D2}
$$

## 3. Singular series

The local product is

$$
\mathfrak S_{3,7}(Q)
=C_{3,7}\prod_{\substack{\ell\mid Q\\\ell\ge5}}
\frac{\ell-1}{\ell-2}. \tag{D3}
$$

For each variable exceptional prime,

$$
\frac{\ell-1}{\ell-2}
=\frac{\ell}{\ell-1}
 \left(1+\frac1{\ell(\ell-2)}\right). \tag{D4}
$$

The second Euler product converges, while the first is bounded by `Q/phi(Q)`. Thus
`S_3716(Q)<<log log(3Q)`.

## 4. Sieve and shell normalization

The standard Selberg upper-bound sieve for two affine forms on an interval gives

$$
E_{3,7}(Q)\ll
\mathfrak S_{3,7}(Q)\frac{Q}{(\log Q)^2}
\ll\frac{Q\log\log(3Q)}{(\log Q)^2}. \tag{D5}
$$

Since `P(Q)=pi(2Q)-pi(Q)~Q/log Q`, division yields

$$
\frac{E_{3,7}(Q)}{P(Q)}
\ll\frac{\log\log(3Q)}{\log Q}\longrightarrow0. \tag{D6}
$$

## 5. Transfer to the TPC-230 obstruction

TPC-230 proves in the literal aligned model

$$
\frac{M(Q)}{D(Q)}\le8\frac{E_{3,7}(Q)}{P(Q)}. \tag{D7}
$$

Equations (D6)--(D7) imply `M/D->0`. Since the maximum possible saving is at most
`M`, no fixed positive saving survives at all sufficiently large scales.

## 6. Fixed finite families

For fixed coprime positive `a,b` and nonzero fixed `c`, every solution of
`ap+br=cQ` is parameterized by `p=p0+bk`, `r=r0-ak`; the determinant is `cQ`.
The same sieve argument gives `O_{a,b,c}(Q log log(3Q)/log^2 Q)` edges. A fixed
finite union remains `o(P(Q))`. This is a support-density theorem, not an actual V59
source-identification theorem.

Each fixed equation gives degree at most two on the unordered prime-row graph, so a
fixed finite family has maximum degree `Delta=O(1)`. If its collision coefficients are
bounded by `C` and row masses have ratio at most `kappa`, Cauchy--Schwarz gives

$$
\frac{(D-E_{AP})_+}{D}
\le C\Delta\frac{M_{\rm incident}}D
\le 2C\Delta\kappa\frac{E_{\rm total}}P=o(1). \tag{D8}
$$

Thus the fixed-finite-family comparable-row stop is an energy theorem, not merely a
support-count heuristic.
