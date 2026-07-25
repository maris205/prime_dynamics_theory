#!/usr/bin/env python3
"""Exact provenance regression for TPC-100.

The checks model the literal order

    beta=(theta,c,kappa) -> opened atoms (beta,z) -> source inverse
    -> fine cells obtained by deleting only j.

They are finite algebraic checks, not an asymptotic dispersion or
Mobius-correlation experiment.
"""

from collections import defaultdict
from fractions import Fraction
from math import gcd


PRIMES = (11, 13, 17, 19, 23, 29, 31)


def inv(a, q):
    return pow(a % q, -1, q)


def hq(q, n):
    return min((q - 1) // 2, q // n)


counts = defaultdict(int)


# Branch-level integer provenance.  The full quotient is integral, while the
# would-be coefficient ell*v*B/c need not be.
false_quotient_witnesses = []
for q in PRIMES:
    for ell in range(1, min(5, q)):
        for v in range(1, min(5, q)):
            for c in range(1, min(6, q)):
                for kappa in range(1, min(5, (q - 1) // c + 1)):
                    b = c * kappa
                    if b >= q:
                        continue
                    for sigma in range(1, 2 * q + 1):
                        g = gcd(b, sigma)
                        B = b // g
                        Omega = ell * v * sigma * B
                        assert Omega % c == 0
                        assert Omega // c == kappa * ell * v * (sigma // g)
                        counts["integer_provenance"] += 1
                        if (ell * v * B) % c:
                            false_quotient_witnesses.append(
                                (q, ell, v, c, kappa, sigma, g, B)
                            )
                            counts["false_integer_quotient"] += 1

assert false_quotient_witnesses


# q|u is a predicate on an actual opened source value.  For each actual
# moving row, a no-wrap interval contains at most one corresponding j.
for q in PRIMES:
    for m in range(1, q):
        for h in (-3, -2, -1, 1, 2, 3):
            for start in (-q, -2, 0, 3, q // 2):
                for length in sorted({0, 1, min(3, q - 1), q - 1}):
                    J = range(start, start + length + 1)
                    hits = [j for j in J if (m * j + h) % q == 0]
                    assert len(hits) <= 1
                    counts["opened_q_u_uniqueness"] += 1


# Build literal-style resolved branches.  theta fixes j and sigma.  The
# actual source values U(t) and M(t) vary with z.
branches = []
atoms = []
branch_id = 0
for q in PRIMES:
    for ell in (1, 2):
        for v in (1, 2):
            for j in (1, 2, 3, 4):
                for sigma in (1, 2, 3, 4):
                    for h in (1, 2):
                        a = ell * j * v
                        if gcd(a, sigma) != 1 or gcd(a * sigma, h) != 1:
                            continue
                        for d0 in (1, 2, 3, 4):
                            numerator = h + a * d0
                            if numerator % sigma:
                                continue
                            u0 = numerator // sigma
                            if u0 <= 0:
                                continue
                            assert sigma * u0 - a * d0 == h
                            for c in (1, 2, 3):
                                for kappa in (1, 2, 3):
                                    b = c * kappa
                                    if b >= q or gcd(b, j * h) != 1:
                                        continue
                                    g = gcd(b, sigma)
                                    B = b // g
                                    if gcd(a, B) != 1:
                                        continue
                                    tau = next(
                                        (
                                            t
                                            for t in range(B)
                                            if (u0 + a * t) % B == 0
                                        ),
                                        None,
                                    )
                                    if tau is None:
                                        continue
                                    opposite_rows = [
                                        n
                                        for n in range(1, (q - 1) // 2 + 1)
                                        if (n * j + h) % b == 0
                                    ]
                                    if not opposite_rows:
                                        continue
                                    n_opp = opposite_rows[0]
                                    for N in (1, 2, 3):
                                        zs = tuple(range(N))
                                        source_values = []
                                        valid = True
                                        for z in zs:
                                            t = tau + B * z
                                            D = d0 + sigma * t
                                            U = u0 + a * t
                                            m = ell * v * D
                                            if (
                                                D <= 0
                                                or U <= 0
                                                or 2 * m >= q
                                                or 2 * abs(m - n_opp) >= q
                                            ):
                                                valid = False
                                                break
                                            assert m * j + h == sigma * U
                                            assert (sigma * U) % b == 0
                                            source_values.append((z, t, D, U, m))
                                        if not valid:
                                            continue

                                        Omega = ell * v * sigma * B
                                        assert Omega % c == 0
                                        assert Omega % q != 0
                                        eps = (
                                            -1
                                            if (
                                                ell + v + j + sigma
                                                + c + kappa + N
                                            ) % 2
                                            else 1
                                        )
                                        omega = (eps * (Omega // c)) % q
                                        H = hq(q, N)
                                        beta = {
                                            "id": branch_id,
                                            "q": q,
                                            "ell": ell,
                                            "v": v,
                                            "j": j,
                                            "sigma": sigma,
                                            "h": h,
                                            "a": a,
                                            "d0": d0,
                                            "u0": u0,
                                            "c": c,
                                            "kappa": kappa,
                                            "b": b,
                                            "g": g,
                                            "B": B,
                                            "tau": tau,
                                            "n_opp": n_opp,
                                            "N": N,
                                            "H": H,
                                            "omega": omega,
                                            "eps": eps,
                                            "atom_ids": [],
                                        }
                                        branch_weight = 0
                                        for z, t, D, U, m in source_values:
                                            weight = 1 + (
                                                branch_id + 2 * z + c + kappa
                                            ) % 5
                                            atom = {
                                                "id": len(atoms),
                                                "beta_id": branch_id,
                                                "q": q,
                                                "ell": ell,
                                                "v": v,
                                                "j": j,
                                                "sigma": sigma,
                                                "h": h,
                                                "a": a,
                                                "d0": d0,
                                                "u0": u0,
                                                "c": c,
                                                "kappa": kappa,
                                                "b": b,
                                                "g": g,
                                                "B": B,
                                                "tau": tau,
                                                "n_opp": n_opp,
                                                "N": N,
                                                "H": H,
                                                "omega": omega,
                                                "eps": eps,
                                                "z": z,
                                                "t": t,
                                                "D": D,
                                                "u": U,
                                                "m": m,
                                                "weight": weight,
                                            }
                                            atoms.append(atom)
                                            beta["atom_ids"].append(atom["id"])
                                            branch_weight += weight
                                            counts["opened_source_identities"] += 1
                                        beta["weight"] = branch_weight
                                        assert branch_weight == sum(
                                            atoms[i]["weight"]
                                            for i in beta["atom_ids"]
                                        )
                                        counts["branch_atom_mass_equalities"] += 1
                                        branches.append(beta)
                                        branch_id += 1

assert branches and atoms
assert {beta["eps"] for beta in branches} == {-1, 1}
counts["both_polarizations_present"] += 1


# Exact branch census equals the opened-atom census, with H inherited from
# N_beta rather than from any cell occupancy.
branch_census = defaultdict(int)
atom_census = defaultdict(int)
for beta in branches:
    branch_census[(beta["q"], beta["H"], beta["omega"])] += beta["weight"]
    assert beta["H"] == hq(beta["q"], beta["N"])
    counts["inherited_width_checks"] += 1
for atom in atoms:
    atom_census[(atom["q"], atom["H"], atom["omega"])] += atom["weight"]
assert branch_census == atom_census
counts["global_census_reassembly"] += len(branch_census)


# The flattened provenance record deletes the native j coordinate and its
# direct stored copy a=ell*j*v.  It retains z, the independent physical source
# data, sigma, content and width, but contains no opaque beta id or
# weight-derived id.  The retained source identity itself determines j, so the
# resulting maximally literal cells must be singletons.  This is an audit
# conclusion, not a dispersion gain.
def deletion_key(p):
    return (
        p["q"],
        p["ell"],
        p["v"],
        p["sigma"],
        p["h"],
        p["d0"],
        p["u0"],
        p["c"],
        p["kappa"],
        p["b"],
        p["g"],
        p["B"],
        p["tau"],
        p["n_opp"],
        p["N"],
        p["H"],
        p["eps"],
        p["z"],
        p["t"],
        p["D"],
        p["u"],
        p["m"],
    )


cells = defaultdict(list)
reconstruction = {}
for atom in atoms:
    key = deletion_key(atom)
    pair = (key, atom["j"])
    assert pair not in reconstruction
    reconstruction[pair] = (atom["beta_id"], atom["z"], atom["id"])
    cells[key].append(atom)
    counts["lossless_atom_reconstructions"] += 1

for key, members in cells.items():
    js = [p["j"] for p in members]
    assert len(js) == len(set(js))
    assert len(members) == 1
    p0 = members[0]
    assert (p0["sigma"] * p0["u"] - p0["h"]) % p0["m"] == 0
    assert (
        (p0["sigma"] * p0["u"] - p0["h"]) // p0["m"]
        == p0["j"]
    )
    fixed_fields = ("m", "u", "ell", "v", "c", "B", "eps", "H")
    for field in fixed_fields:
        assert len({p[field] for p in members}) == 1
    counts["fine_cell_consistency"] += 1
    counts["forced_singleton_cells"] += 1


# Atomwise finite-field linearization and fine-cell injectivity.
invertible_cells = {}
for key, members in cells.items():
    inv_members = [p for p in members if p["u"] % p["q"] != 0]
    if not inv_members:
        continue
    assert len(inv_members) == len(members)
    q = members[0]["q"]
    first = members[0]
    A = (
        first["eps"]
        * first["ell"]
        * first["v"]
        * first["B"]
        * inv(first["c"] * first["u"], q)
    ) % q
    A2 = (
        first["eps"]
        * first["kappa"]
        * first["ell"]
        * first["v"]
        * inv(first["u"] * first["g"], q)
    ) % q
    assert A != 0 and A == A2
    seen = {}
    for p in members:
        affine = A * (p["m"] * p["j"] + p["h"]) % q
        assert affine == p["omega"]
        assert p["omega"] != 0
        assert p["j"] not in seen
        seen[p["j"]] = p["omega"]
        counts["atomwise_linearizations"] += 1
    assert len(seen.values()) == len(set(seen.values()))
    counts["fine_cell_injectivity"] += 1
    invertible_cells[key] = members


# Same-beta different-z atoms keep the same omega and, because z and actual
# source values are retained, occur in different fine cells.
atom_cell = {
    p["id"]: deletion_key(p)
    for p in atoms
}
for beta in branches:
    ids = beta["atom_ids"]
    for i, aid in enumerate(ids):
        for bid in ids[i + 1:]:
            a_atom = atoms[aid]
            b_atom = atoms[bid]
            assert a_atom["omega"] == b_atom["omega"]
            assert atom_cell[aid] != atom_cell[bid]
            counts["forced_same_beta_cross_collisions"] += 1


# Exact resonance preimages use H_beta, never the number of atoms in a cell.
for key, members in invertible_cells.items():
    p0 = members[0]
    q = p0["q"]
    A = (
        p0["eps"]
        * p0["ell"]
        * p0["v"]
        * p0["B"]
        * inv(p0["c"] * p0["u"], q)
    ) % q
    H = p0["H"]
    assert H == hq(q, p0["N"])
    if H != hq(q, len(members)):
        counts["width_not_cell_occupancy_witnesses"] += 1
    EH = {
        x % q for x in range(1, H + 1)
    } | {
        (-x) % q for x in range(1, H + 1)
    }
    for r in sorted({1, 2, q - 1}):
        direct = [
            p["j"]
            for p in members
            if r * p["omega"] % q in EH
        ]
        residues = {
            inv(p0["m"], q) * (inv(r * A, q) * s - p0["h"]) % q
            for s in EH
        }
        formula = [p["j"] for p in members if p["j"] % q in residues]
        assert direct == formula
        counts["inherited_resonance_preimages"] += 1


# Sample exact cross-cell collision congruences.  This includes forced
# same-beta collisions when the two corresponding cells enter the sample.
cells_by_qh = defaultdict(list)
for key, members in invertible_cells.items():
    p = members[0]
    cells_by_qh[(p["q"], p["H"], p["h"])].append(members)

for (q, H, fixed_h), group in cells_by_qh.items():
    sample = group[: min(28, len(group))]
    for i, C in enumerate(sample):
        pc = C[0]
        AC = (
            pc["eps"] * pc["ell"] * pc["v"] * pc["B"]
            * inv(pc["c"] * pc["u"], q)
        ) % q
        for D in sample[i + 1:]:
            pd = D[0]
            AD = (
                pd["eps"] * pd["ell"] * pd["v"] * pd["B"]
                * inv(pd["c"] * pd["u"], q)
            ) % q
            direct_count = 0
            for p in C:
                partners = 0
                for s in D:
                    lhs = p["omega"] == s["omega"]
                    rhs = (
                        AC * pc["m"] * p["j"]
                        - AD * pd["m"] * s["j"]
                        - pc["h"] * (AD - AC)
                    ) % q == 0
                    assert pc["h"] == pd["h"] == fixed_h
                    assert lhs == rhs
                    partners += int(lhs)
                    direct_count += int(lhs)
                    counts["cross_cell_congruences"] += 1
                assert partners <= 1
            assert direct_count <= min(len(C), len(D))
            counts["cross_cell_count_bounds"] += 1


# Exact uncentered and centered energy from opened weights.  The atom census
# must agree with direct branch re-summation before the energy is compared.
for (q, H, fixed_h), group in cells_by_qh.items():
    sample = group[: min(35, len(group))]
    census = defaultdict(int)
    masses = []
    diagonal = 0
    for C in sample:
        mass = 0
        for p in C:
            census[p["omega"]] += p["weight"]
            mass += p["weight"]
            diagonal += p["weight"] ** 2
        masses.append(mass)

    raw = sum(value ** 2 for value in census.values())
    cross = 0
    for i, C in enumerate(sample):
        for k, D in enumerate(sample):
            if i == k:
                continue
            cross += sum(
                p["weight"] * s["weight"]
                for p in C
                for s in D
                if p["omega"] == s["omega"]
            )
    assert raw == diagonal + cross
    counts["uncentered_energy_identities"] += 1

    total_mass = sum(masses)
    centered = Fraction(raw, 1) - Fraction(total_mass ** 2, q - 1)
    diag_centered = sum(
        Fraction(sum(p["weight"] ** 2 for p in C), 1)
        - Fraction(masses[i] ** 2, q - 1)
        for i, C in enumerate(sample)
    )
    cross_centered = Fraction(0, 1)
    for i, C in enumerate(sample):
        for k, D in enumerate(sample):
            if i == k:
                continue
            collision_mass = sum(
                p["weight"] * s["weight"]
                for p in C
                for s in D
                if p["omega"] == s["omega"]
            )
            cross_centered += (
                Fraction(collision_mass, 1)
                - Fraction(masses[i] * masses[k], q - 1)
            )
    assert centered == diag_centered + cross_centered
    assert diag_centered >= 0
    counts["centered_energy_identities"] += 1


total = sum(counts.values())
print("TPC-100 exact provenance certificate")
print(f"resolved branches: {len(branches)}")
print(f"opened atoms: {len(atoms)}")
print(f"fine cells: {len(cells)}")
for key in sorted(counts):
    print(f"{key}: {counts[key]}")
print(f"false quotient witness: {false_quotient_witnesses[0]}")
print(f"total exact checks: {total}")
