PYTHON ?= /root/math/.venv/bin/python
export PYTHONPATH := src

RESULT := results/result.json
PDF := main.pdf
SEMANTIC_PDF := square-clock-monotonicity-and-finite-clock-nonattainment.pdf

.PHONY: result test pdf archive clean

result: $(RESULT)

$(RESULT): experiments/build_result.py src/finite_clock_gap/__init__.py src/finite_clock_gap/core.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_result.py

test: result
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m pytest -q -p no:cacheprovider

pdf: $(SEMANTIC_PDF)

$(PDF): main.tex references.bib
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

$(SEMANTIC_PDF): $(PDF)
	cp $(PDF) $(SEMANTIC_PDF)

archive: result pdf
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/build_archive.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) experiments/verify_archive.py

clean:
	latexmk -C
	$(RM) $(SEMANTIC_PDF)
