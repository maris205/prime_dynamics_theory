# TPC-230 proof package

## Theorem

Let `G` be a matching on a finite set of Hilbert rows `u_q`. Let `D` be total diagonal
mass and `M` the mass on matched vertices. Then

$$
E_{AP}\ge D-M,\qquad D-E_{AP}\le M. \tag{1}
$$

Both bounds are sharp. Consequently, `E_AP<=(1-delta)D` implies `M/D>=delta`.
If all row masses are positive and have ratio at most `kappa`, with `P` rows and `E`
edges, then

$$
\frac MD\le2\kappa\frac EP. \tag{2}
$$

For the literal aligned dilation-four rows, `kappa<=4`, so strict `1/400` saving
requires `E/P>=1/3200`.

## Proof

Because `G` is a matching, the collision decomposition is

$$
E_{AP}=\sum_{q\text{ unmatched}}\|u_q\|^2
+\sum_{(p,r)\in E(G)}\|u_p+u_r\|^2.
$$

The second sum is nonnegative and the first equals `D-M`, proving (1). Choosing
`u_r=-u_p` on every edge makes every matched term vanish and attains equality.
Combining the first inequality with `E_AP<=(1-delta)D` gives the necessary mass
condition.

If `d_min<=||u_q||^2<=d_max`, then at most `2E` vertices are matched, so
`M<=2E d_max`, while `D>=P d_min`. This proves (2).

For the literal aligned rows, `floor(4q/Q)` lies from four through seven. Primitivity
modulo `16Q` leaves at least the two multipliers `+/-1` and at most the eight odd
multipliers through `+/-7`. Equal atom amplitudes make row mass proportional to this
count. Therefore `kappa<=8/2=4`; substituting `delta=1/400` into
`E/P>=delta/(2kappa)` gives `1/3200`. ∎

## Claim boundary

The theorem is deterministic and exact. It does not estimate `E/P` asymptotically and
does not prove comparable actual V59 source masses. It states the toll that any such
mechanism must pay.
