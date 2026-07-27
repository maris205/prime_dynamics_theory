"""Build the RH-202--RH-211 publication manifest."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PAPERS=ROOT.parent;NUMBERS=tuple(range(202,212));D={".pytest_cache","__pycache__",".ipynb_checkpoints"};N={"main.aux","main.bbl","main.blg","main.fdb_latexmk","main.fls","main.log","main.out","dependency_manifest.json","archive_verification.json","batch_dependency_manifest.json","batch_archive_verification.json"}
def h(p):
 x=hashlib.sha256()
 with p.open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):x.update(c)
 return x.hexdigest()
def dirs():
 out=[]
 for n in NUMBERS:
  m=tuple(PAPERS.glob(f"RH-{n}-*"))
  if len(m)!=1:raise RuntimeError(f"expected one RH-{n}, found {len(m)}")
  out.append(m[0])
 return out
def main():
 fs=[]
 for d in dirs():fs.extend(p for p in d.rglob("*") if p.is_file() and not any(q in D for q in p.relative_to(d).parts) and p.name not in N and p.suffix!=".pyc")
 fs=sorted(fs);o={"status":"rh202_211_batch_publication_manifest","paper_numbers":list(NUMBERS),"file_count":len(fs),"files":{str(p.relative_to(PAPERS)):h(p) for p in fs}};(ROOT/"results/batch_dependency_manifest.json").write_text(json.dumps(o,indent=2,sort_keys=True)+"\n");print(json.dumps({"file_count":len(fs)}))
if __name__=="__main__":main()
