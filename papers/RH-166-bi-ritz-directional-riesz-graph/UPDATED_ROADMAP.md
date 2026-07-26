# Roadmap after RH-166

The finite data contract for a realized packet is now explicit:

```text
frame V + compressed blocks + right residual c + left residual b
       + continuous contour resolvent bounds a,d
       -> rank and directional graph certificates.
```

The unresolved word is “continuous”.  The next paper should prove how a
finite contour mesh and exact sample inverse bounds cover the entire curve,
with a yes/no sampling-density condition.
