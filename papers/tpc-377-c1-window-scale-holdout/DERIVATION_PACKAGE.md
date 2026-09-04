# TPC-377 derivation package

## 1. Finite scale family

For an origin a, count N in (1024,1536,2048), and a shell anchor Q, use
the finite kernel

K_p(u,t) = p (p/Q)^2 66^2/(66^2+(u-t)^2)
 (1_{p|(u-t)} - 1/(p-1)) 1_{u!=t}1_{p not|u}1_{p not|t}.

The all-plus matrix is A=sum_p K_p, and its geometry is
G(u)=sum_t sum_p K_p(u,t)^2. Normalize by
T(u,t)=A(u,t)/sqrt(G(u)G(t)).

## 2. Exact finite identities

The geometry is a finite sum of nonnegative rational squares. For the
fixed block length 256, let b_N(u)=floor((u-a)/256). The mask
|b_N(u)-b_N(t)|<=1 defines B_1, and R_1=T-B_1 entrywise. Thus for
any selected unit eigenvector v of T,
v^T B_1 v + v^T R_1 v = v^T T v.

For a fixed origin the three count windows are nested prefixes with the
same left endpoint. This is an exact protocol relation, not a claim that
the corresponding matrices are restrictions of one normalized operator.

## 3. Finite outcome

The completed certificate records the count-by-Q failure table, the
row-level spectra and Schur values, and the selected-mode band/tail
Rayleigh fractions. The certified finite comparison is
[[0,3,3],[0,3,3],[0,3,3]], with rows ordered by
N=(1024,1536,2048) and columns by Q=(512,2048,8192).

## 4. Claim ceiling

Even a complete match is only finite scoped evidence for this declared
scale ladder. It does not prove origin uniformity, window-scale
uniformity, cross-block causality, a growing operator bound, source-uniform
arithmetic L2, a power saving, Route-B reassembly, or a twin-prime
theorem.
