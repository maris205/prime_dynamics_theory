# TPC-413 computational protocol

- Pool complete shells `Q=65536,131072`: counts `5709,10749`.
- Use heights `16,32,66,128`, `N=4H`, and CRT representatives `r+sL` for `s=1,2,3`.
- Keep source-shell labels in every amplitude and certificate row.
- Independent replay rebuilds the sieve, CRT, and all literal masks for 12 rows.
- Run producer, replay, stress, and Bridge-B in normal and `-O -B` modes.
