"""Build a stable local publication manifest."""
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKIPDIR={".pytest_cache","__pycache__",".ipynb_checkpoints"}; SKIP={"main.aux","main.bbl","main.blg","main.fdb_latexmk","main.fls","main.log","main.out","dependency_manifest.json","archive_verification.json","batch_dependency_manifest.json","batch_archive_verification.json"}
def sha(path):
 d=hashlib.sha256()
 with path.open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""): d.update(c)
 return d.hexdigest()
def main():
 files=sorted(p for p in ROOT.rglob("*") if p.is_file() and not any(x in SKIPDIR for x in p.relative_to(ROOT).parts) and p.name not in SKIP and p.suffix!=".pyc")
 out={"status":f"{ROOT.name}_publication_manifest","file_count":len(files),"files":{str(p.relative_to(ROOT)):sha(p) for p in files}}
 (ROOT/"results/dependency_manifest.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); print(json.dumps({"file_count":len(files)}))
if __name__=="__main__": main()
