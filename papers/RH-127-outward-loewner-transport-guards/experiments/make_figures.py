import json
from pathlib import Path
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
def main():
 d=json.loads((R/'results/outward_guard_audit.json').read_text());rows=d['records'];fig,a=plt.subplots(1,2,figsize=(10.7,4.2));a[0].hist([r['gram_guard_ratio'] for r in rows],bins=45,alpha=.75,label='Gram guard/slack');a[0].hist([r['tail_guard_ratio'] for r in rows],bins=45,alpha=.55,label='tail guard/slack');a[0].axvline(1,color='black',ls='--');a[0].set_xlabel('required guard / numerical slack');a[0].set_ylabel('certified pairs');a[0].set_title('Outward certification reserve');a[0].legend(frameon=False);a[0].grid(True,alpha=.22)
 x=[.5,1,2,4,8];a[1].plot(x,[z*z for z in x],marker='o');a[1].set_xlabel(r'$\|S\|$');a[1].set_ylabel('radius amplification');a[1].set_title(r'Congruence cost is exactly $\|S\|^2$');a[1].grid(True,alpha=.22);fig.tight_layout();o=R/'figures/outward_loewner_transport_guards';fig.savefig(o.with_suffix('.pdf'),bbox_inches='tight');fig.savefig(o.with_suffix('.png'),dpi=220,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()

