TPC_AGENT_RESULT_V1

task_id: `recon418-regression`  
role: `tpc_release_qa`  
verdict: `PROPOSE_FOR_AUDIT` — bounded QA findings, not a research candidate  
reproducibility: `PASS_CURRENT_STARTUP_SUITE`  
claim_integrity: `QUALIFIED_FINITE_SYNTHETIC_ONLY`  
candidates: `[]`  
files_changed: `[]`

The current eight-command regression is reproducible on the locked baseline. The finite parity/operator argument survives inspection under integer shell scales, integer heights, and the inherited synthetic CRT masks. However, the checks do not establish fresh independent recomputation of the large four-shell aggregates, comprehensive mutation rejection, or PDF semantic validity.

### Execution and preservation

After reading all four invoked Python sources, I confirmed standard-library-only imports and read-only check paths. The producer writes only through the mutually exclusive `--write` branch; the stress checker mutates memory; the wrapper reads/hashes artifacts and invokes check subprocesses. See [producer:296](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/code/tpc418_c1_shell_parity_envelope.py:296) and [wrapper:13](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/tpc_bridge_b_tpc418_c1_shell_parity_envelope_checker.py:13).

Actual top-level commands, both exit **0**, Python **3.12.3**:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_tpc418_c1_shell_parity_envelope_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B research/tpc-big-road/tpc_bridge_b_tpc418_c1_shell_parity_envelope_checker.py --check
```

Each wrapper executes all six child commands at [TPC_HANDOFF.md:896](/root/autodl-tmp/math_research3/prime_dynamics_theory/TPC_HANDOFF.md:896): producer, independent, and stress, each with `-B` and `-O -B`, always `--check`. Thus all eight required command/mode forms were covered, with **12 child executions**, not eight separately issued top-level commands. Wrapper success requires every child exit 0, empty stderr, and identical normal/optimized stdout.

Both returned:

```text
TPC418_BRIDGE_CHECK=PASS fixtures=3 sigma=PASS independent=PASS stress=PASS paper_artifacts=PASS strict_firewall=PASS
```

The stress suite comprises nine certificate mutations and two parser rejections. No required checker failed; no artifacts were regenerated.

### Mathematical audit and bounded findings

**1. Corrected parity envelope is supported.** For increasing amplitudes, an even block has negative alternating sum bounded by endpoint variation; an odd block has positive sum bounded by its final amplitude. Consequently the actual sign is
\(\sigma_j=\epsilon_j(-1)^{n_j+1}\), and
\[
|A|\le B_*<3E+4\lceil O/2\rceil\le3K+1.
\]
Odd blocks alternate actual sign; intervening even blocks do not flip the next start sign. This validates the counting argument in [PROOF_PACKAGE.md:83](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/PROOF_PACKAGE.md:83).

An exact in-memory rational calculation confirmed the mixed-parity fixture:
\[
A=\frac{1507}{270},\quad
B_{\text{old}}=\frac{125}{36},\quad
A-B_{\text{old}}=\frac{1139}{540}>0,\quad
B_{\text{corrected}}=\frac{1507}{270}.
\]
The standalone [counterexample JSON:1](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/results/tpc418_counterexample.json:1) records the **old** grouping; its `B_star` must not be mistaken for the corrected envelope.

**2. Finite operator estimate is supported, with a domain-wording defect.** From the stated masks,
\[
D_r\ge V_-H/4,\qquad
\|q\|_2^2\le\frac{4P_-^2}{V_-^2H}\le\frac4{a_{\min}^2H}.
\]
The two-sided kernel sum is at most \(4H\), giving
\(\|C\|_2\le16|A|/V_-\). Triangle inequality yields the advertised bound. The inherited argument is explicit in [TPC417 proof:43](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-417-c1-four-shell-finite-operator-bound/PROOF_PACKAGE.md:43).

TPC418 [proof:122](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/PROOF_PACKAGE.md:122) unnecessarily writes \(N<Q_j<p\). Its mixed fixture has \(N=4>Q_1=3\); its small fixture includes \(N=Q_1=16\). The sufficient inequality is \(|r-s|<N<p\), which holds. This does not invalidate the bound.

Integer \(Q_j\) is essential, although omitted from the headline claim and specified only in [proof:69](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/PROOF_PACKAGE.md:69) and code. A real-scale extension fails: \(Q=(5/2,5)\), shells \(\{5\},\{7\}\), \(H=1\) satisfy the displayed interval and prime constraints, but the first amplitude is \(5\), and \(B_*=5\not<4\). This is a scoped elimination of that extension, not of the integer theorem.

**3. Strongest reproducibility objection: shared inherited evidence.** Both implementations import TPC417 certificate data for the four-shell fixture. They regenerate shell/parity information but reuse large aggregate and matrix rows instead of independently recomputing them. See [producer:211](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/code/tpc418_c1_shell_parity_envelope.py:211), [independent:49](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/experiments/tpc418_independent_checker.py:49), and [independent:74](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/experiments/tpc418_independent_checker.py:74). No TPC417 producer/checker was executed this round. The README’s small-fixture independence language is defensible; an end-to-end independent-recomputation interpretation is not.

**4. Stress and PDF claims require narrower wording.** The [computational protocol:9](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/notes/computational_protocol.md:9) advertises height mutation coverage, but the [actual mutation list:36](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/experiments/tpc418_adversarial_certificate_stress.py:36) contains none. Additional in-memory probes, with recomputed payload digests, found that its standalone `validate` accepts:

- `sigma_j=True` in place of `1`;
- a changed fixture height;
- `PHYSICAL_H0="PROVED"`.

These are **standalone stress-validator limitations**, not demonstrated escapes through the complete hash-locked suite. The probe command was `PYTHONDONTWRITEBYTECODE=1 python -B -` with an inline `Fraction`/`runpy`/deep-copy audit; exit **0**.

The wrapper’s `paper_artifacts=PASS` means presence and SHA-256 identity, not compilation, rendering, or semantic inspection. Its file list makes PDFs mandatory, despite the [README:31](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/README.md:31) wording “when they are available.”

### Seven-field contract

1. **Signs/weights/masks:** model index \(i\) is zero-based, sign \((-1)^i\), amplitude \(p_i^3/[Q_i^2(p_i-1)]\), kernel \(T_d=H^2/(H^2+d^2)\), exact diagonal deletion. CRT assigns even-index primes to divide \(o\), odd-index primes to divide \(o+N\); unit masks determine the displayed \(M,D\). [TPC417 main.tex:20](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-417-c1-four-shell-finite-operator-bound/paper/main.tex:20)
2. **Physical \(h_0\):** absent. \(H\) is model height, not physical fixed \(h_0=2\).
3. **Domain/order:** complete shells, \(2Q_j\le Q_{j+1}\), increasing primes within shells, global concatenation; window \(r=0,\ldots,N-1\). No physical cumulative-prefix transfer.
4. **Ranges:** integers \(Q_j\ge2,H\ge1\), \(N=4H\), finite \(K\ge1\), nonempty shells, \(L\ge2\), every selected prime \(>N\). Fixtures: four-shell \(H=16,32,66,128\); small \(H=1,2,4\); mixed \(H=1\). Physical \(X\)/conductor ranges missing.
5. **Uniformity/exceptions:** deterministic finite inequality with explicit constants; no exceptional-set theorem, designated arithmetic seed, or common growing physical regime established.
6. **Normalization:** exact local \(Z=D^{-1/2}MD^{-1/2}\); \(V_-=\sum_{\text{odd}}\alpha_i^2\), \(m_-=\lfloor L/2\rfloor\). Not physical natural normalization.
7. **Loss ledger:** finite bound \(2/(a_{\min}\sqrt H)+16B_*/V_-\); physical losses unpaid, strict \(1/400\) unestablished, fixed-power credit zero.

This is island **②**, a synthetic operator subproblem relevant to image Bridge A—not closure of either mathematical bridge. Closest existing result: **TPC417**; no renamed route proposed. Growing/physical exclusions remain explicit in [TPC418 proof:145](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/PROOF_PACKAGE.md:145). No conjectural improvement is asserted.

### Baseline and handoff

Start/end `HEAD=origin/main=ab23455ba941e5a14ded27d49de0e874aee811ac`. Control SHA-256 values were identical at both endpoints:

```text
AGENTS.md                 6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md            9b5229094d55c20d6fdf5079a9ba91e4a0561fcf5505db23eb590db1090f3007
TPC_ROUTE_MAP.md          3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
```

Twenty relevant artifact/dependency hashes also remained identical. `git --no-optional-locks status --porcelain=v1 -uall` was byte-identical: the supplied ten tracked modifications, 615 untracked files, empty index. `git rev-parse`, `git diff --cached --name-only`, `git --no-optional-locks diff --name-only`, and all `sha256sum` checks exited **0**.

Files read were the required controls/guide, cited TPC418/TPC417 originals, four check sources, and check dependencies; other release artifacts were hashed only. External primary URLs: none; no browsing. ARS guidance kept reproduction evidence separate from mathematical conclusions.

Narrowest next action: parent audit of the inherited-replay and coverage wording. No repair, research reopening, mathematical GO, or publication is authorized by this result.
