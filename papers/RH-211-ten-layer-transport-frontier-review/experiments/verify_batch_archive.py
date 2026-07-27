"""Verify the RH-202--RH-211 publication manifest."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PAPERS=ROOT.parent
def h(p):
 x=hashlib.sha256()
 with p.open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):x.update(c)
 return x.hexdigest()
def main():
 m=json.loads((ROOT/"results/batch_dependency_manifest.json").read_text());b=[n for n,v in m["files"].items() if not (PAPERS/n).is_file() or h(PAPERS/n)!=v]
 if b:raise RuntimeError(b)
 o={"status":"rh202_211_batch_archive_verified","paper_numbers":m["paper_numbers"],"file_count":m["file_count"],"failure_count":0};(ROOT/"results/batch_archive_verification.json").write_text(json.dumps(o,indent=2,sort_keys=True)+"\n");print(json.dumps(o))
if __name__=="__main__":main()
