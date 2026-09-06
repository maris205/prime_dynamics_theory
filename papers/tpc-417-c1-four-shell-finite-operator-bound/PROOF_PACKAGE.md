# Proof Package

## Claim

For the declared four-shell CRT profile, let `N=4H`, let `D_r` be the exact
local diagonal energy at window coordinate `r`, and let `Z=D^{-1/2}MD^{-1/2}`.
For each `H` in `{16,32,66,128}`, the full finite matrix satisfies

`||Z||_2 <= 2/(a_min sqrt(H)) + 16 |A|/V_minus`,

where `A=P_plus-P_minus` and `V_minus` is the odd-index sum of squared
amplitudes.

## Status

PROVABLE AS STATED (for the finite synthetic proxy and its declared CRT mask).

## Assumptions and notation

- The four complete shells are `Q<p<=2Q` for `Q=65536,131072,262144,524288`.
- Every selected prime exceeds `N`, and the ordered pool has odd cardinality
  `75483`, with `m_minus=37741` and `m_plus=37742`.
- Even-index primes divide the anchor `o`; odd-index primes divide `o+N`.
- `a_i=p_i^3/[Q_i^2(p_i-1)]`, `T_d=H^2/(H^2+d^2)`, and
  `S_r=sum_{s != r} T_{s-r}^2`.
- `P_minus=sum_odd a_i`, `P_plus=sum_even a_i`,
  `V_minus=sum_odd a_i^2`, `V_plus=sum_even a_i^2`, and `a_min=min_i a_i`.

## Proof Strategy

Use the exact diagonal-deletion identity to separate the endpoint star from
the interior bulk.  Bound the normalized star by Cauchy--Schwarz and the
normalized bulk by a symmetric row-sum estimate.

## Dependency Map

1. The CRT mask gives `b_0=P_plus` and `b_r=0` for `r>=1`.
2. The diagonal-deletion identity gives the displayed entries of `M` and `D`.
3. The elementary bounds `S_r>=H/4` and `sum T_d<=4H` control both blocks.
4. Cauchy--Schwarz and the minimum amplitude control the star block.
5. The triangle inequality combines the two blocks.

## Proof

For distinct window coordinates, `|r-s|<N<Q_i<p_i`; hence no selected prime
divides two distinct window points.  The endpoint masks are exactly the
declared ones, and every non-anchor window point is a unit for every selected
prime.  The signed diagonal-deletion identity consequently gives
`M_{rs}=T_{r-s}(-A+b_r+b_s)`, where `b_0=P_plus` and `b_r=0` for `r>=1`.
Thus `M_{0r}=P_minus T_r` and `M_{rs}=-A T_{r-s}` for `r,s>=1`.

At the anchor, positive rows are deleted and negative rows contribute their
full off-diagonal energy, so `D_0=V_minus S_0`.  At `r>=1`, every negative
row contributes `S_r`; a positive row omits the single term at the anchor,
which has squared weight `T_r^2`.  Therefore
`D_r=V_minus S_r+V_plus(S_r-T_r^2)`.

For every `r`, one of the two sides of the window contains at least `H`
distances in `{1,...,H}`.  Each such distance contributes at least `1/4`
to `S_r`, so `S_r>=H/4`.  Since `D_r>=V_minus S_r` for `r>=1`, and
`P_minus^2<=m_minus V_minus` while `V_minus>=m_minus a_min^2`, the normalized
star vector satisfies

`||q||_2^2 = (P_minus^2/D_0) sum_{r>=1} T_r^2/D_r`
`<= 4 P_minus^2/(V_minus^2 H) <= 4/(a_min^2 H)`.

For the bulk block, `D_r>=V_minus H/4`.  Splitting a one-sided sum at `H`
gives `sum_{d>=1}T_d <= H + H^2 sum_{d>H}d^{-2} <= 2H`; both sides together
are at most `4H`.  Hence every absolute row sum of the symmetric normalized
bulk block is at most `16|A|/V_minus`.  The symmetric row-sum inequality
therefore gives `||C||_2<=16|A|/V_minus`.

Finally `Z` is the sum of the endpoint-star block and the interior-bulk block.
The triangle inequality and the star estimate yield
`||Z||_2 <= 2/(a_min sqrt(H)) + 16|A|/V_minus`.  This proves the claim. ∎

## Corrections or Missing Assumptions

None within the declared finite synthetic proxy.  The statement does not
assert a growing limit, physical source identification, or arithmetic sign law.

## Open Risks

The certificate is an exact audit of the finite formula, not an arithmetic
theorem.  `FULL_OPERATOR_GROWING_THEOREM`, arithmetic `L2`, fixed-power credit,
Route-B, and twin-prime gates remain open or absent.
