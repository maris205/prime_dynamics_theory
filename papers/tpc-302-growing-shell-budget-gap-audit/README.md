# TPC-302 - Growing-shell native budget-gap audit

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-302 carries the TPC-301 tolerance/common-prefix/source-normalization
attack to the complete 34-row TPC-288 growing/control grid.  The weighted
target is compiled source-first from the exact physical Gram matrix on every
row, rather than copied from the earlier 18-row atlas.  There are 430 explicit
shell targets (the inherited parent metadata separately records 1,380 edges).
The common-prefix weighted/positive budget gap is above 10 in all 34 rows at
each of tau=1/4, 1/2, and 3/4; the minima are 85.3203517096, 38.2186652435,
and 39.2637006403.  The common weighted budget is above 1e-5 in all 102
row--tolerance cases under each of three source normalizations.

## What is new

TPC-301 established robustness on 18 inherited rows but left the growing-shell
extension open.  TPC-302 adds 16 growing-path rows and 18 declared source
controls, and recomputes the signed minimizer by exhaustive equal-sign
enumeration of the physical Gram matrix on all 34 rows.  Thus the target
class and the source-budget test are aligned on the same physical shell.

The finite theorem layer proves the Gram PSD identity, global-sign reduction,
Gray-code exhaustiveness, tolerance/prefix monotonicity, and common-prefix
normalization cancellation.  The numerical result is deliberately scoped to
the declared finite grid; it is not a uniform growing-shell theorem and gives
no arithmetic L2 credit.

## Claim firewall

    PROVED_EXACT_FINITE = physical Gram PSD identity, global-sign reduction,
    exhaustive finite sign enumeration, tolerance/prefix monotonicity,
    common-prefix normalization invariance
    NUMERICALLY_CERTIFIED_FINITE = 34 source-first labels; 612 frontier cases;
    34/34 weighted ratios below one; 34/34 positive ratios above one;
    common and full gaps above 10 at all three tolerances; 102/102 budget
    floors above 1e-5 for each of three normalizations
    NUMERICAL_OBSERVATION = displayed gap and budget minima
    MODELING_CHOICE = TPC-288 grid, 17 literal cutoffs, three tolerances,
    equal-sign targets, common-prefix protocol, and source normalizers
    OPEN = uniform growing profile-budget theorem, arithmetic L2, fixed-power
    credit, full Gate B, and the twin-prime conjecture

## Research extraction

    STRONGEST_POSITIVE_RESULT = source-first growing-grid gap stability:
    34/34 rows and 3/3 tolerances retain a common gap above 10.
    STRONGEST_OBSTRUCTION = finite stability does not control the profile
    budget as the shell or cutoff grows; no asymptotic bridge is paid.
    OPEN_THEOREM = prove or refute a uniform native profile-budget lower bound
    for the literal source family on growing prime shells.
    REUSABLE_STRUCTURE = exact physical Gram -> exhaustive sign target ->
    literal profile image -> constrained native budget frontier.
    ROUND2_CLUE = TEST_UNIFORM_NATIVE_BUDGET_GROWTH_OR_CONSTRUCT_A_GROWING_SHELL_COUNTEREXAMPLE

## Reproduction

    export PYTHONDONTWRITEBYTECODE=1
    python -B code/tpc302_growing_shell_budget_gap_audit.py --write
    python -B code/tpc302_growing_shell_budget_gap_audit.py --check
    python -B experiments/tpc302_independent_checker.py
    python -B experiments/tpc302_stress.py
    python -B research/tpc-big-road/tpc_bridge_b_tpc302_growing_shell_budget_gap_audit_checker.py --check

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
Route-A/Route-B evaluator files are absent from this checkout; the local
proof package, independent source-first replay, stress suite, PDF audit, and
Bridge-B checker are the available fail-closed validation path.  No official
Route-A or Route-B pass is asserted.
