# TPC-181: Metric-to-fixed-atom selector gate

Paper title:

> *The Metric-to-Fixed-Atom Selector Gate: A Singleton Obstruction,
> Exact Bridge Hypotheses, and the Pointwise Return*

## Exact result

TPC-170 proves, on a prescribed packet schedule,

```text
phase_quantifier = LEBESGUE_AE_FIXED_PHASE
scale_quantifier = EVENTUALLY_PRESCRIBED_SCHEDULE
endpoint_quantifier = ALL_PREFIX_THETA_SHELL
metric_power = every delta < 1/4
```

TPC-180 finds no source-backed value-bearing named phase registry.
Even if such a registry were later supplied, a full-measure good set
does not by itself contain a prescribed singleton. For any named
`alpha_star`, the null set `{alpha_star}` is compatible with the
almost-everywhere theorem.

The selector result is therefore:

```text
H2.metric_fixed_atom_crosswalk = NOT_TESTABLE
phase_metric_uncontrolled_atomic = STOP_SCOPED
named_atom_status = NOT_IDENTIFIED
fixed_atom_decay_obtained = false
```

The scoped stop applies only to uncontrolled promotion from
Lebesgue-a.e. phase to an atom. It does not stop the selected
architecture and does not stop either parent-ready pointwise route:

```text
O161.bad_endpoint_pointwise_fixed_atom
  = OPEN_PARENT_READY
O161.direct_additive_twist_fixed_atom
  = OPEN_PARENT_READY
```

A legal source-backed metric bridge must name the exact phase and
production schedule and prove schedule-specific avoidance:

```text
alpha_star not in limsup E_n
```

where `E_n` is the TPC-170 bad set for that exact schedule. Phase
averages, density-one registries, scale-dependent selectors, or a
registry identity without an avoidance theorem are insufficient.

## Level boundary

- `L0`: source locks, schemas, and mutation diagnostics.
- `L1`: the rigorous singleton-versus-a.e. nonimplication and typed
  scoped selector obstruction.
- `L2`: none.

The metric powers `delta < 1/4` remain ineligible for the named
fixed-atom ledger.

## Reproduce

Run TPC-180 first, then:

```powershell
python experiments/tpc181_selector_gate.py
python experiments/tpc181_selector_gate.py --check
```

Generated artifacts:

```text
experiments/tpc181_selector_gate.json
experiments/tpc181_selector_gate_audit.json
schemas/tpc181-selector-gate-v1.schema.json
schemas/tpc181-selector-gate-audit-v1.schema.json
```

Stable PDF:

```text
tpc-181-metric-fixed-atom-selector-gate.pdf
```

No named-phase estimate, program-positive L2 result, strict `1/400`
gain, prime-pair lower bound, or twin-prime theorem is claimed.
