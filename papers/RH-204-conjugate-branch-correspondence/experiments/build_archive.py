import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SD={".pytest_cache","__pycache__",".ipynb_checkpoints"}; SN={"main.aux","main.bbl","main.blg","main.fdb_latexmk","main.fls","main.log","main.out","dependency_manifest.json","archive_verification.json","batch_dependency_manifest.json","batch_archive_verification.json"}
def sha(p):
 d=hashlib.sha256()
 with p.open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):d.update(c)
 return d.hexdigest()
def main():
 fs=sorted(p for p in ROOT.rglob("*") if p.is_file() and not any(x in SD for x in p.relative_to(ROOT).parts) and p.name not in SN and p.suffix!=".pyc"); o={"status":f"{ROOT.name}_publication_manifest","file_count":len(fs),"files":{str(p.relative_to(ROOT)):sha(p) for p in fs}}; (ROOT/"results/dependency_manifest.json").write_text(json.dumps(o,indent=2,sort_keys=True)+"\n");print(json.dumps({"file_count":len(fs)}))
if __name__=="__main__":main()
