import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def main():
 d=json.loads((ROOT/'results/defect_recurrence_audit.json').read_text());e=np.array([r['efficiency'] for r in d['records']]);fig,ax=plt.subplots(1,2,figsize=(10.7,4.2));ax[0].hist(e,bins=50,color='tab:blue',alpha=.82);ax[0].axvline(1,color='black');ax[0].set_xlabel('actual / affine upper');ax[0].set_ylabel('random defect pairs');ax[0].set_title('One-step theorem efficiency');ax[0].grid(True,alpha=.22)
 for rho in (.2,.5,.8,.95,1.05):
  vals=[.4]
  for _ in range(60):vals.append(rho*vals[-1]+.02)
  ax[1].plot(vals,label=fr'$\rho={rho}$')
 ax[1].axhline(1,color='black',ls='--',lw=1);ax[1].set_xlabel('step');ax[1].set_ylabel(r'upper for $\gamma^2$');ax[1].set_yscale('log');ax[1].set_title('Affine recurrence regimes');ax[1].legend(frameon=False,fontsize=8);ax[1].grid(True,alpha=.22);fig.tight_layout();o=ROOT/'figures/defect_stable_rayleigh_recurrence';fig.savefig(o.with_suffix('.pdf'),bbox_inches='tight');fig.savefig(o.with_suffix('.png'),dpi=220,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()

