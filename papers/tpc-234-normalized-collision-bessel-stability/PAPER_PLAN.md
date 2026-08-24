# TPC-234 paper plan

## Question

After TPC-233 refutes fixed raw row comparability, does unit-row normalization prevent
depth-dependent collision-operator blowup?

## Contribution

Use the exact multiplicity-two bucket geometry to prove a depth-uniform Bessel bound
`G<=2I` for arbitrary normalized row amplitudes.  Separate conditioning stability from
saving by an exact literal `4/3` amplification block.

## Sections

1. Conditioning problem and normalization.
2. Multiplicity-two Bessel theorem.
3. Spectral consequences and sharpness.
4. Literal `Q39,L7` block and finite checks.
5. Source-validity boundary.

## Claim class

`PROVED_STRUCTURAL_L1`.  Unit normalization is a modeling transform until an actual
V59 coefficient crosswalk proves it source-valid.
