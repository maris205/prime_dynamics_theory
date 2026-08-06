PYTHON := /root/math/.venv/bin/python
SEMANTIC_PDF := branch-symmetric-markov-mobius-orthogonality.pdf

.PHONY: result test pdf archive

result:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. $(PYTHON) experiments/build_result.py

test: result
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. $(PYTHON) -m pytest -q -p no:cacheprovider

pdf:
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
	cp main.pdf $(SEMANTIC_PDF)

archive: result pdf
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. $(PYTHON) experiments/build_archive.py
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. $(PYTHON) experiments/verify_archive.py
