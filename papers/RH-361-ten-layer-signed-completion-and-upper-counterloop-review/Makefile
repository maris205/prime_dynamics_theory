PYTHON := /root/math/.venv/bin/python
SEMANTIC_PDF := ten-layer-signed-completion-and-upper-counterloop-review.pdf

.PHONY: result test pdf archive batch

result:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_result.py

test: result
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m pytest -q -p no:cacheprovider

pdf:
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
	cp main.pdf $(SEMANTIC_PDF)

archive: result pdf
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_archive.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/verify_archive.py

batch: archive
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_batch_archive.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/verify_batch_archive.py
