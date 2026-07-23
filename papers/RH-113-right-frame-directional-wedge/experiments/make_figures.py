"""Create RH-113 right-frame figures."""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def main()->None:
 data=json.loads((ROOT/'results/directional_wedge_audit.json').read_text());base=[]
 for row in data['rows']:
  for channel in row['channels']:
   record=next(r for r in channel['thresholds'] if float(r['threshold'])==1e-8);base.extend((row['sigma'],s) for s in record['steps'])
 fig,axes=plt.subplots(1,2,figsize=(10.9,4.25));ax=axes[0];sigmas=np.array([x for x,_ in base]);loss=np.array([max(1-s['capture_ratio'],1e-17) for _,s in base])
 for sigma in sorted(set(sigmas),reverse=True):
  values=loss[sigmas==sigma];ax.scatter(np.full(values.size,sigma),values,s=16,alpha=.75)
 ax.set_xscale('log');ax.set_yscale('log');ax.set_xlabel(r'scale $\sigma$');ax.set_ylabel(r'$1-$ recent-frame capture');ax.set_title('Four-frame variational loss');ax.grid(True,which='both',alpha=.25)
 ax=axes[1];gain=np.array([s['directional_tail_gain'] for _,s in base])
 for sigma in sorted(set(sigmas),reverse=True):
  values=gain[sigmas==sigma];ax.scatter(np.full(values.size,sigma),values,s=16,alpha=.75)
 ax.axhline(1,color='black',lw=1,ls='--');ax.set_xscale('log');ax.set_xlabel(r'scale $\sigma$');ax.set_ylabel('global / frame-tail radius');ax.set_title('Directional tail resolution');ax.grid(True,which='both',alpha=.25)
 fig.tight_layout();out=ROOT/'figures/right_frame_directional_wedge';out.parent.mkdir(parents=True,exist_ok=True);fig.savefig(out.with_suffix('.pdf'),bbox_inches='tight');fig.savefig(out.with_suffix('.png'),dpi=220,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()
