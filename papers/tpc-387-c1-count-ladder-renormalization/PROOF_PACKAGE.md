# TPC-387 proof package

## PROVED_EXACT_FINITE

- Candidate grid, origin indices, count roles, band modes, and fit rule are
  fixed before holdout readout.
- Current intervals are pairwise disjoint and disjoint from listed prior
  panels.
- The rational 13-point anchor has positive geometry and symmetric matrices
  for all four laws.
- Parent code and certificate hashes, JSON canonicality, and row digest are
  checked.

## NUMERICALLY_CERTIFIED_FINITE

- 256 rows and 32 cells replay in ordinary and optimized Python modes.
- All 32 calibration-slope endpoint predictions pass the predeclared 3% cap.
- The inherited spectral diagnostic has 40 finite failures and the Schur
  diagnostic has none; these counts are independently reproduced.
- Twenty-five structural mutations are rejected.

## OPEN

The finite slope does not establish count uniformity, a growing operator
bound, or validity of the source normalization. Arithmetic reassembly and a
twin-prime theorem remain outside the certificate.
