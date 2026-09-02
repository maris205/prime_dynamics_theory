# TPC-350 computational protocol

* Parent producer: TPC-349 code, locked by normalized SHA256
  `ed3b543a44a270301f3cc7543533c1ce35a6f9ea433e9581df19759b2bca3a03`.
* Parent certificate: TPC-349 certificate, locked by normalized SHA256
  `baceb7b6cbf32fbbf84289d302551ed7f42abb45c39333a7d235a229c9a7a741`.
* Fresh origins: `60097, 72097, 84097`.
* Interval lengths: `256, 512, 1024, 2048`.
* Shell anchors: `36, 80, 128, 256`, with primes `Q<p<=2Q`.
* Kernel exponents: `1,2`; height `H=66`.
* Source laws: `all_plus`, `alternating_index`.
* Total rows: `3*4*4*2*2=192`; growth series: `3*4*2*2=48`.
* Baseline: maximum defect norm among all mask-hit coordinate columns.
* Exact anchor: interval `[97,110]`, `Q=4`, exponent one, all-plus source law.
* The producer uses forward shell accumulation; the independent checker uses
  reverse shell accumulation and recomputes the matrix metrics.
