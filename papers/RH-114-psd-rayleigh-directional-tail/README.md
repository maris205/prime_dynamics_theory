# RH-114: PSD-Rayleigh directional memory tail

RH-113 reduced fourth-mode support to four directional actions.  RH-114
proves a structured bound for those actions when the discarded memory tail is
positive semidefinite.

Let `T >= 0` be the tail, `P` the packet isometry, `Q` a right four-frame, and
`R=(I-PP*)TPQ`.  If `||T|| <= delta`, then

```text
R*R <= delta * Q*P*T*P Q.
```

For a recent directional action `Y=A P Q`, any PSD upper `D >= R*R` gives
`gamma^2=lambda_max(G^(-1/2) D G^(-1/2))`, where `G=Y*Y`.  Consequently,

```text
volume((A+T)P Q) >= (1-gamma)_+^4 volume(Y).
```

The scalar choice `D=delta^2 I` is a conservative special case.  The
packet-block choice retains the positive-tail geometry; the exact residual
Gramian is an audit upper endpoint.

Across 360 records there are zero PSD-dominance or certificate failures.  On
the fine chain the largest scalar gamma is `0.00134724`, while the packet
block gamma is `0.000175802`; the exact directional maximum is
`6.59362e-6`.  Threshold counts are unchanged, so the result is a quantitative
route improvement and a precise statement of the next missing all-level law.
