# TPC-323 paper plan

## Research question

Does a declared sign law select a stable spectral shape after the signed
projector interface is trace-normalised, and is that shape choice independent
of the coherent energy ratio?

## Frozen object

Use exactly the TPC-322 literal block family with `H=66`,
`X={640,1280,2560}`, `Q={24,36,54,80}`, and `s={1,2}`.  Keep the four
predeclared laws: all-plus, index alternation, the mod-4 character, and the
half split.

## Claim ladder

1. `PROVED_EXACT_FINITE`: for every finite block family, trace-normalised
   signed spectra factor into an energy scalar `rho` and a probability profile
   `pi`; positive scalar changes leave `pi` unchanged.
2. `NUMERICALLY_CERTIFIED_FINITE`: on all 24 rows, all-plus signed profiles
   majorize direct profiles; the other law counts are 17/7, 21/3, and 18/6
   (majorizing/mixed).
3. `NUMERICAL_OBSERVATION`: among the four declared laws, all-plus is the only
   one with a uniform majorization label on this panel.
4. `NUMERICALLY_CERTIFIED_FINITE`: all-plus energy is below one on 3 rows and
   above one on 21, while its profile label remains unchanged.
5. `OPEN`: fresh-panel profile holdout, source-native arithmetic realization,
   growing signed reassembly bound, and any twin-prime consequence.

## Adversarial controls

- forward and reverse shell accumulation;
- SciPy and NumPy eigensolvers;
- independent reverse/einsum reconstruction without importing the producer;
- exact rational small anchor for the trace/energy identity;
- deterministic synthetic stress tests, including energy contraction with
  profile concentration.

## Paper sections

1. Question and scope;
2. signed operator and profile coordinates;
3. exact amplitude–shape factorisation;
4. finite protocol and numerical guard;
5. profile-majorization and energy results;
6. obstruction, route status, and next clue.
