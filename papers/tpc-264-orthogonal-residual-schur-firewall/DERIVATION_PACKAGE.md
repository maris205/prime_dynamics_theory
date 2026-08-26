# TPC-264 derivation package

## 1. Common-clock notation

Keep the literal V59 Hilbert-space object from TPC-263.  Write `g_x=A_x beta`
and let `P=P_3` be the exact rank-three projection onto the source-only frame
`span(z_0,z_1,z_2)`.  Set

```text
p=Pw,       q=Pg_x,
u=(I-P)w,   v=(I-P)g_x.
```

The four terms obtained by expanding `<p+u,q+v>` have two zero mixed terms,
because `range(P)` and `ker(P)` are orthogonal.  Thus

```text
<w,g_x>=<p,q>+<u,v>.
```

TPC-263 controls the first term through the rank-three channel.  TPC-264
studies the second term without silently replacing it by zero.

## 2. Residual Gram matrix

Let `a=||u||` and `b=||v||`, and put `z=<u,v>`.  The two-vector residual Gram
matrix is

```text
Gamma(z) = [[a^2, z], [conjugate(z), b^2]].
```

It is positive semidefinite, so its determinant gives

```text
|z|^2 <= a^2 b^2.
```

This is the Schur bound.  The important question is whether every admissible
`z` can actually be realized while keeping `a` and `b` fixed; the answer is
dimension-dependent.

## 3. Exact realization

If `ker(P)` has dimension at least two and `a,b>0`, choose orthonormal `e_1,e_2`
in the complement and set

```text
u=a e_1,
v=b (conjugate(z)/(a b)) e_1
  + b sqrt(1-|z|^2/(a^2 b^2)) e_2.
```

With the conjugate-linear-first-slot convention this gives `<u,v>=z` after
choosing the phase in the first coefficient consistently.  A direct
coordinate calculation is preferable in the proof: for `z=re^{i theta}` use
`v=b(r/(ab)e^{i theta}e_1 + sqrt(1-r^2/(a^2b^2))e_2)` and conjugate the phase
if the slot convention is reversed.  Every point in the disk is therefore
attained.  If the complement is one-dimensional, Cauchy--Schwarz is always an
equality and `|z|=ab`; if it is zero-dimensional, `z=0`.

## 4. Full scalar geometry

Let `c=<p,q>`.  The full scalar is `c+z`.  Therefore its feasible set is:

```text
closed disk {y: |y-c|<=ab},      dim ker(P)>=2,
circle       {y: |y-c|=ab},      dim ker(P)=1 and ab>0,
singleton    {c},                dim ker(P)=0 or ab=0.
```

This is an exact conditional theorem, not an estimate for the actual prime
shell.  It identifies the missing datum in TPC-263: a bound on `ab` alone
shrinks the radius, while a signed residual theorem must locate `z` inside the
disk.

## 5. Endpoint-budget consequence

If a permitted structural class allows `a,b` both of size `x^(5/6)`, then the
Schur radius has size `x^(5/3)`.  Even if TPC-263 makes `c` smaller than every
fixed logarithmic power, the disk still contains points of full `x^(5/3)`
size.  This establishes a precise structural firewall:

```text
rank-three log control + norm-only residual data
    does not imply a positive fixed-power saving.
```

To pay TPC-261's strict endpoint gap, a future theorem must supply a residual
radius saving `ab << x^(5/3-delta)` with `delta>1/400` after losses, or an
equally strong phase/cross-Gram estimate.  The scale statement is a modeling
choice for the synthetic witness, not a claim about literal V59 residual norms.
