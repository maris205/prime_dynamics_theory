# RH-384 Replay Audit

## Deterministic build order

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /root/math/.venv/bin/python experiments/build_schema.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf prime-tail-scale-separation.pdf
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /root/math/.venv/bin/python experiments/verify_archive.py
```

## Frozen result

- Status: `RH-384_prime_tail_scale_separation`.
- `all_pass`: true.
- Source count: 51.
- Source aggregate: `90434e0468ecc062cb522da096a267748725b5dca8e59c642bb7711f45a3e0e4`.
- Certificate bytes: 48,689.
- Certificate SHA-256: `01c91e57a01de9841f282327ab2f6e1a9368e136393ddab7a2cfe6b019a519c8`.
- Schema: closed Draft 2020-12, generated from the exact result.
- Core test suite before archive: 20 passed.

## Reproducibility defenses

- strict JSON parsing with duplicate/nonfinite rejection;
- exact type checks (`bool` is not accepted as `int`);
- optimized-mode execution;
- release-blob identity for every external source;
- hostile Decimal contexts with exponent/trap changes;
- exact upward bound on tail loss before lower-factor subtraction;
- genuine A- and B-surrogate mutations;
- archive membership/hash mutation tests.

## Final publication replay

- Test suite with manifest present: 20 passed.
- PDF: 8 A4 pages; log scan, font embedding, text extraction, Ghostscript render, and page raster inspection pass.
- Publication manifest: `RH-384_fixed_publication_manifest`.
- Publication members: 29.
- External immutable inputs: 51.
- Archive verification: `RH-384_archive_verified`.
- Failure count: 0.
- Manifest rebuild, result/source-lock match, release-blob identity, source-digest contract, exact-certificate digest, and semantic-PDF identity: all true.
