# TPC-394 computational protocol

The producer and checker use one thread per process (`OMP_NUM_THREADS=1`,
`OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`) and `numpy.float64` for the
finite matrix.  The producer accumulates primes in ascending order.  The
independent checker accumulates the same shell in descending order and does
not import the producer.

The eight intervals are generated from `a_j=5000001+401j` at the locked
indices `(0,5,10,15,20,25,30,35)`.  Five are calibration and three are
holdout, all with `N=1024`.  The fixed band is block distance `<=3` on eight
128-point blocks.  Every law/normalization/origin combination is recorded,
for 64 rows total.

The certificate is canonical sorted-key JSON.  Numeric replay comparison
allows only `8e-8*max(1,|a|,|b|)` for opposite floating summation order.  The
producer and checker are each run normally and with `-O`; stress is run in
both modes.  The Bridge-B checker locks all source, result, note, PDF, and
compile-log hashes.
