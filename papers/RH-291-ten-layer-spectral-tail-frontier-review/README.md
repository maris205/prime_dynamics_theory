# RH-291: Ten-layer spectral-tail frontier review

RH-282--RH-291 reopen the operator route through a projection-free normal
spectral realization.  For the Hardy-scaled folded Gaussian operator, the
modulus-complete head `|mu|>1/2` is a genuine finite noisy spectral
submultiset, while its diagonal complement satisfies the RH-279 trace norm,
operator norm, prefix, and root-rate conditions with

```text
R = 7/5,
m_sigma = ceil(4 log(1/sigma)),
root-rate upper = (7/10) exp(1/4) < 1.
```

The complement has an all-order trace envelope, and its moving high-order
`det_2` tail factor converges to one for every fixed derivative order.  The
logarithmic clock is sharp for the inherited `S2` mass-and-cap information
class, and the modulus head is minimal once the threshold is fixed.

The cloud-side audit also changes: the exact comparison shell must use the
finite radius `beta_k`, not the limiting radius `beta`.  Re-centering improves
all seven archived root errors, but remains finite floating evidence.  A
diagonal theorem gives a growing actual-noisy trace prefix, while a hidden
root-of-unity shell proves that unweighted prefix agreement cannot identify a
divisor.

The updated ledgers are:

```text
noisy modulus spectrum      (true,false,true,true,true)
graded monodromy counterloop (true,true,false,true,true)
weighted cross-branch glue   false
```

Both complete counts are zero.  Gates A--E remain false/open.  RH-292 should
address the missing direct weighted modulus-complement-to-anchor prefix.  A
sufficient route must simultaneously control, on the RH-282 clock, total
noisy trace versus counterloop plus anchor and noisy head versus the
finite-radius counterloop.  Head transport alone, more tail estimates, or
finite endpoint fits are not the frontier.

## Reproduction and archive audit

Run each paper's result builder and tests, compile all ten PDFs, then from this
directory run:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_batch_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_batch_archive.py
```
