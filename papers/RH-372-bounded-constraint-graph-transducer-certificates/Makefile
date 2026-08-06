.PHONY: result pdf test archive

PYTHON ?= /root/math/.venv/bin/python

result:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. $(PYTHON) experiments/build_result.py

pdf:
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
	cp main.pdf bounded-constraint-graph-transducer-certificates.pdf

test:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. $(PYTHON) -m pytest -q -p no:cacheprovider

archive: result pdf
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. $(PYTHON) experiments/build_archive.py
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. $(PYTHON) experiments/verify_archive.py
