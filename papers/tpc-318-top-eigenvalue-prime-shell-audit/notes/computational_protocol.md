# TPC-318 computational protocol

* Parent: corrected TPC-317 certificate, locked by normalized-LF SHA-256
  `72bb54e0d50523e44b262092f1ad9305654114f16b7db4edbfd1e25caaa9f15a`.
* `H=66`, `Q={24,36,54,80}`, `s={1,2}`.
* Source panels: `I_X=(X/2,X]` for `X=640,1280,2560`.
* Each row is accumulated in forward and reverse prime-shell order.
* The top two eigenvalues use SciPy's symmetric subset driver; full NumPy
  `eigvalsh` is the second scalar path.
* The finite interval uses safe `|K|<=160`, an entrywise Gram guard, Weyl's
  norm conversion, solver spread, residual, and an outward display pad.

Pass criteria:

* 24 unique rows;
* 24 dual solver/finite residual records;
* 16 strict adjacent-scale top-eigenvalue decreases;
* 10 or more rows with relative top gap below `0.01` recorded as a stability
  obstruction;
* producer, independent checker, stress suite, and optimized replay agree.

No fitted asymptotic exponent is promoted to a theorem, and no arithmetic
reassembly is performed.
