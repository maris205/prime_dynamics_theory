# Computational protocol

The producer writes a canonical JSON document with exact fraction records,
object locks, scope firewalls, and finite q-collision fixtures.  `--check`
recomputes the document and requires a byte-for-byte match.

The independent checker does not import the producer.  It rejects duplicate
JSON keys and nonfinite constants, verifies exact key/type equality, recomputes
all fixture rows, and rederives the exponent and leading-constant ledgers.

The stress program uses several independent finite prime shells.  It verifies
primitive support, post-collapse Cauchy, positive collision excess, and the
distinction between direct and collapsed energies.  All fixtures use rational
compact-support weights only for exact software QA and are labeled
`NUMERICAL_FINITE_ILLUSTRATION_ONLY`.

Release checks run all three programs in normal and optimized Python modes and
require empty stderr and byte-identical stdout for each pair.
