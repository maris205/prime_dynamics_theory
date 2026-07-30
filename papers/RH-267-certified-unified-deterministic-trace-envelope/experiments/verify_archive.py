"""Verify publication manifest."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(p):
 h=hashlib.sha256();
 with p.open("rb") as s:
  for c in iter(lambda:s.read(1<<20),b""):h.update(c)
 return h.hexdigest()
def main():
 m=json.loads((ROOT/"results/dependency_manifest.json").read_text()); f=[]
 for r,e in m["files"].items():
  p=ROOT/r
  if not p.is_file():f.append({"file":r,"reason":"missing"})
  elif digest(p)!=e:f.append({"file":r,"reason":"sha256_mismatch"})
 d={"status":f"{ROOT.name}_archive_verified","file_count":m["file_count"],"failure_count":len(f),"failures":f};(ROOT/"results/archive_verification.json").write_text(json.dumps(d,indent=2,sort_keys=True)+"\n");print(json.dumps(d,sort_keys=True));
 if f:raise SystemExit(1)
if __name__=="__main__":main()
