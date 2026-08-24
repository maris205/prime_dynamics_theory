# TPC-230 derivation package

## 1. Mass decomposition

For a matching graph, let

$$
D=\sum_q\|u_q\|^2,\qquad
M=\sum_{q\text{ matched}}\|u_q\|^2,
\qquad U=D-M.
$$

The global AP energy decomposes exactly as

$$
E_{AP}=U+\sum_{(p,r)}\|u_p+u_r\|^2\ge U=D-M.
$$

Hence `D-E_AP<=M`. Equality is attained by `u_r=-u_p` on every edge.

## 2. Necessary fixed-saving condition

If `E_AP<=(1-delta)D`, then

$$
D-M\le(1-\delta)D,
$$

so `M/D>=delta`.

## 3. Edge-density toll

Suppose every row mass lies between `d_min` and `d_max=kappa*d_min`. With `P` vertices
and `E` matching edges,

$$
M\le2E d_{max},\qquad D\ge P d_{min},
$$

and therefore

$$
\frac MD\le2\kappa\frac EP.
$$

Thus `delta` saving requires `E/P>=delta/(2kappa)`.

## 4. Literal aligned rows

At `L=4`, the cutoff is one of `4,5,6,7`. Primitive multipliers are among
`+/-1,+/-3,+/-5,+/-7`; `+/-1` always survive. Hence every aligned row has between two
and eight equal-amplitude atoms, so `kappa<=4`. For `delta=1/400`, the density toll is
`E/P>=1/3200`.

## 5. Exact replay

At Q25, `P=6`, `E=1`, uniform matched mass is `1/3`, while literal aligned atom mass is
`10/26=5/13`. Over `Q=8..4096`, 2268 scales have edges and 1821 have none; maximum
literal fraction is `3/4` first at `Q=11`. These are finite certificate facts, not an
asymptotic density theorem.
