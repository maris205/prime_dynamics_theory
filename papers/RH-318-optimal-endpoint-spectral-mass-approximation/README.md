# RH-318: Optimal endpoint spectral-mass approximation

Let `E_spec(M)` be the least endpoint `H2(rho_star)` mismatch over all finite
conjugate spectra in `|mu|<=q` with squared mass at most `M`.  Then

    E_spec(M)^2 ~ log(q_star/q)/log M.

The exact constants are

    d = log(q_star/q) = 0.3377217782684642...,
    sqrt(d) = 0.5811383469264992....

The lower bound uses the all-order target asymptotic and the mass cap.  The
upper bound uses the exact spectral prefixes of RH-316 and their sharp mass
clock from RH-317.

For the actual family, this yields only the universal lower-rate restriction
`liminf log(1/sigma)||g_sigma||^2 >= d`; it does not prove convergence or
nonconvergence.  Gates A--E remain false/open.
