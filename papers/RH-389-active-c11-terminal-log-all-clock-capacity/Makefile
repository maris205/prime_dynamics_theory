PYTHON ?= python3
export PYTHONPATH := src:.

RESULT := results/result.json
SCHEMA := results/result.schema.json
PDF := main.pdf
SEMANTIC_PDF := active-c11-terminal-log-all-clock-capacity.pdf
RH387_JY_VERIFIER := ../RH-387-all-order-prime-tail-integral-resummation/experiments/verify_remote_source.py
RH388_MAYNARD_VERIFIER := ../RH-388-rank-one-p2-tail-resummation/experiments/verify_remote_source.py

.PHONY: result schema test remote remote-network remote-network-jy remote-network-maynard remote-network-tao pdf archive clean

result: $(RESULT)

schema: $(SCHEMA)

$(RESULT): experiments/build_result.py experiments/source_locks.py src/terminal_log_capacity/__init__.py src/terminal_log_capacity/core.py results/external_source_lock.json results/maynard_external_source_lock.json results/tao_external_source_lock.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B experiments/build_result.py

$(SCHEMA): $(RESULT) experiments/build_schema.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B experiments/build_schema.py

test: result schema
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B -m pytest -q -p no:cacheprovider

remote:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B $(RH387_JY_VERIFIER)
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B $(RH388_MAYNARD_VERIFIER)
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B experiments/verify_tao_source.py

remote-network-jy:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B $(RH387_JY_VERIFIER) --network

remote-network-maynard:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B $(RH388_MAYNARD_VERIFIER) --network

remote-network-tao:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B experiments/verify_tao_source.py --network

remote-network: remote-network-jy remote-network-maynard remote-network-tao

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
