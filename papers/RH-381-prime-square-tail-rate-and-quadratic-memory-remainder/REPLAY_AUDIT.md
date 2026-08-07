# RH-381 replay audit

Status: **PASS**

The fixed replay is:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf prime-square-tail-rate-and-quadratic-memory-remainder.pdf
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /root/math/.venv/bin/python experiments/verify_archive.py
```

Exact replay counts:

- 20 tests passed;
- 25 source locks and 25 release-blob identities passed;
- 6 exact run/Euler rows passed;
- 4 exact finite tail-identity rows passed;
- 6 directed interval rows passed at precision 60;
- 9,592 primes through cutoff 100,000 were enumerated;
- the exact fixture is 2,574 bytes with SHA-256
  `d55fd48071eb5b88c054f3d34329f274f792f2bbd859b4ab98e31b5b7020beb8`;
- the directed fixture is 6,851 bytes with SHA-256
  `e0342f871b1f952039da2b1025fa7598771b9fa089295f07cb60b11f70cee15c`;
- all four strict constant/type gates, duplicate source-lock rows,
  source/path/group/commit/digest mutations, schema mutations, non-finite
  JSON mutations, and optimized-mode replay behaved fail closed;
- all five Gate flags remained false.

Archive acceptance requires exactly 28 fixed publication members and 25
external inputs, result/source-lock identity, release-blob identity,
independent interval-digest identity, semantic-PDF identity, manifest rebuild
identity, and zero verification failures.
