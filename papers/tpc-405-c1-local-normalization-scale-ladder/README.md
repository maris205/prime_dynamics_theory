# TPC-405: C1 Local-Normalization Scale Ladder

TPC-405 turns the TPC-404 local identity into a parameter-uniform theorem for
one adjacent entry of the selected-prime CRT proxy. Let H,N be integers with
H>=1, N>=H+2, let Q>N, and choose 2m distinct primes Q<p_i<=2Q, with the
explicit CRT residues o=0 (mod p_i) for even i and o=-N (mod p_i) for odd i.
With the TPC-404 selected-prime local geometry,

    0 <= z <= t_1/(a_min sqrt(S_0 S_1)) <= 4/(a_min H) <= 4/H.

Here z is the locally normalized entry at (o,o+1), a_min is the smallest
selected amplitude, and S_0,S_1 are the two translated kernel energies. The
proof is Cauchy--Schwarz plus G(o+1)>=V_minus S_1, S_0,S_1>=H/4, and a_p>1.

The exact certificate covers a 5-by-4 scale ladder with H in
16,32,66,128,256 and N=4H, all m=1,2,3,4 (20 cases). Decimal normalized
values are observations, while the inequalities and stored quantities are
exact rationals. The theorem is only for this one synthetic selected-prime
proxy entry; it is not a full operator estimate, not a theorem for the
physical h_0, and not an arithmetic or twin-prime result.

Status: PROVED_UNIFORM_FINITE_CRT_PROXY_ADJACENT_ENTRY_BOUND;
ARITHMETIC_ADVANCE=NO; FIXED_POWER_CREDIT=0; FULL_GATE_B=OPEN;
TWIN_PRIME_RESULT=NONE.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 python -B code/tpc405_c1_local_normalization_scale_ladder.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc405_independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc405_adversarial_certificate_stress.py --check

The next clue is TEST_C1_LOCAL_NORMALIZATION_COMPLETE_SHELL_ENTRY_BOUNDARY.
