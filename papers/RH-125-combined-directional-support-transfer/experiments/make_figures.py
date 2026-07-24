import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
R=Path(__file__).resolve().parents[1]
def main():
 d=json.loads((R/'results/combined_transfer_audit.json').read_text());rows=d['pairs'];chains=d['chains'];fig,a=plt.subplots(1,2,figsize=(10.9,4.25));edges=[(.16,.08),(.08,.04),(.04,.02),(.02,.01)];vals=[[r['efficiency'] for r in rows if (r['source_sigma'],r['target_sigma'])==e] for e in edges];a[0].boxplot(vals,tick_labels=['.16→.08','.08→.04','.04→.02','.02→.01']);a[0].set_yscale('log');a[0].set_ylabel('transferred lower / target candidate');a[0].set_title('One-step combined efficiency');a[0].grid(True,axis='y',alpha=.22)
 for c in chains:a[1].plot([x['sigma'] for x in c['levels']],[x['lower'] for x in c['levels']],alpha=.45)
 a[1].invert_xaxis();a[1].set_yscale('log');a[1].axhline(1e-8,color='black',ls='--',lw=1,label='$10^{-8}$');a[1].set_xlabel('archived scale');a[1].set_ylabel('propagated regularized lower');a[1].set_title('Twenty-four five-scale chains');a[1].legend(frameon=False);a[1].grid(True,which='both',alpha=.22);fig.tight_layout();o=R/'figures/combined_directional_support_transfer';fig.savefig(o.with_suffix('.pdf'),bbox_inches='tight');fig.savefig(o.with_suffix('.png'),dpi=220,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()

