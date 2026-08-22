# TPC-218 Proof Package

## Maximum claim

PROVED_STRUCTURAL_L1: the literal V46 common-source finite-window kernel
admits a prime-label- and packet-label-preserving Hilbert lift with normalized
split envelope x^(1/96)(log x)^5; scalar shell recovery costs P<=2Q and
returns x^(11/32)(log x)^5.

TPC218_ARITHMETIC_ADVANCE = NO; TPC218_FIXED_ATOM_CREDIT = 0;
TPC218_L2 = NONE; TPC218_FULL_GATE_B = OPEN.

## Theorem

Let I_x=(x/2,x] and N=|I_x|. For fixed J and
M=max_j ||psi_j||_infty, define the rows and kernels in
research/tpc-big-road/bridge_b_prime_shell_packet_lift.md. Then

~~~
sum_(n in I_x)||K_vec(n)||_2^2
  << J M^2 (N+U^2)(Q^2/H)(log x)^5,

N^(-1)sum_(n in I_x)||K_vec(n)||_2^2
  << J M^2 x^(1/96)(log x)^5.
~~~

Moreover, with K_j=sum_q K_(j,q),

~~~
N^(-1)sum_(n in I_x)sum_j|K_j(n)|^2
  << J M^2 x^(11/32)(log x)^5.
~~~

## Proof dependencies

1. 4Q<H gives fixed-q cutoff injectivity.
2. Active rows satisfy h>=H/(2Q), giving the unsigned harmonic cluster bound.
3. Reduced fractions with denominator at most U have spacing at least U^(-2).
4. The scalar additive large sieve is applied coordinatewise in q and j.
5. Pointwise Cauchy over q gives the scalar corollary.

No PNT, Möbius cancellation, prime cancellation, or source theorem for the
signed Gate-B scalar is used.

## Exact finite validation

The producer and independent checker recompute a rational-coefficient dilation
fixture, three finite intervals, the P=4 q-alignment, and the packet projection
alignment. The rational fixture uses mu(d)/d only to avoid floating logarithms;
it is explicitly not an asymptotic substitute for the literal coefficient.

## Invalid promotion rules

The following promotions are forbidden:

~~~
split x^(1/96) -> arithmetic saving                 FORBIDDEN
finite q ratio 4 -> asymptotic prime lower bound     FORBIDDEN
packet trace bound -> signed four-packet cancellation FORBIDDEN
checker PASS -> full Gate-B or twin-prime theorem    FORBIDDEN
~~~

## Open edge

The next theorem must act on the literal signed prime shell and beat the exact
P collapse while retaining the four-packet, zero/nonunit, fixed-atom, and
normalization interfaces. This is recorded as
ROUND2_CLUE = PROVE_A_SIGNED_PRIME_SHELL_REASSEMBLY_BEYOND_THE_EXACT_P_COLLAPSE.
