PYTHON := /root/math/.venv/bin/python
SEMANTIC_PDF := terminal-lag-exponential-tilt-phase-transition.pdf

.PHONY: result test pdf archive clean

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

clean:
	latexmk -c
