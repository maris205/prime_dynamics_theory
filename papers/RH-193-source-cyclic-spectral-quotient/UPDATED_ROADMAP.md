# Roadmap after RH-193

```text
full Frobenius operator I_m tensor A                 [wrong low-rank target]
  -> source-cyclic restriction K_S                   [proved exact]
  -> source-observable spectral support              [next]
  -> compare temporal roots with physical spectrum   [next finite audit]
  -> canonical packet and cross-scale transport      [open]
  -> Gate A                                           [open]
```

The source-cyclic restriction preserves the complete input-output moment
sequence, but it can still have dimension comparable to `n`.  A later
minimal quotient may remove modes that are unexcited by `S` or invisible to
the observation.  No low-dimensional truncation is licensed merely by the
four-dimensional temporal fit.
