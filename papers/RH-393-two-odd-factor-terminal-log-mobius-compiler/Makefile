PYTHON ?= python3
export PYTHONPATH := src:experiments:.
export PYTHONDONTWRITEBYTECODE := 1

RESULT := results/result.json
SCHEMA := results/result.schema.json
PDF := main.pdf
SEMANTIC_PDF := two-odd-factor-terminal-log-mobius-compiler-and-multi-shift-squarefree-landscape.pdf
REMOTE_VERIFIER := experiments/verify_offline_sources.py

.PHONY: result schema test test-optimized remote pdf archive clean

result: $(RESULT)

schema: $(SCHEMA)

$(RESULT): experiments/build_result.py experiments/source_locks.py src/two_odd_compiler/core.py results/external_source_lock.json results/maynard_external_source_lock.json results/tao_external_source_lock.json
	$(PYTHON) -B experiments/build_result.py

$(SCHEMA): $(RESULT) experiments/build_schema.py
	$(PYTHON) -B experiments/build_schema.py

test: result schema
	$(PYTHON) -B -m pytest -q -p no:cacheprovider

test-optimized: result schema
	$(PYTHON) -OO -B -m pytest -q -p no:cacheprovider

remote:
	$(PYTHON) -B $(REMOTE_VERIFIER) --source johnston-yang-arxiv-2204.01980v2
	$(PYTHON) -B $(REMOTE_VERIFIER) --source maynard-annals-2015-small-gaps
	$(PYTHON) -B $(REMOTE_VERIFIER) --source tao-cambridge-2016-logarithmic-chowla

pdf: $(SEMANTIC_PDF)

$(SEMANTIC_PDF): $(PDF)
	cp $(PDF) $(SEMANTIC_PDF)

archive: result schema pdf
	$(PYTHON) -B experiments/build_archive.py
	$(PYTHON) -B experiments/verify_archive.py

clean:
	@echo "RH-393 manuscript bytes are frozen; no clean target mutates them."
