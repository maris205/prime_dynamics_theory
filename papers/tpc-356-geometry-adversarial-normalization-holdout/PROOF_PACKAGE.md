# TPC-356 proof and scope package

## Proposition 1: deterministic geometry-only selection

The candidate list, pilot count, score, tie-break, and greedy separation rule
are finite deterministic objects.  Therefore the selected triple is uniquely
determined.  The producer and the reverse-shell checker independently obtain
`(38423,42010,45597)`.

## Proposition 2: response-blindness

The selection score is computed from the unsigned component matrices only.
It does not read the V59 source vectors, a response metric, or a sign law.
This is an exact property of the declared program and protocol.

## Proposition 3: finite normalized polarization

On every replay row the inherited positive geometry diagonal makes the
TPC-355 congruence a finite real matrix.  Expanding a finite square proves
the polarization identity and finite Cauchy envelope for both raw and
normalized operators.

## Proposition 4: certified finite audit

The canonical certificate contains 216 law-level rows.  Reverse-shell
reconstruction agrees with the producer within the declared numerical
tolerance, and ten mutation tests reject altered headers, rows, provenance,
gains, and firewall fields.

## Scope firewall

The all-plus minimum gain `0.019062676850676086` and mean gain
`0.0068817732644231855` are finite scoped observations on the selected
origins.  They do not imply a bound for all origins or growing intervals.
No source-uniform masked $L^2$ estimate, arithmetic advance, fixed-power
credit, Route-B reassembly, or twin-prime theorem is claimed.
