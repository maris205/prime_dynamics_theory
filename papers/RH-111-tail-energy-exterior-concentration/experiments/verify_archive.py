from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
def sha(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 return h.hexdigest()
def load(n):return json.loads((ROOT/n).read_text())
def main():
 s=load('results/summary.json'); d=load('results/dependency_manifest.json'); a=load('results/exterior_concentration_audit.json')
 for k,v in s['result_hashes'].items():assert sha(ROOT/k)==v
 for k,v in d['local_sources'].items():assert sha(ROOT/k)==v
 for k,v in d['publication_artifacts'].items():assert sha(ROOT/k)==v
 for v in d['external_inputs'].values():assert sha(REPO/v['path'])==v['sha256']
 x=a['audit_summary']; assert (x['scale_count'],x['channel_count'],x['update_count'],x['fine_update_count'])==(5,10,360,234); assert x['concentration_enclosure_failure_count']==0
 expected={'1e-08':(78,78,78),'1e-06':(65,69,72),'1e-04':(42,55,55)}
 for k,c in expected.items():
  z=a['threshold_summary'][k];assert (z['fine_generic_support_count'],z['fine_refined_support_count'],z['fine_spectral_support_count'])==c
 for k in ('all_level_exterior_concentration_law_proved','all_level_physical_volume_lower_bound_proved','uniform_stage_A_closed','hilbert_polya_operator','riemann_hypothesis'):assert not a['theorem_boundary'][k]
 text=' '.join((ROOT/'main.tex').read_text().lower().split())
 for p in ('tail-energy concentration upper bound','refined trace exterior certificate','hilbert--polya','riemann hypothesis'):assert p in text
 archived=[ROOT/n for n in ('.gitignore','README.md','THEOREM_LEDGER.md','UPDATED_ROADMAP.md','main.tex','references.bib','pyproject.toml','requirements.txt','main.pdf','tail-energy-exterior-concentration.pdf','figures/tail_energy_exterior_concentration.pdf','figures/tail_energy_exterior_concentration.png','results/exterior_concentration_audit.json','results/exterior_concentration_smoke.json','results/dependency_manifest.json','results/summary.json')]
 files={str(v.relative_to(ROOT)):sha(v) for v in archived}; out=ROOT/'results/archive_verification.json';out.write_text(json.dumps({'status':'all_rh111_archive_hashes_verified','file_count':len(files),'files':files},indent=2,sort_keys=True)+'\n');print(json.dumps({'output':str(out.relative_to(ROOT)),'file_count':len(files),'status':'all_rh111_archive_hashes_verified'},sort_keys=True))
if __name__=='__main__':main()
