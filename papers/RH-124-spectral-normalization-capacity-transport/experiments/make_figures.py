import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
R=Path(__file__).resolve().parents[1]
def main():
 d=json.loads((R/'results/spectral_transport_audit.json').read_text());rows=d['records'];fig,a=plt.subplots(1,2,figsize=(10.8,4.2));q=np.array([r['q4_ratio']/r['q4_lower'] for r in rows]);v=np.array([r['volume_ratio']/r['volume_lower'] for r in rows]);c=np.array([r['capacity_upper']/r['capacity_ratio'] for r in rows]);a[0].hist(np.log10(q),bins=45,alpha=.65,label='$q_4$');a[0].hist(np.log10(v),bins=45,alpha=.55,label='volume');a[0].hist(np.log10(c),bins=45,alpha=.45,label='capacity upper');a[0].set_xlabel('log10(actual / one-sided bound)');a[0].set_title('Sharp transport envelopes');a[0].legend(frameon=False);a[0].grid(True,alpha=.2)
 r=np.geomspace(1e-4,1,300);a[1].loglog(r,np.sqrt(r),label='direct $q_4$: $r^{1/2}$',lw=2);a[1].loglog(r,r**2.5,label='separate volume/capacity: $r^{5/2}$',lw=2);a[1].set_xlabel('$r=m/M$');a[1].set_ylabel('lower transfer factor');a[1].set_title('Independent-factor loss $r^2$');a[1].legend(frameon=False);a[1].grid(True,which='both',alpha=.22);fig.tight_layout();o=R/'figures/spectral_normalization_capacity_transport';fig.savefig(o.with_suffix('.pdf'),bbox_inches='tight');fig.savefig(o.with_suffix('.png'),dpi=220,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()

