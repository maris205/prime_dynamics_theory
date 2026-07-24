import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
R=Path(__file__).resolve().parents[1]
def main():
 d=json.loads((R/'results/eventual_support_audit.json').read_text());fig,a=plt.subplots(1,2,figsize=(10.8,4.2));rho=np.linspace(0,.95,250);x=np.linspace(0,.95,250);rr,xx=np.meshgrid(rho,x);floor=(1-np.sqrt(xx))**4;im=a[0].pcolormesh(rr,xx,floor,shading='auto',cmap='viridis');a[0].set_xlabel(r'$\rho$');a[0].set_ylabel(r'fixed point $q/(1-\rho)$');a[0].set_title('Rayleigh support factor');fig.colorbar(im,ax=a[0],label=r'$(1-\sqrt{x_*})^4$')
 for r in (.2,.5,.8,.95):
  q=.2*(1-r);vals=[.9]
  for _ in range(60):vals.append(r*vals[-1]+q)
  a[1].plot(vals,label=fr'$\rho={r}$')
 a[1].axhline(.2,color='black',ls='--',label='fixed point');a[1].set_xlabel('level');a[1].set_ylabel(r'$\gamma_n^2$ upper');a[1].set_title('Contractive affine envelopes');a[1].legend(frameon=False,fontsize=8);a[1].grid(True,alpha=.22);fig.tight_layout();o=R/'figures/conditional_eventual_directional_support';fig.savefig(o.with_suffix('.pdf'),bbox_inches='tight');fig.savefig(o.with_suffix('.png'),dpi=220,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()

