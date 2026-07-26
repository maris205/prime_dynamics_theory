# TPC-122: Signed-prefix to zero-mode transfer

This paper refines the open distinguished-zero-mode input isolated in
TPC-111 and TPC-112.

On each canonically ordered literal fiber it proves the exact Abel
identity

```text
sum_i sigma_i w_i
  = S_m w_m + sum_{k < m} S_k (w_k - w_{k+1}),
S_k = sum_{i <= k} sigma_i.
```

For

```text
||w||_BV* = |w_m| + sum_{k < m} |w_k - w_{k+1}|,
```

the resulting bound is sharp:

```text
sup_{||w||_BV* <= 1} |sum_i sigma_i w_i|
  = max_k |S_k|.
```

TPC-111 already contains the finite duality.  The new result here is
the complete exponent ledger, including the literal content
remainder.  If a future prefix theorem gives saving `delta`, the
outer BV envelope costs `ell_Z`, and the content remainder has
exponent `eta_cont`, then

```text
eta_Z_cert = min(delta - ell_Z, eta_cont).
```

This formula is callable only when `delta >= ell_Z`; otherwise the
certificate supplies no nonnegative zero-mode exponent for the
TPC-112 cone.

Together with the TPC-112 determinant cone, the exact sufficient
conditions become

```text
delta    >= ell_Z + lambda_D / 2,
eta_cont >= lambda_D / 2.
```

The paper does not prove the required growing signed-prefix estimate.
The finite duality is L0 and its crosswalk to the fixed-`h0`
TPC-111 ordered affine outer fibers is a conditional L1 interface:
TPC-111's content, masks, polarizations, native keys and literal outer
reassembly must first be retained and verified. For a subpower class
decomposition, the paper requires a common uniform error term and
uses a fixed liminf class reserve; a classwise minimum is not assumed
uniform automatically. There is no L2 arithmetic advance, parity
breach, or twin-prime conclusion.

## Reproduce

```powershell
python experiments/tpc122_prefix_transfer_audit.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-122-signed-prefix-zero-mode-transfer.pdf`

SHA-256:

`f5e81670180a787c6542efc8ff04f29a81ffdb262c84af9708c876f1d23eea16`
