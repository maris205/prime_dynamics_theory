import json
from pathlib import Path
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
def main():
 d=json.loads((R/'results/ten_layer_review_audit.json').read_text());fig,a=plt.subplots(1,2,figsize=(11.2,4.5));colors={'constructive':'tab:blue','negative':'tab:red','synthesis':'tab:green'}
 for i,x in enumerate(d['layers']):a[0].bar(x['number'],1,color=colors[x['class']]);a[0].text(x['number'],.5,str(x['number']),ha='center',va='center',rotation=90,color='white',fontsize=8)
 a[0].set_xlim(119.3,129.7);a[0].set_ylim(0,1.12);a[0].set_yticks([]);a[0].set_xlabel('RH layer');a[0].set_title('Five constructive, two obstruction, three synthesis layers')
 labels=['direct','trace','directional'];sizes=[1,1,2];a[1].bar(labels,sizes,color=['tab:orange','tab:purple','tab:green']);a[1].set_ylabel('unproved mathematical inputs');a[1].set_ylim(0,2.5);a[1].set_title('Inclusion-minimal physical frontier');a[1].text(2,2.12,'gamma recurrence + base liminf',ha='center',fontsize=9);a[1].text(.98,.95,'+ outward radii for independent paths',transform=a[1].transAxes,ha='right',fontsize=8,color='firebrick');a[1].grid(True,axis='y',alpha=.2);fig.tight_layout();o=R/'figures/ten_layer_gauge_recurrence_review';fig.savefig(o.with_suffix('.pdf'),bbox_inches='tight');fig.savefig(o.with_suffix('.png'),dpi=220,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()

