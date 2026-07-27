import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def h(p):
 x=hashlib.sha256()
 with p.open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):x.update(c)
 return x.hexdigest()
def main():
 m=json.loads((R/"results/dependency_manifest.json").read_text());b=[n for n,v in m["files"].items() if not (R/n).is_file() or h(R/n)!=v]
 if b:raise RuntimeError(b)
 o={"status":f"{R.name}_archive_verified","file_count":m["file_count"],"failure_count":0};(R/"results/archive_verification.json").write_text(json.dumps(o,indent=2,sort_keys=True)+"\n");print(json.dumps(o))
if __name__=="__main__":main()
