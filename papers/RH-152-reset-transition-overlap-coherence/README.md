# RH-152: Reset Transition Overlap Coherence

RH-151 independently certified 130 clock-rank reset packets.  RH-152 proves
outward principal-angle, frame-overlap, inverse-overlap, and polar-transition
bounds for consecutive packet balls.

All 120 frozen transitions remain invertible.  The minimum robust overlap is
`8.9866e-5`, the maximum inverse-overlap upper is `1.1128e4`, and every polar
transition is stable with radius at most `0.01170`.

The result is positive but nonuniform: 19 transitions lie below overlap
`0.1`, six below `0.01`, and two below `0.001`.  The reset atlas therefore
supports a finite moving frame, but the next outward assembly must retain the
condition-number drawdown rather than replacing it by a uniform constant.
