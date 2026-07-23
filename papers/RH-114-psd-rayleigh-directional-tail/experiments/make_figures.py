"""Create RH-114 PSD-Rayleigh figures."""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def main()->None:
 data=json.loads((ROOT/'results/psd_rayleigh_audit.json').read_text());base=[]
 for row in data['rows']:
  for channel in row['channels']:
   rec=next(r for r in channel['thresholds'] if float(r['threshold'])==1e-8);base.extend((row['sigma'],s) for s in rec['steps'])
 sigmas=np.array([x for x,_ in base]);fig,axes=plt.subplots(1,2,figsize=(10.9,4.25));ax=axes[0]
 for name,label,color in [('scalar_gamma','scalar $\\delta^2 I$','tab:red'),('block_gamma','PSD block','tab:blue'),('exact_gamma','exact directional','tab:green')]:
  values=np.array([s[name] for _,s in base]);means=[];locations=[]
  for sigma in sorted(set(sigmas),reverse=True):
   locations.append(sigma);means.append(np.median(values[sigmas==sigma]))
  ax.plot(locations,means,'o-',label=label,color=color)
 ax.set_xscale('log');ax.set_yscale('log');ax.set_xlabel(r'scale $\sigma$');ax.set_ylabel(r'generalized tail constant $\gamma$');ax.set_title('Directional relative tail');ax.grid(True,which='both',alpha=.25);ax.legend(frameon=False,fontsize=8)
 ax=axes[1];names=['scalar_relative_lower','block_relative_lower','exact_relative_lower','product_weyl_lower'];labels=['scalar PSD','packet-block PSD','exact relative','product Weyl'];width=.18;x=np.arange(4)
 vals=[np.median([s[n] for _,s in base]) for n in names];ax.bar(x,vals,width=.62,color=['tab:red','tab:blue','tab:green','tab:gray']);ax.set_xticks(x,labels,rotation=22,ha='right');ax.set_yscale('log');ax.set_ylabel('median normalized lower bound');ax.set_title('Certificate comparison at $10^{-8}$');ax.grid(True,axis='y',which='both',alpha=.25)
 fig.tight_layout();out=ROOT/'figures/psd_rayleigh_directional_tail';out.parent.mkdir(parents=True,exist_ok=True);fig.savefig(out.with_suffix('.pdf'),bbox_inches='tight');fig.savefig(out.with_suffix('.png'),dpi=220,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()
