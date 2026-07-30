# RH-290: Triple-branch spectral/counterloop ledger

The RH-282 certificate changes the noisy spectral ledger but does not merge it
with the graded counterloop ledger.

```text
noisy modulus-spectral branch : (true,false,true,true,true)
graded monodromy branch       : (true,true,false,true,true)
cross-branch weighted glue    : false
```

The five entries are legal head, coefficient bridge, uniform tail, analytic
target, and certified boundary constant.  Each branch now satisfies four of
five obligations, but the missing entries belong to different typed objects.
Taking the coordinatewise maximum would give five trues and is invalid unless
the noisy spectral complement satisfies the RH-288 weighted prefix bridge to
the deterministic anchor.  A sufficient typed route must control, on one
clock, both total noisy trace versus counterloop plus anchor and noisy head
versus counterloop.  Head transport alone is insufficient.

Both complete counts remain zero.  Gates A--E remain false/open.
