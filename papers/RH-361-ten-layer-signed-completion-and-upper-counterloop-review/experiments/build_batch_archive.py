"""Build the RH-352--RH-361 batch publication manifest."""

from __future__ import annotations

import json

from build_archive import NUMBERS, PAPERS, ROOT, digest, paper_directories, publication_files


def main() -> None:
    files = []
    for directory in paper_directories():
        files.extend(publication_files(directory))
    files = sorted(files)
    payload = {
        "status": "rh352_361_batch_publication_manifest",
        "paper_numbers": list(NUMBERS),
        "file_count": len(files),
        "files": {str(path.relative_to(PAPERS)): digest(path) for path in files},
    }
    (ROOT / "results/batch_dependency_manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"paper_count": len(NUMBERS), "file_count": len(files)}))


if __name__ == "__main__":
    main()
