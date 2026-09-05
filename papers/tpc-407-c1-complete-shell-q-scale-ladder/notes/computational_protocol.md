# Computational protocol

The producer enumerates complete prime shells at `Q=4096,8192,16384,32768`,
checks their exact counts, constructs the full CRT origin, and stores all
fractions and squared inequalities exactly at `H=66,N=264`.  The independent
checker rebuilds the sieve and CRT period and literally replays each masked
row energy for every prime and window coordinate.  The stress checker mutates
scale, shell, domain, bound, case, and firewall fields.  Normal and optimized
Python modes are required.
