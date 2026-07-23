# RH-112: global wedge-Lipschitz barrier

RH-112 tests whether propagating the fourth exterior operator as one global
object can improve the singular-value-product certificate of RH-109.

The answer is negative, in a precise sense.  For `||E|| <= delta`,

```text
||wedge^4(A+E)-wedge^4(A)||
    <= (||A||+delta)^4-||A||^4.
```

This norm-only constant is sharp on scalar identities.  Nevertheless, the
resulting normalized four-volume lower bound is universally no larger than
the product Weyl bound.  Its positivity radius is

```text
s1*((1+nu_hat)^(1/4)-1) ~ s1*nu_hat/4,
```

whereas product Weyl stays positive up to `delta < s4`.  Thus weak-mode
capacity is paid inside the global exterior perturbation constant.

The archived audit contains 360 records and no domination failures.  This is
a useful negative result: the global norm-only branch is closed, while
directional right-frame wedge actions are not ruled out and become RH-113.

Reproduce with:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_wedge_lipschitz_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_wedge_lipschitz_audit.py --smoke
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
```

No all-level exterior lower law, Stage A closure, Hilbert--Polya operator,
zero identification, or Riemann Hypothesis conclusion is claimed.
