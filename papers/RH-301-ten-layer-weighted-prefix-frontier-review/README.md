# RH-301: Ten-layer weighted-prefix frontier review

RH-292--RH-301 sharpen the sole remaining analytic determinant leaf without
claiming that it is closed.

The main positive reduction is that the bridge need not reach the convenient
slope-four tail cut.  Within the current sharp mass-and-cap envelope, tail
absorption shortens the certified bridge clock to

    a_* = 1/log(10/7) = 2.803673252057129....

At this critical certified clock, a uniform coefficient error
O(sigma^beta) has the sharp information-class threshold

    beta >= a_* log(7/5) = 0.9433582098747317....

The existing coefficientwise inputs do imply a weighted full-trace bridge on
some unknown slow clock, but not on this logarithmic clock.  The archived
orbit-tube localization ceiling is only 1/log(lambda)=1.930709419..., so its
clock range is disjoint from every mass-and-cap tail-admissible bridge.

If the counterloop period is tied to the intrinsic endpoint-resolution
clock, the minimal bridge crosses one exact alias and the slope-four cut
crosses two.  A separate absolute majorant for the square-root parity
correction also grows on the minimal clock; grouped cancellation is
essential.

For the head constituent, zero-padded root-l1 transport gives the sharp local
shell threshold 0.6729348509145321 within its disk-bounded information
class, but no actual noisy-head matching is known.  The cleanest direct
alternative is annular convergence of the
complement logarithmic mismatch in H-infinity or H2 on any

    1.4 < rho < 1.4267874838640739.

The typed ledgers remain

    noisy modulus spectrum       = (true,false,true,true,true)
    graded monodromy counterloop = (true,true,false,true,true)
    weighted cross-branch glue   = false
    complete count               = 0

Gates A--E remain false/open.

## Reproduction and archive audit

Run each paper result builder and test suite, compile all ten PDFs, then from
this directory run:

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_batch_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_batch_archive.py
