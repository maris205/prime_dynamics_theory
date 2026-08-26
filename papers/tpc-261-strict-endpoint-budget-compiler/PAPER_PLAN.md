# TPC-261 paper plan

## Question

After TPC-260 identifies four-packet mode zero as the missing literal datum, what
endpoint budget is actually sufficient to turn a finite lane estimate into the
target exponent, and what can be concluded from the current log-only and
null-compatible information?

## New contribution

Compile the exact baseline-to-target gap

```text
E0 = 5/3,   E* = 1997/1200,   E0-E* = 1/400
```

into a lane-wise theorem.  If lane `l` saves `delta_l` powers and pays
`lambda_l` powers in reassembly, its effective credit is
`sigma_l=delta_l-lambda_l`; a finite family reaches the target only when
`min_l sigma_l > 1/400`.  Equality is borderline at the power level.  A
logarithmic saving alone has zero fixed-power credit.

The paper then scales the exact TPC-260 plus/alternating witness to show that
packet marginals, Haar/null projections, and total diagonal energy do not imply
any positive fixed-power upper bound on the literal four-packet residual.

## Scope and claim ceiling

This is a structural endpoint-budget theorem and obstruction.  It is not a
literal prime-shell counterexample, an arithmetic `L2` estimate, a fixed-atom
credit, a full Gate-B proof, or a twin-prime theorem.  The literal common-clock
mode-zero/cross-Gram estimate remains open.

## Deliverables

1. exact endpoint-budget compiler and strict-threshold proof;
2. log-versus-power firewall;
3. scaled null-compatible four-packet witness;
4. independent exact certificate, stress audit, and Route-B evaluation;
5. a minimum-sufficient literal theorem for the next bridge.
