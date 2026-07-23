# TPC-78: Exact forest completion reduction

This paper specializes the sparse component program of TPC-77 to
complex-scalar incidence matrices whose actual nonzero bipartite support
is a forest.

Its exact results are:

- variable leaves admit cost-preserving erasure;
- forest support fixes matrix rank through maximum matching;
- the pruned-core defect is
  `1 + sum_j (deg(j)-2)`;
- one-complex-defect components have a closed primal-dual formula;
- degree-two variable trees admit explicit phase transport;
- column-dominant pivots admit exact Schur-type elimination;
- higher-defect components reduce to a defect-dimensional complex SOCP;
- balanced Hall motifs give additive and fractional dual-packing lower
  certificates.

The paper also records sharp stop rules: row leaves are not free,
complex stars are geometric-median problems rather than coordinatewise
median problems, cycle support does not determine rank, and general
real-linear blocks require additional surjectivity/conformality
hypotheses.

These are exact L0 algebraic results that advance the L1
interface/certificate layer. They do not establish a fixed-shift
arithmetic saving, a parity-breaking estimate, or a twin-prime theorem.

Build with:

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
