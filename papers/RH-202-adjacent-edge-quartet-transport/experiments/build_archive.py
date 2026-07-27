"""Build a stable local publication manifest."""
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRECTORIES = {".pytest_cache", "__pycache__", ".ipynb_checkpoints"}
EXCLUDED_NAMES = {"main.aux", "main.bbl", "main.blg", "main.fdb_latexmk", "main.fls", "main.log", "main.out", "dependency_manifest.json", "archive_verification.json", "batch_dependency_manifest.json", "batch_archive_verification.json"}

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main():
    files = [path for path in ROOT.rglob("*") if path.is_file() and not any(part in EXCLUDED_DIRECTORIES for part in path.relative_to(ROOT).parts) and path.name not in EXCLUDED_NAMES and path.suffix != ".pyc"]
    payload = {"status": f"{ROOT.name}_publication_manifest", "file_count": len(files), "files": {str(path.relative_to(ROOT)): sha256(path) for path in sorted(files)}}
    (ROOT / "results/dependency_manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": "results/dependency_manifest.json", "file_count": len(files)}, sort_keys=True))

if __name__ == "__main__": main()
