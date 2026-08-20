# Proof Package

## Claim

Let `D` be a finite family of squarefree moduli, let `Q` be a common set of
integers coprime to every modulus in `D`, and let `H >= 1`.  Define the
unweighted reciprocal emitter

```text
B_d(r) = sum_(q in Q) sum_(0<|m|<=d q/H)
         psi(H m/(d q)) 1_(m q^(-1) == r mod d).
```

For a complete period `L=lcm(D)`, write

```text
c_d = mu(d) log(d)/d,
K_d(u) = sum_(r mod d) c_d B_d(r) exp(2*pi*i*r*u/d).
```

Assume `max(Q) < H`, so the zero frequency is absent.  Then

```text
sum_(u mod L) |sum_(d in D) K_d(u)|^2
 = L sum_(h|L) |C_h|^2
       sum_(u mod h, gcd(u,h)=1) |B_h(u)|^2,
C_h = sum_(d in D, h|d) c_d.
```

The row `B_h` is defined by the same emitter formula even if `h` is only a
divisor of an active modulus and is not itself in `D`.

## Proof

For `h|d`, set `d=k h`.  In the row `B_d(k r)`, the congruence

```text
m q^(-1) == k r mod k h
```

is equivalent to `m=k n` and `n q^(-1)==r mod h`.  The range changes from
`|m|<=k h q/H` to `|n|<=h q/H`, and the smooth argument satisfies

```text
H m/(d q) = H k n/(k h q) = H n/(h q).
```

Therefore `B_d(k r)=B_h(r)` exactly.  A rational frequency with reduced
denominator `h` has the form `u/h` with `gcd(u,h)=1`.  Every active divisor
contributing that frequency is a multiple of `h`, and dilation covariance makes
all its row amplitudes equal to `B_h(u)`.  Complete-period Fourier
orthogonality kills distinct rational frequencies and gives the displayed
cluster sum.

The zero frequency would be the `h=1` term.  If `q<H`, then
`|m|<=d q/H<d`, so `d|m` is impossible for nonzero `m`; hence `B_d(0)=0`.

## Four-packet extension

The identity is linear in any external packet index.  In particular, if
`a^(j)=beta+i^j w` and `omega_j=i^j/4`, then each quadratic packet may be
clustered first and the exact polarization

```text
1/4 sum_(j=0)^3 i^j |beta+i^j w|^2 = beta conjugate(w)
```

may be applied afterwards.  This preserves the four-packet signs; it does not
turn the resulting polarized scalar into a positive quantity.

## Finite certificates

The certificate uses `psi(t)=(1+t^2)^(-2)`, `Q={11,13,17}`, and `H=40`.
The family `{5,7,35}` has a weighted physical/direct-sum energy ratio below
one, while `{3,5,7,105}` has a ratio above one.  Thus the exact cluster reduction
is real, but its sign is not universal.

The sign directions are exact.  For `{5,7,35}`, the `(5,7)` cross Gram is zero
and the two nonzero cross terms pair negative prime coefficients with the
positive coefficient of `35`; hence the total cross contribution is strictly
negative.  For `{3,5,7,105}`, all four Mobius coefficients are negative, every
cross Gram is nonnegative, and a nested pair has positive cross Gram; hence the
total cross contribution is strictly positive.  Only the displayed decimal
ratios are `NUMERICAL_OBSERVATION`.

No asymptotic estimate, prime-shell reassembly, Gate-B payment, fixed-atom
credit, or twin-prime conclusion follows from this package.
