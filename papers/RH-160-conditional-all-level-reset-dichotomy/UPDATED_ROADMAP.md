# Roadmap after RH-160

RH-160 ends this ten-paper block with a falsifiable conditional map.  The
remaining work is no longer ambiguous:

1. **O — overlap law.** Prove or refute an eventual lower for consecutive
   reset-frame overlap.  Track running minima and delayed suffixes.
2. **E — weak eigenvalue/tail law.** Prove or refute a uniform subunit bound
   `tau_n / (ell_n - tau_n) < 1`.
3. **S — selected spread law.** Prove or refute a positive lower for
   `(ell_n - tau_n) / u_n`; E alone does not prevent this ratio from vanishing.
4. **L — lag law, only if directional output is needed.** Prove or refute a
   bounded required lag and a positive outward normalized fourth-cross margin.
5. **A — typed assembly.** Feed either the native seed or the joint
   native--directional seed into one consistent downstream construction.

Each interface has an explicit falsifier in the paper.  Failure of L leaves
the native route alive; failure of O, E, or S defeats the present native
formula and should trigger a redesign rather than an overclaim.
