import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];D={".pytest_cache","__pycache__",".ipynb_checkpoints"};N={"main.aux","main.bbl","main.blg","main.fdb_latexmk","main.fls","main.log","main.out","dependency_manifest.json","archive_verification.json","batch_dependency_manifest.json","batch_archive_verification.json"}
def h(p):
 x=hashlib.sha256()
 with p.open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):x.update(c)
 return x.hexdigest()
def main():
 fs=sorted(p for p in R.rglob("*") if p.is_file() and not any(q in D for q in p.relative_to(R).parts) and p.name not in N and p.suffix!=".pyc");o={"status":f"{R.name}_publication_manifest","file_count":len(fs),"files":{str(p.relative_to(R)):h(p) for p in fs}};(R/"results/dependency_manifest.json").write_text(json.dumps(o,indent=2,sort_keys=True)+"\n");print(json.dumps({"file_count":len(fs)}))
if __name__=="__main__":main()
