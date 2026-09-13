#!/usr/bin/env python3
import argparse, re, signal, subprocess, sys, tempfile
from pathlib import Path

parser = argparse.ArgumentParser(description="Run the Overfull TeX kernel on an NDJSON input.")
parser.add_argument("input", type=Path)
args = parser.parse_args()

# Let an external timeout terminate TeX and clean up the temporary files.
signal.signal(signal.SIGTERM, lambda *_: sys.exit(2))
try:
    with tempfile.TemporaryDirectory(prefix="overfull-") as directory:
        work = Path(directory)
        (work / "kernel.tex").write_bytes(Path(__file__).resolve().with_name("kernel.tex").read_bytes())
        with args.input.open("rb") as source, (work / "input.bytes").open("wb") as encoded:
            while chunk := source.read(65536):
                encoded.write(("\n".join(map(str, chunk)) + "\n").encode("ascii"))
            encoded.write(b"0\n")
        with (work / "input.bytes").open("rb") as encoded, (work / "tex.log").open("wb") as log:
            result = subprocess.run(
                ["tex", "-halt-on-error", "-no-shell-escape",
                 "-cnf-line=extra_mem_top=200000000", "-cnf-line=extra_mem_bot=10000000",
                 "-cnf-line=max_strings=4000000", "-cnf-line=pool_size=64000000",
                 "-cnf-line=hash_extra=4000000", "kernel.tex"],
                stdin=encoded, stdout=log, stderr=subprocess.STDOUT, cwd=work)
        if result.returncode:
            with (work / "tex.log").open("rb") as log:
                log.seek(max(0, log.seek(0, 2) - 4096))
                sys.stderr.buffer.write(log.read())
            sys.exit(3)
        raw = (work / "kernel.out").read_bytes()
        if len(raw) > 4096 or not re.fullmatch(rb"(?:[0-9]+\s+)+", raw):
            raise ValueError("invalid output encoding")
        verdict = bytes(int(value) for value in raw.split())
        if not re.fullmatch(rb"(?:ACCEPT|(?:REJECT|DECLINE) [!-~]+)\n", verdict):
            raise ValueError("missing or malformed verdict")
        sys.stdout.buffer.write(verdict)
        sys.exit({b"ACCEPT": 0, b"REJECT": 1, b"DECLINE": 2}[verdict.split()[0]])
except (OSError, ValueError, KeyError) as error:
    print(f"Overfull runner error: {error}", file=sys.stderr)
    sys.exit(3)
