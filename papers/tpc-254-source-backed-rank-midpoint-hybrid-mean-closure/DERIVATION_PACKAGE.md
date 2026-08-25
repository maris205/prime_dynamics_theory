# Derivation Package

## 1. Physical clock and rank split

For real `x`, write

```text
a=floor(x/2), b=floor(x), I_x={a+1,...,b}, N=b-a.
ell=floor(N/2), r=N-ell.
L={a+1,...,a+ell}, R={a+ell+1,...,b}.
```

Thus both children are consecutive active integer intervals even when `x` is
nonintegral. The primary definition is by ordered rank. For example,
`x=27/2` gives `I_x={7,...,13}` and `L={7,8,9}`, whereas
`floor(3x/4)=10`; the integer threshold would select the wrong child.

Put

```text
rho^2=ell*r/N,
h=1_L/ell-1_R/r,
z_mid=rho h.
```

Then `sum h=0` and

```text
rho^2||h||_2^2=(ell*r/N)(1/ell+1/r)=1.
```

The exact projector has rational entries
`(z_mid tensor z_mid)_(i,j)=rho^2 h_i h_j`.

## 2. Source theorem and nonnegative extraction

The frozen hybrid H2 theorem says that for every fixed `gamma<1/2` and every
requested fixed log strength, the maximal Type-I expression

```text
sum_(m<=x^gamma) tau(m)^B max_J
  |sum_(x/2<ms<=x, s in J) w(ms)|
```

is `<< x/(log x)^B`, where every summand is nonnegative and `J` ranges over
active intervals. Freeze `gamma_0=1/4`. For sufficiently large `x`, `m=1`
occurs, has weight `tau(1)^B=1`, and therefore its row is bounded by the
whole nonnegative sum. This yields uniformly for every consecutive
`J subset I_x`

```text
|sum_(u in J)w(u)| <<_(M,K) x/(log x)^M.
```

Taking `J=L,R` gives the two child-sum bounds. No signed extraction occurs.

## 3. Child means and Haar moment

Since

```text
N=x/2+O(1), ell=x/4+O(1), r=x/4+O(1),
```

division by `ell,r` gives

```text
|W_L/ell-W_R/r| <<_(M,K) (log x)^(-M).
```

The parity-exact normalization is

```text
rho^2=N/4                         if N is even,
rho^2=N/4-1/(4N)                  if N is odd.
```

Hence `rho^2=x/8+O(1)` and
`rho=x^(1/2)/(2sqrt(2))+O(x^(-1/2))`. TPC-253's exact identity

```text
<z_mid,w>=rho(W_L/ell-W_R/r)
```

therefore proves

```text
|<z_mid,w>| <<_(M,K) x^(1/2)(log x)^(-M).
```

## 4. Quantifiers and the power firewall

The corollary order is

```text
fixed finite admissible K
-> gamma_0=1/4
-> target M
-> sufficiently strong integer H2 exponent
-> delta<1-gamma_0
-> divisor-tail, BV, and fundamental-lemma choices
-> x>=x_0(M,K).
```

There is no uniformity as `K` grows or as `gamma` approaches `1/2`. The
upstream Ford--Maynard order instead fixes `A,varpi`, then `B_FM`, then
`K=K(B_FM)`, then the large-`x` threshold. Finally, for fixed `eta,M>0`,

```text
[x^(1/2)/(log x)^M]/x^(1/2-eta)=x^eta/(log x)^M -> infinity.
```

Thus the theorem does not imply `x^(1/2-eta)`.

## 5. Adjoint transfer and obstruction

For the literal TPC-247 operator,

```text
<z_mid,A_x beta>=<A_x^*z_mid,beta>,
(A_x^*z_mid)(t)=sum_u conjugate(A_x(u,t))z_mid(u).
```

Cauchy gives

```text
|<z_mid,A_x beta>|<=||A_x^*z_mid||_2||beta||_2.
```

Multiplication with the proved `w` bound yields only a safe upper transfer.
No source-backed cancellation, sign, nonzero value, or saving is available
for the adjoint lane.

For any real unit `z`, a derangement `sigma`, `beta=1`, and real `lambda`, set

```text
A_(i,sigma(i))=lambda z_i,
A_(i,j)=0 otherwise.
```

Then `diag(A)=0`, `A beta=lambda z`, and `<z,A beta>=lambda`. At `N=2`,
`z=(1/sqrt(2),-1/sqrt(2))` gives exact equality in Cauchy. This is a
synthetic norm-only obstruction, not an identification with the V59 matrix.
