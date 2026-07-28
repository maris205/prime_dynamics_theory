# TPC-163: source-locator census and native-key collisions

Paper title:

> *Source-Locator Census for the H1 Crosswalk: Native-Key Collisions
> and the Absence of Production Occurrence Edges in the Frozen Corpus*

## Result

TPC-163 freezes the declared TPC-153/154/155/156/161/162 source corpus and
requires every positive production edge to carry all of:

```text
canonical source path
canonical UTF-8/LF source hash
theorem locator
formula locator
nonempty derivation AST
correct semantic class
```

The exact census finds:

```text
production cut paths                         2988
native triples (ell,k,native_d)               866
native triples with multiplicity > 1          854
rows in collision classes                    2976
excess rows over native triples              2122
multiplicity distribution              {1:12, 2:220, 4:634}
theorem-backed actual-occurrence edges           0
```

The thirteen-class zero table is an
`EXPLICIT_MAPPED_FROZEN_CORPUS_CENSUS`: every listed class is mapped
to the current frozen artifacts and status fields.  It is not a
generic scanner that will automatically discover future schemas or
newly introduced fields.  Extending the corpus or schema requires an
explicit mapping update and a new certificate.

Thus `(ell,k,native_d)` is not a row key for the frozen production
archive.  The zero edge count means only that no qualifying edge is
present in this frozen declared source corpus.  It does **not** prove
that actual occurrences do not exist.

The two positive source-backed claims recovered from TPC-153 are the
cut-to-shadow injection and its exact column conservation.  Both are
explicitly typed as shadow-only statements.  TPC-154 contributes two
additional positive claims---formal completion-fiber nonuniqueness
and the current-artifacts-only recovery obstruction---typed
`FORMAL_ONLY/SCOPED_OBSTRUCTION`.  They cannot contribute an actual
occurrence edge.

## Reproduce

From this directory:

```powershell
python experiments/tpc163_source_census.py
python experiments/tpc163_source_census.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Generated artifacts:

```text
experiments/tpc163_source_census.json
experiments/tpc163_source_census_audit.json
samples/tpc163_native_collision_witness.json
```

Stable archival PDF:

```text
tpc-163-source-locator-census-native-key-collision.pdf
```

## Claim boundary

This is a source-locked L0/L1 archive theorem.  It proves neither a
production occurrence crosswalk, actual active support, a canonical
or minimal parent representation, positive fixed-`X` L2, a
prime-pair lower bound, nor the twin-prime conjecture.
