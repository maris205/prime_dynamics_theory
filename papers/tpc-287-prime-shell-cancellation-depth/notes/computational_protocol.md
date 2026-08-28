# TPC-287 computational protocol

1. Lock the TPC-286 producer and canonical result, plus the frozen TPC-268
   engine, by normalized SHA-256 digests.
2. Enumerate the seven declared shell anchors and verify their exact prime
   lists and cardinalities $1,2,3,4,5,6,7$.
3. For each of six source baselines, two kernel exponents, and seven anchors,
   rebuild the physical off-diagonal output separately for every prime.
4. Compute interval-valued component attachments, the direct shell attachment,
   component mass bounds, retention bounds, and every leave-one-prime-out
   attachment using exact rational output arithmetic and outward intervals.
5. Serialize one canonical JSON document.  `--check` must reproduce it exactly.
6. The independent checker must rebuild the prime shell and physical outputs
   without importing the producer.  Normal and optimized executions must exit
   zero with empty stderr and byte-identical stdout.
7. The stress script mutates theorem text, shell registry, component intervals,
   ratio fields, flags, provenance, and row membership; every mutation must be
   rejected.
8. The Bridge-B checker verifies all artifacts, the finite census, the PDF/log,
   and both normal/optimized runs of producer, independent checker, and stress.

No writer mode is invoked by a check.  The shell ladder is finite and declared;
no result is interpreted as a growing-shell estimate.
