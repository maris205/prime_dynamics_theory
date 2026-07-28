# TPC-178: Canonical/minimal representation eligibility

Paper title:

> *Eligibility Before Canonicality: Why an Archive Key Is Not a
> Physical Representative*

TPC-178 audits the third H1 structural root only on source-backed
eligible carriers.  TPC-175--177 expose none, so no physical
representation class is available for a canonicality or minimality
test:

```text
eligible physical carriers                 0
representation classes tested              0
canonical representatives proved           0
minimal representatives proved             0
noncanonical counterexamples found          0
```

The absence of a counterexample on an empty domain is not a positive
certificate.  The result is

```text
ELIGIBILITY_BLOCKED_EMPTY_CARRIER_DOMAIN
H1.canonical_minimal_representation_certificate = NOT_TESTABLE
```

TPC-164 proved that

```text
(ell,k,native_d,jL,jK)
```

is the unique smallest key separating the 2,988 rows of one frozen
archive.  TPC-178 imports that result only as `ARCHIVE_ADDRESS`.
It does not treat the key as an occurrence identifier, a physical
parent, an equivalence-class selector, or a canonical/minimal
physical representation.

A future positive certificate must first supply an eligible actual
carrier, then define the physical representation space and
equivalence relation, state a source-locked selection or cost
functional, and prove existence plus uniqueness or minimality.

Reproduce from this directory after TPC-177 has been generated:

```powershell
python experiments/tpc178_representation_audit.py
python experiments/tpc178_representation_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Stable archival PDF:

```text
tpc-178-canonical-minimal-representation-eligibility.pdf
```

This is an L1 eligibility obstruction with an L0 executable audit.
It is not actual active support, fixed-`h0=2` arithmetic progress,
a named fixed-phase theorem, program-positive L2, a strict `1/400`
endpoint gain, a prime-pair lower bound, or a twin-prime theorem.
