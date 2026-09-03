# TPC-372 computational protocol

The formal panel is the complete fixed Cartesian product:

* origins `(1010001,1018021,1026041)`;
* full window count `2048`, partitioned by eight contiguous blocks of length
  `256`;
* `Q={512,2048,8192}`, exponent `1`, the inherited `all_plus` law, and beta
  `{0,2}`;
* 18 rows, with no response-driven component or row selection.

For every row, first form the full-window normalized matrix `T`.  The exact
block mask gives `D` by retaining same-block entries and `R=T-D`.  All three
use the full-window geometry.  The producer accumulates shells in increasing
order and the independent checker uses an independent sieve with descending
shell accumulation.  Normal/optimized subprocesses must have empty stderr
and byte-identical stdout.
