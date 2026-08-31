# TPC-321 theorem ledger

| ID | Statement | Status | Evidence |
|---|---|---|---|
| T321.1 | (G_{X,Q,s}) is PSD | PROVED_STRUCTURAL | Gram definition |
| T321.2 | (p_j=\lambda_j/\operatorname{tr}G) is invariant under (G\mapsto cG), (c>0) | PROVED | `DERIVATION_PACKAGE.md` |
| T321.3 | Every declared adjacent-Q pair has (D_{TV}>0.03) on the finite panel | NUMERICALLY_CERTIFIED | certificate + dual paths |
| T321.4 | Every declared adjacent-Q pair has (D_L>0.02) on the finite panel | NUMERICALLY_CERTIFIED | certificate + independent replay |
| T321.5 | Majorization pattern is 3 forward / 2 reverse / 13 mixed | NUMERICAL_OBSERVATION | sign-tolerance classification |
| T321.6 | A uniform shell-profile law holds | REFUTED_FINITE_PANEL | finite separation audit |
| T321.7 | Arithmetic cancellation or power saving follows | OPEN | no signed reassembly |
| T321.8 | Twin primes follow | NONE | Gate B remains open |

## Strongest positive result

The scale-invariant ordered spectral profile is not shell-stable on all 18
declared adjacent transitions; the minimum TV and cumulative-profile gaps are
strictly separated from zero by comfortable finite margins.

## Strongest obstruction

The profile changes are not governed by one order: forward, reverse, and mixed
majorization patterns coexist.  This blocks a simple shell-monotone spectral
principle even before arithmetic reassembly.

## Open theorem

Find a uniform bound or limiting law for the cross-shell profile distances,
with hypotheses strong enough to survive signed prime-shell reassembly.

## Reusable structure

    literal blocks -> PSD Gram -> trace-normalized ordered profile
                     -> cross-shell distances -> majorization firewall

## ROUND2_CLUE

TEST_SIGNED_PROJECTOR_REASSEMBLY_OR_PROVE_A_UNIFORM_SHELL_PROFILE_BOUND_BEFORE_ANY_ARITHMETIC_POWER_CLAIM
