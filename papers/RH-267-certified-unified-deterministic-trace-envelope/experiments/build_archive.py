"""Build publication manifest."""
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; EXD={".pytest_cache","__pycache__",".ipynb_checkpoints"}; EXN={"main.aux","main.bbl","main.blg","main.fdb_latexmk","main.fls","main.log","main.out","dependency_manifest.json","archive_verification.json"}
def digest(p):
 h=hashlib.sha256();
 with p.open("rb") as s:
  for c in iter(lambda:s.read(1<<20),b""):h.update(c)
 return h.hexdigest()
def main():
 f=sorted(p for p in ROOT.rglob("*") if p.is_file() and not any(x in EXD for x in p.relative_to(ROOT).parts) and p.name not in EXN and p.suffix!=".pyc"); d={"status":f"{ROOT.name}_publication_manifest","file_count":len(f),"files":{str(p.relative_to(ROOT)):digest(p) for p in f}}; (ROOT/"results/dependency_manifest.json").write_text(json.dumps(d,indent=2,sort_keys=True)+"\n"); print(json.dumps({"file_count":len(f)}))
if __name__=="__main__":main()
