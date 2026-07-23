from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PAPERS=ROOT.parent;REPO=PAPERS.parent
def sha(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 return h.hexdigest()
def main():
 ext={'rh110_audit':PAPERS/'RH-110-finite-memory-three-mode-capacity/results/three_mode_capacity_audit.json','rh112_summary':PAPERS/'RH-112-global-wedge-lipschitz-barrier/results/summary.json'};local=sorted({*(ROOT/'src').rglob('*.py'),*(ROOT/'experiments').glob('*.py'),*(ROOT/'tests').glob('*.py')});pubs=[ROOT/n for n in ('.gitignore','README.md','THEOREM_LEDGER.md','UPDATED_ROADMAP.md','main.tex','references.bib','pyproject.toml','requirements.txt','figures/right_frame_directional_wedge.pdf','figures/right_frame_directional_wedge.png','main.pdf','right-frame-directional-wedge.pdf')]
 dep={'status':'all_rh113_inputs_sources_and_publication_artifacts_hashed','external_inputs':{k:{'path':str(v.relative_to(REPO)),'sha256':sha(v)} for k,v in ext.items()},'local_sources':{str(v.relative_to(ROOT)):sha(v) for v in local},'publication_artifacts':{str(v.relative_to(ROOT)):sha(v) for v in pubs}};dp=ROOT/'results/dependency_manifest.json';dp.write_text(json.dumps(dep,indent=2,sort_keys=True)+'\n');audit=json.loads((ROOT/'results/directional_wedge_audit.json').read_text());rps=[ROOT/'results/directional_wedge_audit.json',ROOT/'results/directional_wedge_smoke.json',dp];summary={'status':'rh113_right_frame_directional_wedge_archived','theorem':{'directional_frame_variational_certificate':True,'approximate_action_weyl_certificate':True,'recent_frame_recovers_product_weyl':True},'audit':audit['audit_summary'],'threshold_summary':audit['threshold_summary'],'program_boundary':audit['theorem_boundary'],'route_consequence':audit['route_consequence'],'result_hashes':{str(v.relative_to(ROOT)):sha(v) for v in rps},'publication_artifact_hashes':dep['publication_artifacts']};sp=ROOT/'results/summary.json';sp.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');print(json.dumps({'summary':str(sp.relative_to(ROOT)),**audit['audit_summary']},sort_keys=True))
if __name__=='__main__':main()
