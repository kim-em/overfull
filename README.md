# Overfull

A lean4 kernel implemented in TeX.

Don't concern yourself too much over its provenance: it's roughly lean4lean, chewed up and slobbered out by your friendly neighbourhood shoggoth.

This is not performant enough to check Mathlib, but does pass many of the [Lean Kernel Arena](https://arena.lean-lang.org/) tests.

As of 2026-09-13, we pass 165/198 of the Lean Kernel Arena tests within a 60s time limit. With a one-hour time limit, this rises to 179/198.

Requires Bash, TeX Live (`tex`), `od`, and `awk`. Put `kernel.tex` and your `test.ndjson` in the same directory.

```sh
set -o pipefail
od -An -v -tu1 test.ndjson | awk '{for (i=1; i<=NF; i++) print $i} END {print 0}' | tex -halt-on-error -cnf-line=extra_mem_top=200000000 -cnf-line=extra_mem_bot=10000000 -cnf-line=max_strings=4000000 -cnf-line=pool_size=64000000 -cnf-line=hash_extra=4000000 kernel.tex > kernel.run.log &&
awk '{printf "%c", $1}' kernel.out
```
`ACCEPT` means valid, `REJECT` invalid, and `DECLINE` unsupported. TeX diagnostics are in `kernel.run.log`.
