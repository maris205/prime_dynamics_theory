import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
 d=hashlib.sha256()
 with p.open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):d.update(c)
 return d.hexdigest()
def main():
 m=json.loads((ROOT/"results/dependency_manifest.json").read_text());b=[n for n,h in m["files"].items() if not (ROOT/n).is_file() or sha(ROOT/n)!=h]
 if b:raise RuntimeError(b)
 o={"status":f"{ROOT.name}_archive_verified","file_count":m["file_count"],"failure_count":0};(ROOT/"results/archive_verification.json").write_text(json.dumps(o,indent=2,sort_keys=True)+"\n");print(json.dumps(o))
if __name__=="__main__":main()
