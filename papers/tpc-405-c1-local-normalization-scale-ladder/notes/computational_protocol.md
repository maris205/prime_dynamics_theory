# Computational protocol

The exact producer uses Q=8192, the first eight primes in Q<p<=2Q, and the
five heights H=16,32,66,128,256 with N=4H; four multiplicities produce 20
cases. All fractions, CRT residues, row energies, and squared inequalities are
exact. The independent checker reconstructs the shell, CRT origin, and literal
masked row energies without importing the producer. The stress checker mutates
seven theorem-domain, case, bound, and claim-firewall fields. Both normal and
optimized Python modes are required.
