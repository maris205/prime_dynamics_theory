# Derivation Package

## Target

Attach the complete-period TPC-216 direct-sum envelope to the literal physical
interval

```text
I_x=(x/2,x] intersect Z,  N=|I_x|,
K(n)=sum_(d in D_x)c_d sum_(r mod d)B_d(r)e(nr/d).
```

The target is the normalized finite-window bound

```text
N^(-1) sum_(n in I_x)|K(n)|^2
  <<_psi x^(11/32)(log x)^5,
```

with the corresponding unnormalized exponent `43/32`.

## Status

`COHERENT AS STATED` for the complete common-source cluster object.  This is a
structural finite-window attachment; it is not the final arithmetic Gate-B
theorem.

## Invariant Object

The invariant object is the literal common-source kernel `K(n)`.  The direct-sum
energy and reduced-frequency coefficient energy are proof coordinates for the
same kernel, not replacements for the physical scalar.

## Assumptions

- `H=x^(21/32)`, `Q=x^(1/3)`, `Y0=H/(4Q)`, and `U=x^(133/400)`.
- `Q<q<=2Q` and `D_x={Y0<d<=U: mu(d)^2=1}`.
- `c_d=mu(d)log(d)/d` and `B_d` is the literal reciprocal emitter with
  integer cutoff `floor(dq/H)`.
- The smooth profile is bounded: `M_psi=sup_t |psi(t)|<infinity`.
- `x` is sufficiently large that `4Q<H`, `U<Q`, and `q` is a unit modulo every
  active divisor.
- The standard additive large-sieve inequality is used for frequencies
  separated modulo one by at least `delta`.

## Notation

- `C_h=sum_(d in D_x,h|d)c_d`.
- `N_h=sum_(a mod h,(a,h)=1)|B_h(a)|^2`.
- `S_cluster=sum_(h,a)|C_h B_h(a)|^2` over reduced frequencies.
- `E_direct/L=sum_d |c_d|^2 sum_(r mod d)|B_d(r)|^2`.

## Derivation Strategy

1. Regroup the literal divisor Fourier expansion by reduced rational frequency.
2. Use the exact divisor-dilation covariance from TPC-214 to identify every
   grouped row with `B_h` and every grouped coefficient with `C_h`.
3. Prove a Farey spacing bound for distinct reduced fractions of denominator at
   most `U`.
4. Apply the additive large sieve on the consecutive interval `I_x`.
5. Use the TPC-215 cluster-to-direct majorant and the TPC-216 direct envelope.

## Derivation Map

1. `K(n)` depends on all divisor rows.
2. Reduced-fraction regrouping is an exact identity and uses no approximation.
3. The large-sieve step is a proposition about the finite interval and the
   reduced frequency set.
4. The coefficient-energy majorant is inherited from TPC-215 and the direct
   row envelope from TPC-216.
5. The only logarithmic loss added at this stage is the `O((log x)^2)` cluster
   majorant from TPC-215.

## Main Derivation

### Step 1: Exact reduced-frequency regrouping

For `r mod d`, write `g=(r,d)`, `h=d/g`, and `a=r/g`.  Then `a/h` is in lowest
terms, and every reduced frequency `a/h` occurs in precisely the rows with
`h|d`.  The exact dilation identity

```text
B_d((d/h)a)=B_h(a)
```

therefore gives

```text
K(n)=sum_(h<=U) sum_(a mod h,(a,h)=1)
        C_h B_h(a)e(na/h).
```

The `h=1` row is the additive zero axis; it vanishes in the source range.

### Step 2: Frequency spacing

Two distinct reduced fractions with denominators at most `U` differ modulo one
by a nonzero rational whose denominator divides a product at most `U^2`.
Consequently their circular separation is at least `U^(-2)`.

### Step 3: Finite-window inequality

For coefficients `z_(h,a)=C_hB_h(a)`, the additive large sieve gives

```text
sum_(n in I_x)|K(n)|^2
  <= (N+U^2)sum_(h,a)|z_(h,a)|^2.
```

This is the finite-window attachment.  It preserves the full signed `C_h`
before the square; no independent divisor replacement is made.

### Step 4: Coefficient energy

TPC-215 gives

```text
sum_(h,a)|C_hB_h(a)|^2
  <= A_x E_direct/L,
  A_x=O((log x)^2).
```

TPC-216 gives

```text
E_direct/L <<_psi (Q^3/H)(log U)^3
             = x^(11/32)(log x)^3.
```

Hence

```text
sum_(h,a)|C_hB_h(a)|^2
  <<_psi x^(11/32)(log x)^5.
```

### Step 5: Exponent return

Since `U^2/x=x^(-67/200)` and `N asymp x`, the finite-window loss is bounded
by a constant factor.  Thus

```text
N^(-1) sum_(n in I_x)|K(n)|^2
  <<_psi x^(11/32)(log x)^5,
```

and the unnormalized window energy is `<<_psi x^(43/32)(log x)^5`.

## Remarks and Interpretation

- The theorem controls the finite-window off-frequency Gram by spacing, not by
  free orthogonality.
- The `U^2` term is the exact large-sieve boundary cost at this resolution.
- The result is stronger than a complete-period statement for the common-source
  cluster object, but it does not provide Möbius cancellation or prime-shell
  cancellation.

## Boundaries and Non-Claims

- This is not an arithmetic `L2` estimate for the original Gate-B residual.
- It does not prove the prime-only shell/four-packet reassembly needed by the
  final scalar compiler.
- The aligned finite fixture shows that a one-point window cannot be replaced by
  a diagonal sum; the large sieve is needed for a genuine long interval.
- No twin-prime conclusion follows.

## Open Risks

- The inherited TPC-215 majorant is unsigned and costs `O((log x)^2)`.
- A future arithmetic theorem may need a bound that preserves more cancellation
  than this structural large-sieve attachment retains.
