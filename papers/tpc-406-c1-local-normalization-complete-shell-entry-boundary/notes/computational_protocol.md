# Computational protocol

The producer uses `Q=8192`, all 872 primes in `Q<p<=2Q`, `N=4H`, and five
heights.  Each row stores exact rational CRT, kernel, amplitude, energy, and
inequality data.  The independent checker reconstructs the sieve, complete
CRT origin, amplitudes, and literal masked row energies without importing the
producer's formulas.  The stress checker mutates shell, theorem-domain,
bound, case, and claim-firewall fields.  Normal and optimized Python modes
are both required.
