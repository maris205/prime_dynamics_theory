# TPC-356 computational protocol

- Candidate origins: `38001 + 211 j`, `0 <= j <= 50`.
- Pilot geometry: count `256`, `Q in {24,54,80}`, exponents `1,2`.
- Score: maximum unsigned `max(G)/min(G)` over the six pilot settings.
- Ranking: descending score, then ascending origin; greedy separation `1536`.
- Selected origins: `38423, 42010, 45597`.
- Replay counts: `256,512,1024`; shell anchors `24,54,80`; exponents `1,2`.
- Laws: `all_plus`, `alternating_index`, `mod4_character`, `half_split`.
- Source cutoff: `50000`; height: `66`; comparison cutoff: `2`.
- Producer accumulates shells forward; independent checker accumulates them in
  reverse order and implements the source/model independently.
- Numeric tolerance for reverse replay: `2e-5`; fixed power credit: `0`.
