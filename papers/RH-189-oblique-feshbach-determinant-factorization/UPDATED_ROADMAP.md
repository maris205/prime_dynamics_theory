# Roadmap after RH-189

The local packet now has an exact Feshbach object.  The next proof leaf is
the physical complement resolvent:

1. freeze the physical `V,W,K,B,C,D` data for each predeclared window;
2. choose disjoint contours from the length-four root geometry;
3. test the cheapest universal norm-only inverse bound;
4. if that fails, move to nominal contour inverses, mesh covering, and
   outward operator balls;
5. combine the validated inverse with the directed coupling product and
   compute both packet and complement Riesz counts;
6. infer the packet count for the full operator only after validating that
   the complement count inside the root contour is zero.

RH-190 should settle step 3 without interpreting its failure as a spectral
no-go.
