.PHONY: result pdf series archive test all

PYTHON ?= /root/math/.venv/bin/python

result:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_inventory.py

pdf:
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
	cp main.pdf corpus-frontier-synthesis.pdf

series:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_four_volume_archive.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/verify_four_volume_archive.py

archive: result pdf series
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_archive.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/verify_archive.py

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m pytest -q -p no:cacheprovider

all: archive test
