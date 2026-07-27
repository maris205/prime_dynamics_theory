# Roadmap after RH-185

A local length-four biorthogonal candidate survives, but the cross angle is
small. The next layer must insert the exact oblique factor into every
perturbation and Riesz budget:

```text
raw residual success
  + cross-angle conditioning
  -> conditioned packet gate
```

If the coarse gate fails, test regularization and the sharper product-form
Schur certificate before rejecting the branch.
