# TPC-322 computational protocol

- Source intervals: (I_X=(X/2,X]capmathbb Z), (X=640,1280,2560).
- Prime shells: (mathcal S_Q=(Q,2Q]capmathbb P), (Q=24,36,54,80).
- Height and exponents: (H=66), (s=1,2).
- Each literal (B_p) is built in binary64 from the displayed formula.
- The producer forms the Frobenius block Gram in forward and reverse prime
  order, audits four named sign patterns, and exhausts (2^{m-1}) signs with
  the first sign fixed.
- Ratios receive an outward (10^{-12}) guard; sign extrema are retained as
  finite numerical evidence.
- The independent checker uses reverse shell construction and `einsum` for
  each block inner product and does not import the producer.
- The stress suite tests the projector identity, global sign gauge, positive
  definiteness/extrema on a toy Gram, pattern labels, and interval semantics.
- No random seed, external dataset, or unrecorded parameter is used.
