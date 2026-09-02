# TPC-346 derivation package

For panel p, let Y_p be the stacked twin-target row means and let N_p
be the matrix whose columns are the three nuisance-category means. The
shared three-panel model uses

```text
N_shared = [N_1; N_2; N_3].
```

The panel-adaptive model uses the block matrix

```text
N_adapt = diag(N_1,N_2,N_3).
```

The shared column space is contained in the adaptive block space: a common
coefficient vector (c_1,c_2,c_3) is represented by the block coefficient
(c,c,c). Therefore finite orthogonal projection gives

```text
||(I-P_adapt)Y||_2 <= ||(I-P_shared)Y||_2.
```

This is only a finite nested-model monotonicity statement. It does not say
that the additional panel-specific columns have a source-independent
arithmetic meaning.

For a training collection T and held-out panel p, the transfer diagnostic
fits N_T c to Y_T by least squares and measures

```text
||Y_p-N_p c||_2^2 / ||Y_p||_2^2.
```

It is a prediction residual, not an orthogonal projection identity. Equal-row
weighting divides each row target and nuisance column by the positive norm of
that row's twin target before stacking. The hostile fresh control-LOO
diagnostic uses the omitted control's twin output as target and the mean of the
other eight controls for each nuisance column.
