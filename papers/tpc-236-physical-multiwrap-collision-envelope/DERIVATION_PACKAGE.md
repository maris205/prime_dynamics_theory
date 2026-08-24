# TPC-236 derivation package

## 1. Physical atoms

For `Q<q<=2Q` prime and `h<=Q`, define

\[
S_{h,q}=\{a\pmod h:\ a=mq^{-1}\pmod h,
\ 0<|m|\le\lfloor hq/H\rfloor\}.
\]

At V59, `H=x^(21/32)`, `Q=x^(1/3)`, and `h<=U=x^(133/400)<Q`.

## 2. Internal injectivity

If `4Q<H`, then two allowed multipliers in one row satisfy

\[
|m-m'|<4hQ/H<h.
\]

Hence congruence modulo `h` forces `m=m'`.

## 3. Gcd-fiber count

Fix `a mod h`, set `g=(a,h)`, and put `M_h=floor(2hQ/H)`.  Every atom in bucket `a`
satisfies `(m,h)=g`.  There are at most `2 floor(M_h/g)` possible signed multipliers.
The zero residue has `g=h` and no nonzero atom because `M_h<h`.  For a nonzero residue
and one such `m`, division by `g` gives one residue class

\[
q\equiv (a/g)^{-1}(m/g)\pmod{h/g}.
\]

An interval of length `Q` contains at most `ceil(Qg/h)` integers in that class.  Thus

\[
R_h(a)\le2\left\lfloor\frac{M_h}{g}\right\rfloor
\left\lceil\frac{Qg}{h}\right\rceil.
\]

Using `M_h<=2hQ/H`, `h<=Q`, and `g>=1` gives

\[
R_h(a)\le \frac{4Q^2}{H}+\frac{4hQ}{gH}
\le\frac{8Q^2}{H}.
\]

Because physical V59 denominators satisfy `h<=U`, the sharper source-scale form is

\[
R_h(a)\le4x^{1/96}+4x^{23/2400}=(4+o(1))x^{1/96}.
\]

## 4. Weighted Bessel compiler

For arbitrary Hilbert-valued rows supported on `S_(h,q)`, pointwise Cauchy gives

\[
\left\|\sum_qc_qv_{h,q}\right\|^2
\le\left(\frac{4Q^2}{H}+\frac{4hQ}{H}\right)
\sum_q|c_q|^2\|v_{h,q}\|^2
\le\frac{8Q^2}{H}\sum_q|c_q|^2\|v_{h,q}\|^2,
\]

where the middle expression maximizes over all active residue gcd fibers; the final
uniform form avoids any dependence on the active support.

Multiplying by explicit `|C_h|^2` and summing in the orthogonal pre-reassembly
`h`-direct sum preserves the same factor.  A common linear packet transform `T` costs
only its explicit operator norm squared and preserves polarization.

## 5. V59 exponent

\[
Q^2/H=x^{2/3-21/32}=x^{1/96}.
\]

This is a structural energy toll, not an arithmetic saving.

## 6. Triple collision

For `(Q,H,h)=(101,8830,80)`, exact integer-power comparisons give
`H=floor(Q^(63/32))` and `h<=floor(Q^(399/400))=99`.  The rows
`q=113,127,193` all have cutoff one and support `{17,63}`.  Their equal-coefficient
energy ratio is

\[
\frac{\|v_{113}+v_{127}+v_{193}\|^2}
{\|v_{113}\|^2+\|v_{127}\|^2+\|v_{193}\|^2}=3.
\]
