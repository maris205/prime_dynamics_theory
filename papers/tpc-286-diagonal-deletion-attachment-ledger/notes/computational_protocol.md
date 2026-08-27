# TPC-286 computational protocol

The producer locks the TPC-284 code/result, the TPC-285 code/result, and the
frozen TPC-268 engine by normalized-LF SHA-256 hashes.  It reconstructs the
full diagonal-including output, the explicit diagonal output, and their
difference for each of the 72 registered controls.  The four-block attachment
uses the same interval arithmetic and projection convention as TPC-284.

Internal endpoints are rational fractions on the frozen engine grid.  New
component intervals are serialized with the engine's established decimal
formatter; parent physical intervals are compared after parsing, so harmless
trailing zero spellings cannot alter a verdict.  Exact subtraction of the
internal intervals certifies reconstruction containment.

The independent checker does not import the producer.  It independently
enumerates prime shells, rebuilds all three outputs, checks the component
intervals, signs, ratios, parent replay, and the complete census.  The stress
checker computes the expected document once and rejects mutations to theorem,
interval, sign, flag, budget, provenance, and row count.

The Bridge-B checker runs producer, independent, and stress scripts in normal
and optimized Python with `PYTHONDONTWRITEBYTECODE=1`, requiring zero standard
error and byte-identical paired stdout.
