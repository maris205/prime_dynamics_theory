PYTHON ?= /root/math/.venv/bin/python

.PHONY: audit test pdf archive verify all

audit:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_volume_audit.py

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m pytest -q -p no:cacheprovider

pdf:
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
	cp main.pdf noisy-head-annulus-signed-completion-synthesis.pdf

archive:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_archive.py

verify:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/verify_archive.py

all: audit test pdf archive verify
