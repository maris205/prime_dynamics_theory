# TPC-346 computational protocol

The producer locks TPC-340 as the source/operator parent and TPC-345 as the
immediate geometry parent. It adds origins 44097, 44609, and 45217, each with
512 source values and hi+2<50000. The all-plus Q=54, exponent-one, H=66
operator and nine controls are unchanged.

For each weighting, the audit computes each panel's own projection, the
shared and block-adaptive three-panel projections, all three pairwise
subspace transfers, six directed single-panel predictions, three
leave-one-panel-out predictions, and nine omitted-control projections on the
fresh panel. Raw records are retained for all 324 control/category pairs.

The reverse-shell checker uses TPC-340's separately hash-locked independent
engine and does not import the producer. The stress suite reseals ten
mutations and requires every one to be rejected.
