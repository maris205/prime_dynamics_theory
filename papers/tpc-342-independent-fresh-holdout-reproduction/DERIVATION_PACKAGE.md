# TPC-342 derivation package

## 1. Finite response vectors

For source class C and control j, define

~~~text
y_(C,j) = A P_j beta_C,
~~~

where A is the fixed all-plus deleted-diagonal operator, P_j is one of the
nine declared coordinate bijections, and beta_C is the source vector masked
to class C.

## 2. Aggregate projection

Let J be the nine controls and put

~~~text
bar y_(C,J) = (1/9) sum_(j in J) y_(C,j),
N_J = [bar y_(B,J), bar y_(P,J), bar y_(Z,J)].
~~~

Let P_J be the Euclidean orthogonal projector onto col(N_J).  The reported
in-sample statistic is

~~~text
rho_J = ||(I-P_J) bar y_(T,J)||_2^2 / ||bar y_(T,J)||_2^2.
~~~

The SVD rank rule is the number of singular values strictly above
max(shape)*eps*sigma_max.  In the three new rows the prime-power column is
zero, so the certified rank is two.

## 3. Held-out projection

For an omitted control j, define

~~~text
N_(-j) = [mean_(i != j) y_(B,i),
          mean_(i != j) y_(P,i),
          mean_(i != j) y_(Z,i)].
~~~

The test statistic is

~~~text
rho^LOO_j = ||(I-P_(-j)) y_(T,j)||_2^2 / ||y_(T,j)||_2^2.
~~~

The omitted twin output is not used to form P_(-j).  This is a deterministic
control-index holdout, not a probabilistic independence assertion.

## 4. Exact identity

For every finite matrix N and vector y, the projector is self-adjoint and
idempotent.  Hence P_N y is orthogonal to (I-P_N)y, and

~~~text
||y||_2^2 = ||P_N y||_2^2 + ||(I-P_N)y||_2^2.
~~~

Dividing by ||y||_2^2 gives 0 <= rho_N(y) <= 1 for nonzero y.

## 5. Panel facts

The three source intervals are [40097,40608], [40609,41120], and
[41121,41632]; all shifted arguments satisfy the declared parent cutoff.
There are 108 raw class/control records and 81 nonempty records.  The
in-sample retention range is 0.2701410521--0.2951006120; the 27 holdout
retentions range from 0.5894842476 to 0.9429165296.

These numbers are finite observations of the declared model.  No limiting
parameter, source-uniform estimate, signed cancellation, or twin-prime
conclusion is derived from them.
