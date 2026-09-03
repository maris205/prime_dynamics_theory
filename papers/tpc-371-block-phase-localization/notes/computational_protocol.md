# TPC-371 computational protocol

The formal panel is fixed before its certificate is written:

* origins: `(1010001,1018021,1026041)`, inherited from grid
  `1010001+401j` at indices `(0,20,40)`;
* parent count: `2048`; block indices `0,...,7`; block length `256`;
* `Q={512,2048,8192}`, exponent `1`, laws
  `all_plus`, `alternating_index`, `mod4_character`, `half_split`, and
  beta `{0,2}`;
* all `576` rows are evaluated, with no response-driven filtering;
* cap values are spectral `0.64` and Schur `0.83`;
* exact anchor inherited from TPC-370: `[1010346,1010359)`, `Q=4`, exponent `1`.

The producer uses the TPC-355 literal masked block and accumulates shells in
increasing order.  The independent checker uses a separately implemented
prime sieve and descending-shell accumulation.  Normal and optimized Python
replays are compared by the Bridge-B checker with empty stderr and exact
stdout equality.
