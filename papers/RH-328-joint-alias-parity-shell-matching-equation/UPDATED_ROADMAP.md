# Roadmap after RH-328

RH-328 supplies the exact fixed-reference joint certificate

```text
e = L * (c_phys^(2k) - y) + E_obs + R,
y = c0^(2k) + (A-P-B)/L.
```

It also quantifies the conditioning of any same-order exchange
representation.  If `L` is comparable to the alias packet `A` and the
observation error plus far remainder is already `o(H_k)`, then power matching
must be accurate to `o((beta R)^(-2k))`, and the contrast radius must be
accurate to `o((beta R)^(-2k)/k)`.  A coarse interval fit or an `O(1/k)`
unit-edge approximation is nowhere near the required precision.

The sharp uncertainty ledger is

```text
m = L * (c_phys^(2k) - y),
|E_obs| <= U = sum_j W_j delta_j,
|R| <= V,
possible e in [m-U-V, m+U+V].
```

The best-case absolute residual is `max(|m|-U-V,0)`, while the worst case is
`|m|+U+V`.  Existence of a cancelling choice inside that interval is not a
statement about the actual physical errors.

RH-329 should perform a validated isolated-model audit with a fully fixed
data source.  It must report all of the following separately:

1. the model's actual boundary observation `B`;
2. its fixed deterministic reference and shell scale `L`;
3. its physical noisy contrast magnitude, without optimizing it after seeing
   the demand;
4. the required power `y` and actual power mismatch;
5. the observation Duhamel majorant with every prefix/suffix weight;
6. the far/omitted remainder bound;
7. the best-case and worst-case uncertainty residuals in units of
   `H_k = k R^(-2k)`;
8. whether the contrast-radius demand exhibits the predicted exponential
   precision barrier.

If the isolated model fails, RH-329 should publish that failure as a scoped
negative result.  Passing a finite isolated audit still would not identify
the physical noisy operator or prove the full-trace replacement.  RH-330
remains responsible for the actual full-trace transfer criterion retaining
joint cancellation.  Gates A--E remain false/open.
