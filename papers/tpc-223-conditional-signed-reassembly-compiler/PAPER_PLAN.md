# TPC-223 paper plan

1. Freeze the four-packet signed-reassembly interface exposed by TPC-222.
2. Introduce a conditional two-channel exponent ledger: prime-AP dispersion and
   polarized packet cross-correlation, with an explicit structural-loss term.
3. Prove the exact compiler implication and the strict `1/400` criterion.
4. Certify strict, borderline, failed, and missing-channel ledgers with exact
   rational arithmetic and an independently reimplemented checker.
5. Keep every arithmetic input conditional: the paper is a theorem about the
   compiler, not a proof of either dispersion hypothesis on the literal prime shell.
