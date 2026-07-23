"""Create RH-115 composite-gate figures."""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def main()->None:
 data=json.loads((ROOT/'results/composite_gate_audit.json').read_text());keys=['1e-08','1e-06','1e-04'];labels=[r'$10^{-8}$',r'$10^{-6}$',r'$10^{-4}$'];fig,axes=plt.subplots(1,2,figsize=(10.9,4.25));ax=axes[0];x=np.arange(3);width=.18
 series=[('direct_weyl','direct Weyl'),('tail_energy_trace','tail-energy trace'),('psd_packet_block','PSD packet block')]
 for offset,(name,label) in zip((-.27,-.09,.09),series):ax.bar(x+offset,[data['threshold_summary'][k]['candidate_support_counts'][name] for k in keys],width,label=label)
 ax.bar(x+.27,[data['threshold_summary'][k]['composite_support_count'] for k in keys],width,label='admitted composite');ax.set_xticks(x,labels);ax.set_ylim(88,120);ax.set_ylabel('certified updates (of 120)');ax.set_title('Full-chain support counts');ax.grid(True,axis='y',alpha=.25);ax.legend(frameon=False,fontsize=7)
 ax=axes[1];steps=[s for r in data['rows'] for c in r['channels'] for q in c['thresholds'] if float(q['threshold'])==1e-8 for s in q['steps']];improvement=np.array([s['improvement_over_direct'] for s in steps]);ax.plot(np.arange(len(steps)),improvement,lw=1.4,label='admitted composite - direct');bad=[(i,s['diagnostic_exact_directional']-s['actual_ratio']) for i,s in enumerate(steps) if not s['diagnostic_exact_dominance_holds']]
 if bad:ax.scatter([i for i,_ in bad],[v for _,v in bad],color='tab:red',zorder=3,label='excluded exact excess')
 ax.axhline(0,color='black',lw=.8);ax.set_xlabel('archived update');ax.set_ylabel(r'$q_4$ lower-bound increment');ax.set_title('Gain and outward-admissibility filter');ax.grid(True,alpha=.25);ax.legend(frameon=False,fontsize=8)
 fig.tight_layout();out=ROOT/'figures/composite_directional_support_gate';out.parent.mkdir(parents=True,exist_ok=True);fig.savefig(out.with_suffix('.pdf'),bbox_inches='tight');fig.savefig(out.with_suffix('.png'),dpi=220,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()
