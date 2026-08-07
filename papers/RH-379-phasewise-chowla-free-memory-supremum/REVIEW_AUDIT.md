# RH-379 adversarial peer-review audit

This is an internal ARS-style mathematical and reproducibility review, not a
claim of external journal peer review.

## Reviewer summary

| Metric | Value |
|---|---|
| Title | *Phasewise Chowla-Free Lag-Two Memory: Exact Max-Plus Optimization and the All-Clock Supremum* |
| Review rounds | 2 |
| Final verdict | **ACCEPT for the declared mathematical and executable scope** |
| Critical / major / minor findings after round 2 | `0 / 0 / 0` |
| Reviewer confidence | High |

## Five-dimension assessment

| Dimension | Weight | Score | Weighted score | Evidence |
|---|---:|---:|---:|---|
| Originality | 20% | 8/10 | 1.60 | New phasewise 192-table reduction, exact memory correction, and arbitrary-clock cofinal argument |
| Methodological rigor | 25% | 9/10 | Fixed order of limits, exact arithmetic, two independent optimizers, source locks, fail-closed comparisons |
| Evidence sufficiency | 25% | 9/10 | Every central finite claim is executable; imported asymptotic inputs are bounded by locked predecessors |
| Argument coherence | 15% | 9/10 | Census -> canonicalization -> DP -> square clocks -> cofinal supremum -> blocker |
| Writing quality | 15% | 8/10 | Precise theorem scope and explicit negative claims; generic repository style rather than venue-specific formatting |
| **Overall** | **100%** |  | **8.65/10** | ARS verdict band: Accept |

## Principal strengths

1. The paper does not infer `K -> I` compatibility before canonicalization.
   It first replaces every table by a payoff-dominating subset and only then
   uses the identical full canonical compatibility profiles.
2. The exact three-state max-plus computation is not a single opaque solver.
   It is cross-checked against the all-`J` baseline plus cyclic MWIS identity,
   including self-loop clocks `q=1,2`.
3. The arbitrary-clock upper bound does not assume a same-support memory
   saturation theorem.  It constructs a retained one-site independent set
   and separately charges discarded `J` mass to the prime-square tail.
4. The manuscript keeps the fixed-clock `N` limit before the cofinal `y`
   limit and supplies the reverse inequality by the explicit one-site
   embedding `f_r(x,z)=g_r(z)`.
5. The claim boundary is unusually explicit: no finite-clock attainment or
   nonattainment, no `Delta_y` monotonicity, no growing clock, and no
   operator/trace/zero/RH statement.

## Round-one findings and resolutions

| Severity | Finding | Resolution |
|---|---|---|
| Minor | The closed form for `M_(2m)` could be read at `m=0`, contradicting `M_0=0`. | Added `m>=1` for even indices and `m>=0` for odd indices. |
| Minor | `B_y` was used without a local definition. | Added `B_y=(4+2O_y/A_y)/pi^2` and `B_y -> B_infinity` from the locked inputs. |
| Minor | The cofinal finite count omitted the two padded initial sites. | Added an explicit `O(1)` term before division by `N`. |
| Minor | The MWIS formula stated the forward construction without its converse. | Added the zero-to-`J` converse for every zero not immediately preceding an `I`. |
| Major (artifact) | Cofinal result rows initially recorded protocol metadata but did not certify the finite decomposition. | Added exact aggregation, lifted-score equality, retained/discarded decomposition, independence, one-site weight/bound, charge-precondition checks, and included every row in global `all_pass`. |
| Major (artifact) | The result schema was only shallowly closed. | Replaced it with recursive row/object definitions; exact regeneration and exact source-membership tests remain the stronger byte-level contract. |
| Minor (artifact) | Reflection tested only each table against itself. | Exhausted all `512^2` ordered reflected neighbor pairs with zero failures. |
| Minor (artifact) | The square-clock global row did not include the computed `a/2 < b < a` flag in `all_pass`. | Added the flag to the conjunction and a regression assertion. |

## Cross-section checks

| Check | Result | Note |
|---|---|---|
| Title matches result | Pass | Names the phasewise class, exact optimizer, and supremum |
| Abstract matches theorems | Pass | Includes 512/192 census, `q=36`, square-clock correction, and all-clock endpoint |
| Imported input vs new proof | Pass | RH-374/375/376/378 roles are explicit |
| Tables traced to artifact | Pass | See `TABLE_TRACE.md` |
| Citation keys and bibliography | Pass | Six cited keys, six entries, no orphan |
| Limitations and declarations | Pass | First blocker and all negative claims are stated |
| Executable replay | Pass | 15 tests; exact result regeneration; recursive schema validation |

## Final reviewer finding

No theorem-critical defect remains.  In particular, the square-clock formula
is not extended to arbitrary same-support multiples, and the cofinal theorem
uses RH-375 saturation only after reducing to a retained one-site set.  Final
acceptance here is limited to the manuscript's stated phasewise `c11=0`,
fixed-finite-clock class.
