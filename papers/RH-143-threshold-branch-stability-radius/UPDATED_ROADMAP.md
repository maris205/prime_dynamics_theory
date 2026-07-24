# Roadmap after RH-143

The threshold branch is no longer a qualitative discontinuity: every strict
decision has a sharp stability radius.  The finite archive is comfortably
stable against local floating error, but the minimum primary radius is only
`4.34e-9`.  A full interval update must therefore exploit correlated
snapshot/projector errors; the generic coarse RH-142 projector ball is too
broad to insert directly.

The next block returns to the RH-139 controlled-viability frontier, where
block/reset and delayed-start policies can be proved without requiring every
finite branch to be uniformly tight.

