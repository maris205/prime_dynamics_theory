PYTHON ?= /root/math/.venv/bin/python
export PYTHONPATH := src

RESULT := results/result.json
SCHEMA := results/result.schema.json
PDF := main.pdf
SEMANTIC_PDF := polylogarithmic-clock-phasewise-memory-uniformization.pdf

.PHONY: result schema test pdf archive clean

result: $(RESULT)

schema: $(SCHEMA)

$(RESULT): experiments/build_result.py src/polylog_clock/__init__.py src/polylog_clock/core.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B experiments/build_result.py

$(SCHEMA): $(RESULT) experiments/build_schema.py
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. $(PYTHON) -B experiments/build_schema.py

test: result schema
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B -m pytest -q -p no:cacheprovider

pdf: $(SEMANTIC_PDF)

$(PDF): main.tex references.bib
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

$(SEMANTIC_PDF): $(PDF)
	cp $(PDF) $(SEMANTIC_PDF)

archive: result schema pdf
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B experiments/build_archive.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B experiments/verify_archive.py

clean:
	latexmk -C
	$(RM) $(SEMANTIC_PDF)
