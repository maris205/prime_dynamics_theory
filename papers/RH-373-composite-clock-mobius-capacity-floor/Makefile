PYTHON ?= python3
PYTEST ?= pytest
export PYTHONPATH := src

RESULT := results/result.json
PDF := main.pdf
SEMANTIC_PDF := composite-clock-mobius-capacity-floor.pdf

.PHONY: result test pdf archive clean

result: $(RESULT)

$(RESULT): experiments/build_result.py src/composite_clock/core.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_result.py

test: result
	PYTHONDONTWRITEBYTECODE=1 $(PYTEST) -q

pdf: $(PDF)
	cp $(PDF) $(SEMANTIC_PDF)

$(PDF): main.tex references.bib README.md THEOREM_LEDGER.md
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

archive: result pdf
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_archive.py

clean:
	latexmk -C
