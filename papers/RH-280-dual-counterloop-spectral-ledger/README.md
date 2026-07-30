# RH-280: Dual counterloop/spectral ledger

The RH certificate now has two explicitly separated branches:

- noisy spectral quotient: `(false,false,false,true,true)`;
- deterministic graded counterloop: `(true,true,false,true,true)`.

The counterloop branch has an exact operator-derived head and coefficient
bridge, but still lacks the variable-rank noisy quotient tail.  The spectral
branch retains all three original open obligations.  Neither branch is a
complete Gate-A certificate; Gates A--E remain false/open.
