# Overfull

A lean4 kernel implemented in TeX.

Don't concern yourself too much over its provenance: it's roughly lean4lean, chewed up and slobbered out by your friendly neighbourhood shoggoth.

This is not performant enough to check Mathlib, but does pass many of the [Lean Kernel Arena](https://arena.lean-lang.org/) tests.

As of 2026-09-13, we pass 165/198 of the Lean Kernel Arena tests within a 60s time limit. With a one-hour time limit, this rises to 179/198.

Requires Python 3 and TeX Live (`tex`). Clone this repo, then run:

```sh
./check.py test.ndjson
```
`ACCEPT` means valid (exit 0), `REJECT` invalid (exit 1), and `DECLINE` unsupported (exit 2); runner errors exit 3. Run `timeout 30s ./check.py test.ndjson` to use the Arena's 30s limit (timeout exits 124).
