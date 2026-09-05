# Derivation package

Use the TPC-404 identities
G_0=V_-S_0, G_1=V_-S_1+V_+(S_1-t_1^2), and M=t_1P_-.
Because S_1-t_1^2=sum_{d=1}^{N-2}t_d^2>=0, G_1>=V_-S_1.
Cauchy--Schwarz gives P_-^2<=mV_-; since each selected amplitude is at least
a_min, V_->=m a_min^2. Therefore

    z^2 = t_1^2 P_-^2/(G_0 G_1)
       <= t_1^2 m V_-/(V_-S_0 V_-S_1)
       <= t_1^2/(a_min^2 S_0 S_1).

For integer H>=1, N>=H+2, the terms d=1,...,H occur in both S_0 and S_1.
Since t_d=H^2/(H^2+d^2)>=1/2, both sums are at least H/4. Finally,
for Q<p, a_p=(p/Q)^2 p/(p-1)>1. Taking square roots yields the bound.

This is an exact theorem for the declared selected-prime CRT proxy. The
heights in the certificate are a finite audit of the theorem, not its proof.
