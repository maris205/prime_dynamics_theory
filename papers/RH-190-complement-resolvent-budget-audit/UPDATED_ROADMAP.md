# Roadmap after RH-190

The universal radial norm route is closed on the current windows.  The next
wall is the actual physical complement inverse, to be treated by validated
contour numerics:

1. serialize physical oblique block data, not only summary residuals;
2. compute nominal inverses of `zI-D` on fixed contour meshes;
3. validate inverse defects and outward operator uncertainty;
4. cover each continuous contour by a Lipschitz/mesh estimate;
5. insert the resulting complement factor into the exact directed Schur
   product;
6. only after a positive margin, infer a finite Riesz rank.

The radial audit already uses the sharper one-factor bound `chi ||A||`, not
the looser ambient `chi^2 ||A||` estimate.  Its failure therefore does not
come from an avoidable second oblique factor.

The local `sigma=0.01, L=4` packet remains merely a floating candidate until
this `D` leaf is closed.
