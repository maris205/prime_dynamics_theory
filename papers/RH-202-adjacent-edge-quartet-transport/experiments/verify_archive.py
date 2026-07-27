"""Verify the local publication manifest."""
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main():
    manifest = json.loads((ROOT / "results/dependency_manifest.json").read_text())
    failures = [name for name, expected in manifest["files"].items() if not (ROOT / name).is_file() or sha256(ROOT / name) != expected]
    if failures: raise RuntimeError(f"archive verification failed: {failures}")
    payload = {"status": f"{ROOT.name}_archive_verified", "file_count": manifest["file_count"], "failure_count": 0}
    (ROOT / "results/archive_verification.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))

if __name__ == "__main__": main()
