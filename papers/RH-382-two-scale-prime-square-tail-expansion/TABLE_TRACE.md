# RH-382 formula-to-artifact trace

| Manuscript object | Artifact function/result key | Exact check |
|---|---|---|
| `R_ell`, terminal `R8` | `square_run_counts`, `terminal_ledger` | Second differences only through 7; `R8=P E8` |
| `E9=0`, no `E10` | `finite_euler_values`, `terminal_ledger` | Four exact rows and explicit false construction flag |
| Bonferroni loss | `bonferroni_product` | Four finite tails |
| Euler inverse-product lemma | `product_expansion_row` | 24 rows, `m=3..8` |
| `931/4` | `coefficient_ledger.x_quadratic_total` | Exact five-term sum |
| `63` | `coefficient_ledger.memory_lipschitz_total` | Exact six-term sum |
| `T^2+S`, `T^2-S` | `exact_tail_algebra` | Four exact tails |
| Cube telescope | `exact_tail_algebra.cross_cube` | Exact `(T^3-C)/3` identity |
| `931/2` | `coefficient_ledger.x_channel` | Exact fraction |
| `254/3` | `coefficient_ledger.memory_channel` | Exact `84+2/3` |
| `3301/6<551` | `coefficient_ledger.total/strict_margin` | Margin `5/6` |
| Two-scale finite replay | `finite_gap_rows` | Four reproduction-only endpoint rows |
| `p=71` memory sign | `one_tail_sign_mutation` | Correct `<1`, wrong `>1`, difference `4mS` |
| 33 immutable inputs | `source_locks` | Live hashes plus release blobs |
| Gate boundary | `claim_boundary`, `gates` | Five false Gate values |

The artifact trace is a reproduction map. The all-`y` proof remains the
symbolic product/telescope argument in `main.tex`.
