import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
R=Path(__file__).resolve().parents[1]
def main():
 d=json.loads((R/'results/direct_margin_audit.json').read_text());rows=d['pairs'];chains=d['chains'];fig,a=plt.subplots(1,2,figsize=(10.8,4.2));a[0].hist([r['endpoint_relative_error'] for r in rows],bins=35,alpha=.7,label='modes 1 and 4');a[0].hist([r['full_profile_relative_error'] for r in rows],bins=35,alpha=.55,label='all four modes');a[0].set_xlabel('best scalar-fit error / leading scale');a[0].set_ylabel('pairs');a[0].set_title('Cross-scale scalar alignment');a[0].legend(frameon=False);a[0].grid(True,alpha=.22)
 for c in chains:a[1].plot([x['sigma'] for x in c['levels']],[x['margin_lower'] for x in c['levels']],alpha=.45)
 a[1].axhline(0,color='black',ls='--',lw=1);a[1].invert_xaxis();a[1].set_xlabel('archived scale');a[1].set_ylabel('propagated direct margin lower');a[1].set_title('All 24 chains cross below zero');a[1].grid(True,alpha=.22);fig.tight_layout();o=R/'figures/direct_margin_scale_recurrence';fig.savefig(o.with_suffix('.pdf'),bbox_inches='tight');fig.savefig(o.with_suffix('.png'),dpi=220,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()

