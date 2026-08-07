# RH-382 adversarial reviewer audit

## Editorial recommendation

**Accept within the declared scope, subject to release replay.** The paper
contains a genuine theorem edge beyond RH-381: it identifies both surviving
quadratic scales and proves a uniform cubic remainder. It does not enlarge
the factor class or promote numerical evidence.

## Independent proof checks

1. **Euler-tail orientation.** The identity is
   `u_m/U_m^(j)=product_tail(1-(m-1)a)`. The manuscript consistently expands
   `U_m^(j)` about `u_m`, not the inverse orientation.
2. **Inverse-product remainder.** From `P<=1/(1+x)` and `1-P<=x`,
   `U-u-xu=U[(1+x)(1-P)-x]` lies in `[0,Ux^2]`.
3. **Numerator ledger.** The five contributions are
   `45/4, 32, 225/4, 72, 245/4`; their sum is `931/4`.
4. **Memory ledger.** The six contributions are
   `3,15/2,12,15,15,21/2`; their sum is `63`.
5. **Terminal indices.** `R8=P E8` is separate. `E9` appears only from the
   length-seven second difference and is exactly zero because of `p=3`.
   No `E10` is used.
6. **H loss.** The normalized loss is `d=T+eta` with
   `-T^2/2<=eta<=0`; the physical factor `4/pi^2` is restored exactly once.
7. **Tail signs.** The numerator uses `(T^2+S)/2`; memory uses
   `(T^2-S)/2`. This yields `Y+2m` on `T^2` and `Y-2m` on `S`.
8. **Cubic ledger.** The numerator is `931/2`. Memory is
   `4*(63/3+1/6)=254/3`. Total `3301/6=550+1/6<551`.

## Adversarial controls

- Changing only memory `-2mS` to `+2mS` at the exact `p=71` one-tail
  endpoint changes the approximation by `4mS` and makes the normalized
  residual `7.335622869337969>1`.
- The correct displayed sign gives `0.042746686479386<1`.
- The paper does not conflate this with flipping numerator `+YS`.
- Source commit, membership, duplicate-row, unsafe-path, digest, non-finite,
  numeric-type, schema, and Gate mutations are tested fail-closed.

## Scope review

No statement crosses from fixed finite clocks to `q(N)`, from phasewise
`c11=0` to active correlations, from finite reproduction to a fitted
asymptotic, or from Euler arithmetic to an intrinsic operator/trace/zero
model. Gates A--E remain false/open.

## Remaining limitations, correctly stated

- The constants are safe, not claimed optimal.
- No relation collapses `S_y` into `T_y^2`.
- No PNT-scale asymptotic is derived.
- The all-order cluster normal form in the roadmap is a candidate only.
- Active phasewise `c11`, adaptive capacity, selected non-Parry measure, and
  strong-space Ulam routes retain their explicit blockers.
