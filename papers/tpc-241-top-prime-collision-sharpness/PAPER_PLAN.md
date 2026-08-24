# TPC-241 paper plan

## Claim

For every fixed admissible nonnegative normalized common profile, prove an
explicit top-prime q-collapsed coefficient liminf at scale
`x^(1/48)/log x`, transfer one half of it to the literal finite window, and
deduce that every fixed-power improvement below exponent `1/48` is impossible
for this unsigned object.

## Proof spine

1. Freeze the exact V59 scales, profile, primitive residue rows, full kernel,
   and top-prime subenergy.
2. Prove the endpoint-safe first-moment lattice estimate
   `sum_(0<|m|<=T)psi(m/T)=T+O_psi(1)`.
3. Sum over shell primes and obtain the uniform row mass
   `S_p=(3/2+o_psi(1))pQ^2/(H log Q)`.
4. Apply Cauchy over all `p-1` primitive residues only after q-collapse.
5. Insert `C_p=-log(p)/p` and the weighted PNT top-shell average.
6. Convert the exact constant to `10773log(2)/1600` and exponent `1/48`.
7. Apply the TPC-238 lower frame to the complete vector before top-prime
   restriction, obtaining the finite-window constant `10773log(2)/3200`.
8. Prove the fixed-power refutation with the exact quantifiers.

## Claim firewall

The manuscript must not claim signed cancellation, arithmetic `L2`, a
four-packet theorem, class-uniform profile thresholds, strict `1/400`, or a
twin-prime result.  Finite certificates test identities and software only.
