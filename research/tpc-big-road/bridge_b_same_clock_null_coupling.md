# Bridge B V112: same-clock null-channel coupling

Date: 2026-08-26

Status: `PROVED_SOURCE_BACKED_SAME_CLOCK_NULL_CHANNEL_SUPPRESSION_FOR_LITERAL_V59_SIGNED_COUPLING`

TPC-259 is the direct continuation of TPC-258.  It places the source-frozen
transverse null direction and the physical hybrid residual on one literal
V59 clock, then decomposes the signed coupling without hiding the orthogonal
remainder.

## 1. Literal same-clock data

Use

```text
I_x=(x/2,x] intersect Z,
w(u)=Lambda(u+2)-b_x^(Z_x)(u),
Z_x=(log x)^K,
C_x=<w,A_x beta>.
```

Split `I_x` into the four consecutive blocks `B_1,...,B_4` inherited from
the two ordered rank children.  The two within-child normalized Haar vectors
are `z_1=h(B_1,B_2)` and `z_2=h(B_3,B_4)`.  With

```text
L_1=log(3456/3125),
L_2=log(884736/823543),
L_T=(L_1^2+L_2^2)^(1/2),
z_null=(L_2 z_1-L_1 z_2)/L_T,
```

`z_null` is an exact source-only unit vector.  It is selected before reading
`w`, `beta`, or the output.

## 2. New source-backed channel theorem

TPC-254's nonnegative maximal Type-I row applies to every active consecutive
interval.  Applying it to each of the four blocks gives, for every fixed
finite `K` and every fixed `M>0`,

```text
|<z_null,w>| <<_(M,K) sqrt(x)/(log x)^M.
```

TPC-258 supplies the same-clock source-backed diagonal cancellation

```text
<z_null,A_x beta>=o(x^(7/6)/log^3(x)).
```

With `c_x=<z_null,w>` and

```text
w_parallel=c_x z_null,
w_perp=w-c_x z_null,
```

the conjugate-linear-first-slot convention gives the exact identity

```text
<w,A_x beta>
 =conjugate(c_x)<z_null,A_x beta>
  +<w_perp,A_x beta>.
```

Therefore the explicitly identified rank-one channel obeys

```text
conjugate(<z_null,w>)<z_null,A_x beta>
 =o(x^(5/3)/log^(M+3)(x)).
```

The exponent ledger is

```text
1/2+7/6=5/3=80/48,
1/2+55/48=79/48,
80/48-79/48=1/48.
```

## 3. Claim firewall

```text
TPC259_MAXIMUM_CLAIM = PROVED_SOURCE_BACKED_SAME_CLOCK_NULL_CHANNEL_SUPPRESSION_FOR_LITERAL_V59_SIGNED_COUPLING
TPC259_ROUTE_ADVANCE = YES_SCOPED_NULL_CHANNEL
TPC259_ARITHMETIC_ADVANCE = YES_SCOPED_SIGNED_COUPLING_CHANNEL
TPC259_W_NULL_MOMENT = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER
TPC259_NULL_CHANNEL = PROVED_SOURCE_BACKED_o_ONE
TPC259_RESIDUAL_DECOMPOSITION = PROVED_EXACT
TPC259_RESIDUAL_FULL_SCALAR = OPEN
TPC259_FIXED_POWER_SAVING = NONE
TPC259_L2 = NONE
TPC259_FULL_GATE_B = OPEN
TPC259_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC259_FIXED_ATOM_CREDIT = 0
TPC259_TWIN_PRIME_RESULT = NONE
TPC259_STATUS = PROVED_SOURCE_BACKED_SAME_CLOCK_NULL_CHANNEL_SUPPRESSION_FOR_LITERAL_V59_SIGNED_COUPLING
```

The residual `<w_perp,A_x beta>` is not controlled by this theorem.  The
finite real zero-diagonal witness

```text
z=(1,0), w=(0,1), beta=(1,0),
A=[[0,0],[lambda,0]]
```

has zero null channel and full scalar `lambda`.  It is a structural witness,
not a literal prime-shell counterexample; it prevents promotion by projection
algebra alone.

## 4. Route evaluation and next clue

Strongest positive result: the source-frozen null rank-one channel of the
literal signed coupling is arbitrarily log-small on the same clock.

Strongest obstruction: the orthogonal residual can carry the whole signed
scalar even when the null channel is exactly zero in a finite zero-diagonal
model.

Open theorem: control `<w_perp,A_x beta>` or reassemble all four signed
packets while retaining the residual explicitly.  No arithmetic `L2`, full
Gate B, strict global `1/400`, fixed atom, or twin-prime result is paid.

Reusable structure:

```text
same clock -> four-block Haar null -> source-backed w moment
-> exact rank-one split -> residual firewall
```

`ROUND2_CLUE = AUDIT_FULL_FOUR_PACKET_SIGNED_REASSEMBLY_WITH_THE_ORTHOGONAL_RESIDUAL_EXPLICITLY_PRESENT`

The named Session Route-A/Route-B evaluator files are absent from this
checkout.  The project proof package, theorem ledger, local bridge checker,
and `AGENTS.md` are the available fail-closed evaluation authority.
