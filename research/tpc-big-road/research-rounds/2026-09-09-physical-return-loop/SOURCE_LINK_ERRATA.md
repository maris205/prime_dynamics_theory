# Source-link erratum for the immutable raw archive

The complete reviewer responses are preserved verbatim. A local-link audit
found one path typo in
[the finite-attachment raw report](agent-reports/physical-loop-finite-attachment-audit.md).
Its link to the prior attachment report omitted the directory prefix
`research/tpc-big-road/`.

The correct target is
[the prior physical-attachment report, line 97](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-multi-agent-recon/agent-reports/recon-physical-attachment.md:97).
The mathematical corrections are already in
[FINITE_ATTACHMENT_ERRATUM.md](FINITE_ATTACHMENT_ERRATUM.md); this additional
erratum corrects navigation only.

A first naive Markdown-link regex also misclassified TeX function notation
`[f](v)` as links and did not trim whitespace around one valid absolute
target. The corrected document check excludes fenced code and TeX display/
inline regions, trims link-target whitespace, and reports this one preserved
raw-link exception separately. It does not alter a source or proof to make
a mathematical checker pass.
