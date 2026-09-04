# TPC-383 computational protocol

The producer freezes the grid `1600001+401j`, indices `(0,20,40)`, count 512,
block length 128, c=1, Q `(512,2048,8192)`, beta 2, exponent 1, height 66,
four laws, and two normalizations.  The selected intervals are checked against
all earlier coordinate panels by exact endpoint inequalities.

At each Q it constructs one raw matrix and one geometry vector per origin.
The pooled scalar is the mean of the three geometry means and is shared by all
laws.  Both normalized matrices are masked and diagonalized; values are
serialized with 17 significant digits.  The q=8 anchor uses exact rational
arithmetic on `[1600001,1600014)`.

The independent checker repeats the sieve, reverse-shell accumulation, both
normalizations, and eigensystems without importing the producer.  The stress
checker mutates 25 semantic fields.  Bridge-B compares normal and optimized
outputs for all three checks.
