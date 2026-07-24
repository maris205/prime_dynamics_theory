# RH-144: Backward Block-Controlled Viability

For a Young envelope

`F(y) = q + (sqrt(A y) + sqrt(B))^2`,

this paper gives the closed-form largest input radius mapped below a target
radius.  Taking the maximum over controls and iterating backward computes the
exact scalar finite-horizon viability kernel.  Repeating blocks are viable
whenever their backward kernel contains the chosen reset interval.

Applied to the full RH-137 candidate families, 28 of 30 chains admit the
entire initial interval `[0,1)`.  The two coarse left failures have empty
kernels: every candidate control has an unavoidable floor above the safety
wall.  They are therefore not greedy-choice artifacts.  No all-level
repeating-block hypothesis is proved.

