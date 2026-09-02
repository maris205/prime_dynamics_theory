# TPC-351 computational protocol

* Parent producer: TPC-350 code, locked by normalized SHA256
  `7819fb38be3f6d33688ca3a4caa1920da2dd8624805356411d8099fc069e185d`.
* Parent certificate: TPC-350 certificate, locked by normalized SHA256
  `bc874009cfdd8fd7d6ea06d5d109a46d8bd9a732cd4933852f9176c5801bb086`.
* Fresh origins: `60097, 72097, 84097`.
* Interval lengths: `256, 512, 1024, 2048`.
* Shell anchors: `36, 80, 128, 256`, with primes `Q<p<=2Q`.
* Kernel exponents: `1,2`; height `H=66`.
* Source laws: `all_plus`, `alternating_index`.
* Total rows: `3*4*4*2*2=192`; growth series: `3*4*2*2=48`.
* Reciprocal rule: `gamma_j=1/p_j-(1/r)sum_k1/p_k`, represented by exact
  `Fraction` values before floating-point matrix application.
* Parent control: TPC-350 balanced-step response on the identical row key.
* Baseline: maximum defect norm among all mask-hit coordinate columns.
* Exact anchor: interval `[97,110]`, `Q=4`, exponent one, all-plus source law.
* The producer uses forward shell accumulation; the independent checker uses
  reverse shell accumulation and recomputes matrix metrics, exact coefficients,
  parent comparisons, growth series, and the rational anchor.
