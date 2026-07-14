# Complement coupling in time-unfolded Gaussian returns

This directory contains the nineteenth-layer paper in the quadratic
prime-dynamics program:

> *Complement Coupling in Time-Unfolded Gaussian Returns at a Quadratic
> Band-Merging Map: Critical-Sibling Leakage, Floquet Replication, and a
> No-Go Theorem for Naive Feshbach Identification*

The paper tests the missing complement-resolvent step after RH-18 and obtains
a precise negative result for the naive scalar strategy.

The conditioned critical profile is reflection symmetric across the physical
partition `b = u_c**(-1/2)`. Consequently the omitted sibling branch has the
same asymptotic local `L2` mass as the retained branch. It is not a Gaussian
tail, and a slowly growing one-branch window cannot make the off-block
coupling small.

There is a second, independent obstruction. For `T = K_sigma**2`, the full
time-labeled cyclic operator is exactly

```text
C_k = U_k tensor T,
C_k  ~=  direct_sum_l omega_k**l T.
```

Thus every single physical eigenvalue generates a complete roots-of-unity
ring in the time lift. A sector-free Feshbach theorem for `C_k` cannot by
itself prove that the physical Markov operator has that many distinct
eigenvalues.

At `sigma = 1e-4`, the numerical audit finds

```text
right / left critical exit norm       = 0.997381806
right / left return eigenvalue        = 0.994756975
left one-step return radius           = 0.756459484
two-branch one-step return radius     = 0.789824974
full endpoint one-step return radius  = 0.789919739
```

The corrected next target is a two-branch, Perron/parity-extracted,
Floquet-sector effective Hamiltonian. The result does not alter the earlier
deterministic pole theorem, endpoint-rank theorem, or the archived physical
resonance cloud.

Run the tests and full audit with:

```bash
/root/math/.venv/bin/pytest -q
PYTHONPATH=src OPENBLAS_NUM_THREADS=16 /root/math/.venv/bin/python \
  experiments/run_complement_audit.py
```

Build the manuscript with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
