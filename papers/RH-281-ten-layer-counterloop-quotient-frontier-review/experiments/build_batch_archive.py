"""Build the RH-272--RH-281 batch publication manifest."""

from __future__ import annotations

import json

from build_archive import NUMBERS, PAPERS, ROOT, digest, paper_directories, publication_files


def main() -> None:
    files = []
    for directory in paper_directories():
        files.extend(publication_files(directory))
    files = sorted(files)
    payload = {
        "status": "rh272_281_batch_publication_manifest",
        "paper_numbers": list(NUMBERS),
        "file_count": len(files),
        "files": {str(path.relative_to(PAPERS)): digest(path) for path in files},
    }
    output = ROOT / "results/batch_dependency_manifest.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"paper_count": len(NUMBERS), "file_count": len(files)}))


if __name__ == "__main__":
    main()
