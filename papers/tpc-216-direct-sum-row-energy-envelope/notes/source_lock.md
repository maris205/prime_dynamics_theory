# Source Lock

## Literal parent

The scales and reciprocal cutoff are frozen in
`research/tpc-big-road/bridge_b_transition_native_euler_bdh_compiler.md`,
Equations (1.1) and (1.5):

```text
H=x^(21/32), Q=x^(1/3), Y0=H/(4Q), U=x^(133/400)
Q-shell={prime q: Q<q<=2Q}
D_x={d: Y0<d<=U, mu(d)^2=1}
c_d=mu(d)log(d)/d
0<|m|<=floor(dq/H)
```

The parent source records `d<U<Q<q`, making the inverses modulo `d` legal.

## TPC-215 interface

TPC-215 defines the complete-period direct energy

```text
E_direct=L*sum_d |c_d|^2*sum_(r mod d)|B_d(r)|^2
```

and leaves this quantity unestimated.  TPC-216 does not alter the emitter,
coefficient, period convention, smooth profile, or divisor band.

## Derived source inequalities

```text
H/(4Q)=x^(31/96)/4 -> infinity
U/Q=x^(-1/1200) -> 0
4Q<H for sufficiently large x
P=# {q prime: Q<q<=2Q} <= 2Q
Q^3/H=x^(11/32)
```

The `4Q<H` line is the exact condition used for fixed-q no-collision.  A weaker
`2Q<H` line is not used.

## Scope locks

- The theorem is a complete-period normalized direct-sum envelope.
- It does not control finite-window off-frequency terms.
- The shell Cauchy step is unsigned and does not use Mobius cancellation.
- The exact aligned-support fixture is finite structural QA only.
- Prime-shell reassembly, four-packet signs, arithmetic `L2`, fixed-atom credit,
  and strict `1/400` remain open.
