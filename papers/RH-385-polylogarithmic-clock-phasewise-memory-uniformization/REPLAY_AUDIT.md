# RH-385 Replay Audit

## Deterministic build order

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /root/math/.venv/bin/python -B experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /root/math/.venv/bin/python -B experiments/build_schema.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /root/math/.venv/bin/python -B -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf polylogarithmic-clock-phasewise-memory-uniformization.pdf
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /root/math/.venv/bin/python -B experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /root/math/.venv/bin/python -B experiments/verify_archive.py
```

## Frozen result

- Status: `RH-385_polylogarithmic_clock_uniformization_certified`.
- `all_pass`: true.
- Certificate bytes: 472,145.
- Certificate SHA-256:
  `3100168ed679a02c2d97496a2457ff512c2327764ca884b248ad312a6af8eea8`.
- Source count/groups: 67 in `51/8/8`.
- Source aggregate:
  `14a401e81d5d1868a8b3148478ca26f8975d0bde08b0a0117d4808571a2c5d79`.
- Schema: recursively closed, strictly typed, official Draft 2020-12.
- Certificate mutations: 24/24 rejected.
- Outer four-volume replay: volumes 4, archive members 73, dependency hashes
  1,548, result hashes 8, numbered sources 361, failures 0.

## Reproducibility defenses

- strict JSON duplicate/nonfinite/root checks;
- exact Boolean-versus-integer type checks and canonical byte equality;
- exact semantic recomputation of every mutation surface;
- optimized `python -OO` execution;
- source commit/group/path and release-blob identity checks;
- recursively closed official schema validation;
- individual publication membership and SHA-256 mutation checks;
- byte-identical semantic/build PDFs.

## Final publication replay

- Complete test suite with archive present: 27 passed.
- PDF: 8 A4 pages; clean log, font embedding, text extraction, Ghostscript,
  and all-page raster inspection pass.
- Publication manifest: `RH-385_fixed_publication_manifest`.
- Publication members/external inputs: 29/67.
- Archive verification: `RH-385_archive_verified`; failure count 0.
- Manifest rebuild, result/source-lock match, release-blob identity,
  source-digest contract, exact-certificate digest, and semantic-PDF identity:
  all true.
