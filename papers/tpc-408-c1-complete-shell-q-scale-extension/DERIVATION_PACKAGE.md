# TPC-408 derivation package

The TPC-407 local diagonal identity does not use even shell cardinality in
its energy calculation; evenness was only needed for the earlier notation
`2m`. For a full shell with `r` primes, retain every prime and define
`m_-=floor(r/2)` and `m_+=ceil(r/2)`. The CRT residues are still zero on
even indices and `-N` on odd indices. Because every shell prime exceeds `N`,
the masks in the window are exactly the same two classes as before.

The only changed proof line is the Cauchy--Schwarz parameter:
`P_-^2 <= m_- V_-` and `V_- >= m_- a_min^2`; cancellation of `m_-` gives
the same sharp bound. Thus odd complete shells are a genuine extension of
the finite proxy domain, while the full operator and arithmetic gates remain
untouched.
