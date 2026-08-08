PYTHON ?= python3
export PYTHONPATH := src

RESULT := results/result.json
SCHEMA := results/result.schema.json
PDF := main.pdf
SEMANTIC_PDF := all-order-prime-tail-integral-resummation.pdf

.PHONY: result schema test remote remote-network pdf archive clean

result: $(RESULT)

schema: $(SCHEMA)

$(RESULT): experiments/build_result.py src/integral_resummation/__init__.py src/integral_resummation/core.py results/external_source_lock.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B experiments/build_result.py

$(SCHEMA): $(RESULT) experiments/build_schema.py
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. $(PYTHON) -B experiments/build_schema.py

test: result schema
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B -m pytest -q -p no:cacheprovider

remote:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B experiments/verify_remote_source.py

remote-network:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B experiments/verify_remote_source.py --network

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
