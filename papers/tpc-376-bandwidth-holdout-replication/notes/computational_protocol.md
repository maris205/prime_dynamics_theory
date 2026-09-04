# TPC-376 computational protocol

The candidate grid is 1010001 + 401*j, j=0,...,40.  Training indices
0,20,40 were already fixed by TPC-370; this experiment freezes the
reserved indices 5,15,30, giving origins 1012006,1016016,1022031.

The complete 3-by-3 panel is evaluated with count 2048, eight blocks of
length 256, Q=512,2048,8192, exponent 1, beta 2, all-plus signs,
height 66, and the full-window square-energy normalization.  The band
keeps block distances at most one.  Full modes are selected by largest
absolute eigenvalue, with the minimum mode winning ties.

The producer uses the locked TPC-375 engine.  The independent checker
rebuilds the prime shell in descending order and does not import the
producer.  Both normal and optimized Python modes are required to emit
empty stderr and byte-identical output.
