# RH-316: Recursive integer spectral prefix realization

Apply the RH-315 packet at orders `1,2,...,N`.  At step `d`, compute the
remaining real moment error and add a `d`-packet.  Because that packet has no
moments below `d`, the construction is triangular and terminates with

    sum_j mu_j^n = a_n,  1 <= n <= N,
    |mu_j| <= q.

The resulting multiset is finite, conjugate closed, and has genuine integer
multiplicities; equivalently it is the spectrum of a finite normal matrix.

The numerical reproduction uses the archived RH-263 deterministic anchors
through order eight; it is an implementation check, not a fitted proxy.

This resolves synthetic finite-prefix realizability only.  It does not
identify the constructed matrix with the actual noisy operator.  Gates A--E
remain false/open.
