# RH-289: Finite-moment shell nonidentifiability

For any prefix length `N`, choose `L>N` and add the complete root-of-unity
shell

```text
S_(L,gamma) = {gamma exp(2 pi i j/L) : 0<=j<L}.
```

Its power sums vanish for every order `1<=n<=N`, while the first hidden
moment is

```text
sum_(z in S) z^L = L gamma^L.
```

Its genus-one factor is exactly

```text
prod_(z in S) (1-w z) exp(w z) = 1-(gamma w)^L.
```

Therefore two spectral multisets can have identical arbitrarily long finite
moment prefixes and different divisors immediately beyond the prefix.  The
construction is conjugation symmetric and can be appended to any existing
head.

This is a scoped negative theorem: finite or merely growing unweighted
prefix agreement cannot identify the noisy cloud or activate the RH-288
gluing criterion without a weighted tail/root-localization estimate.
