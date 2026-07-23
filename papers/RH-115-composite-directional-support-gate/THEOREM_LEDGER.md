# RH-115 theorem ledger

## Exact results

- Factorized capacity gate `q4 >= volume_lower/capacity_upper`.
- Monotone composite gate obtained by maximizing admitted lower bounds.
- Information-optimality of the maximum when no cross-candidate dependence
  is assumed.
- Outward-admissibility filter requiring all factors to refer to one enclosed
  operator instance.

## Validation

- 360 records and zero admitted dominance failures.
- Full counts at `1e-8`: direct `113`, PSD block `114`, composite `114`.
- Full composite counts at `1e-6` and `1e-4`: `109` and `98`.
- Three excluded diagnostic failures are copies of one weak record under the
  three threshold labels.

## Boundary

The exact-directional diagnostic is not admitted without a cross-assembly
outward guard.  All-level capacity and directional-tail laws remain open, as
do Stage A, Hilbert--Polya, zeros, and RH.
