# RH-398 research audit

## Research question

Across all fixed positive lags, what is the exact maximum of the RH-396
fixed-lag Euler-run endpoint, which lags attain it, what happens on the
complement, and what joint endpoint remains after reintroducing finite phase
clocks?

## Supported answer

- `B_infinity(h)<=B_infinity(1)` for every fixed `h>=1`.
- Equality holds exactly when `mu^2(h)=1 and gcd(h,210)=1`.
- The complement has supremum `B_infinity(1)` but does not attain it.
- For `h=p^2`, prime `p>=11`, the strict gap is at most `1/p^2`.
- If `p0(h)>=5`, the gap is larger than `2/1334025`, with the stronger
  proved chain through `1/36750`.
- The joint supremum over fixed `h` and finite `q` is `B_infinity(1)` and no
  finite pair attains it.
- The retained infimum is `3/pi^2` and is not attained.

## Novel contribution

Within the frozen RH corpus and source closure, the contribution is the exact
fixed-lag comparison and equality classification.  Its load-bearing steps
are:

1. rewriting the endpoint using the `A_m` product and a finite alternating
   telescope;
2. computing all four parity branches of the residue-deletion loss
   `Lambda_T(L)`;
3. transferring those branches to the three prime-square collision levels;
4. proving the complete weak local order and identifying every strict even
   run;
5. partitioning all lags into exact equality and strictness branches, with
   the special prime-`2` condition treated correctly;
6. realizing every strict local loss on a positive-density exact-run CRT
   cylinder;
7. passing all finite comparisons on one common cofinal prime-initial
   sequence using RH-396's absolute Euler-product tail;
8. constructing the prime-square complement sequence and the quantitative
   `p0>=5` cylinder gap;
9. combining the fixed-lag maximum with RH-396's strict finite-clock theorem.

The novelty statement is search-bounded by the repository closure.  It is
not a global claim that no analogous theorem exists outside that boundary.

## Evidence layers

| Layer | Role |
|---|---|
| RH-396 | sole load-bearing analytic endpoint and finite-clock theorem |
| manuscript proof | telescope, deletion loss, local transfer, equality partition, strict cylinders, complement and joint endpoint |
| RH-397 | direct release and provenance predecessor only |
| RH-394, RH-392, RH-395, RH-375 | transitive provenance and comparison only |
| 72-row certificate | finite exact reproduction and negative controls |
| result/schema/source tests | implementation, type, source, and claim-firewall protection |
| release tests | archive membership, offline replay, official schema, and hygiene protection |

## Adversarial questions resolved

| Question | Resolution |
|---|---|
| Is the comparison a growing-lag terminal theorem? | No. Every endpoint is evaluated at a separately fixed scalar lag. |
| May one compare different finite prime supports? | The proof uses a common support first and one common cofinal passage afterward. |
| Does local nonincrease alone prove strictness? | No. Strictness is charged to a positive-density exact-run cylinder. |
| Is `2|h` an ordinary square-factor branch? | No. It is the special equivalence `2|h iff 4|d`. |
| Is squarefreeness enough for equality? | No. Factors `3`, `5`, or `7` are strict. |
| Is coprimality to `210` enough? | No. Odd square factors at least `11` are strict. |
| Can primes at least `11` be ignored without a range proof? | Only when squarefree, because the base cutoff allows run lengths at most eight and the exact deletion formula proves invisibility on that range. |
| Does a finite CRT word establish a strict endpoint gap? | No. The proof requires the associated positive-density cylinder and the Euler-product tail. |
| Does the complement attain its supremum? | No. The exact equality classification excludes every complement lag. |
| Can a finite clock attain the joint supremum? | No. RH-396 gives strictness for every finite `q`. |

Research verdict: GO within fixed-data terminal-log scalar endpoint scope.
