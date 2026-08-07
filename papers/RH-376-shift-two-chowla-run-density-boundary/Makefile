PYTHON ?= /root/math/.venv/bin/python
export PYTHONPATH := src

RESULT := results/result.json
PDF := main.pdf
SEMANTIC_PDF := shift-two-chowla-run-density-boundary.pdf

.PHONY: result test pdf archive clean

result: $(RESULT)

$(RESULT): experiments/build_result.py src/shift_two_chowla/core.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_result.py

test: result
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m pytest -q -p no:cacheprovider

pdf: $(PDF)
	cp $(PDF) $(SEMANTIC_PDF)

$(PDF): main.tex references.bib README.md THEOREM_LEDGER.md INTEGRITY_AUDIT.md
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

archive: result pdf
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_archive.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/verify_archive.py

clean:
	latexmk -C
