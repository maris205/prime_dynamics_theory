# Roadmap after RH-164

There are now two complementary rank certificates:

```text
sharp feedback:      a d b c < 1                    (RH-163)
balanced Neumann:    max(a,d) sqrt(b c) < 1         (RH-164)
```

The balanced form is convenient but carries a similarity-conditioning price
for graph bounds.  The next target is geometric: choose a contour that
minimizes the resolvent feedback.  For normal disk-separated blocks, the
midgap circle gives an exact closed-form threshold.
