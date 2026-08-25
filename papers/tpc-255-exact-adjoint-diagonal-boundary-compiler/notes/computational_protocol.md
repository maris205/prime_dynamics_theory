# Computational protocol

The producer constructs the expected canonical JSON document and checks the
released file byte for byte.  It uses sorted ASCII keys, compact separators,
no NaN, and one trailing newline.  Rational and Gaussian-rational values are
serialized as strings.

The independent checker imports no producer module.  It validates the schema,
eight source hashes, exact adjoint pairing, mask period means, the full
independent reconstruction, strict nested integer typing, and 100 adversarial
mutations in 14 named classes.  The stress program creates 192 deterministic
finite families and verifies the coordinate decomposition, pairing,
child-jump signs, and unit masks in exact arithmetic.

Every script is run under normal and optimized Python.  The two stdout streams
must be byte-identical and stderr must be empty.  No Python `assert` is used.
