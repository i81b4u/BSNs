# BSN Hash Awareness PoC

This repository demonstrates why hashing Dutch BSNs (Burgerservicenummers)
with unsalted MD5, SHA-1, or SHA-256 is not enough to make them safe.

The generator emits only canonical BSN candidates that pass the 11-proof checksum.
They do not prove that a BSN was ever issued or belongs to a real person.

## Why This Matters

A BSN has a small, enumerable input space: 9 decimal digits. The BSN checksum
(the 11-proof) makes it cheap to filter that space down to valid-looking
candidates. Because the input space is small, an attacker can generate every
valid-looking BSN candidate, hash each one, and look up leaked unsalted hashes.

The hash algorithm does not solve this by itself. SHA-256 is stronger than MD5
or SHA-1 for many purposes, but a deterministic SHA-256 hash of a tiny input
space is still practical to enumerate.

Important points:

- Unsalted BSN hashes are pseudonymous identifiers, not anonymized data.
- Salting prevents shared precomputed tables, but a known salt still allows
  enumeration.
- A keyed HMAC with a strong secret is a better fit when deterministic matching
  is required.
- Avoid storing stable BSN-derived identifiers unless they are genuinely needed.
- Always hash the canonical 9-digit, zero-padded BSN string if demonstrating
  this behavior. `012345678` and `12345678` hash to different values.
- These scripts generate awareness output only. Do not publish generated BSN
  lists or hash lookup tables.

## Safe Use

Do not enter a real BSN into these command-line tools. Command-line arguments
and output may be retained in shell history, process listings, terminal
scrollback, CI logs, recordings, monitoring tools, or redirected files. Use
only published test BSNs in a controlled local environment. Do not redirect
generated output to persistent storage.

The code accepts only the canonical BSN representation: exactly nine ASCII
digits, including leading zeroes. It does not check whether a candidate was
issued or belongs to a person. Even `000000000` passes the checksum; this
is a mathematical property, not evidence that it is an issuable BSN.

The responsible-use guidance in this README and the disclaimer is not a
licence restriction. See [LICENSE](LICENSE) for the applicable licence.

## Test Data

For tests and examples, use the official
[RvIG test BSN and A-number table](https://www.rvig.nl/test-bsn-a-nummers-omnummertabel), not a real person's
BSN. RvIG states that its omnummertabel BSNs are never coupled to existing
people. It recommends values beginning with `99999` for general testing and
values beginning with `0000` for leading-zero cases.

This repository uses `999990019` (RvIG Test-BSN 910) as its general example
and `000000012` (RvIG Test-BSN 1) for a leading-zero case. The table is not
bundled here; always use the current official source and observe any notices
published with it.

## Files

- `bsn.py`: shared BSN formatting, checksum, and hashing helpers.
- `bsncheck.py`: checks one BSN candidate.
- `genbsnlist.py`: streams valid-looking BSN candidates and unsalted hashes for
  a numeric range.
- `tests/test_bsn.py`: standard-library regression tests.
- `.github/workflows/tests.yml`: runs tests on Python 3.11–3.14 for pushes and pull requests.

## Requirements

Use Python 3.11 or newer. No third-party packages or installation step are
required; run the scripts from this directory. The minimum supported version
is 3.11; see the [Python version lifecycle](https://devguide.python.org/versions/).

The demo calls `hashlib.new(..., usedforsecurity=False)` because these hashes
are demonstration output, not a security mechanism. This can permit MD5 on
restricted builds; it does not guarantee every build provides all three
algorithms. If an algorithm is unavailable, the generator exits with a clear
error instead of a traceback. See the
[hashlib documentation](https://docs.python.org/3/library/hashlib.html).

## Usage

Check one candidate:

```sh
python3 bsncheck.py 999990019
```

The checker reports `999990019 passes the BSN checksum.` Its exit codes are:

- `0`: canonical input that passes the checksum.
- `1`: input is not exactly nine ASCII digits.
- `2`: checksum failure, or an argument-parsing error (reported on stderr).

Generate a small demo range:

```sh
python3 genbsnlist.py 999990019 999990020
```

Generate CSV with a header:

```sh
python3 genbsnlist.py --csv --header 999990019 999990020
```

The point of the demo is that deterministic hashes of a small input space can
be enumerated; do not retain or distribute the resulting output.


Range starts are inclusive and ends are exclusive. Bounds must satisfy
`0 <= begin <= end <= 1000000000`; empty ranges are allowed. The generator
exits with `0` on success, `1` for invalid ranges or unavailable hash algorithms,
and `2` for argument-parsing errors. With `--header`, an empty range produces
only the header. Errors may occur after a header or earlier rows were emitted.

## Helper API

Use `passes_bsn_checksum(candidate)` for canonical formatting and checksum
checks. `is_valid_bsn(candidate)` remains available as a compatibility wrapper
with identical behavior; new callers should use the explicit name. Neither
function checks issuance or identity. Checker output now says “passes the BSN
checksum” instead of “mathematically valid BSN”; its exit codes are unchanged.

`hash_bsn(candidate)` requires exactly nine ASCII digits but does not require
a passing checksum. It returns MD5, SHA-1, and SHA-256 hex digests, raises
`ValueError` for noncanonical input, and raises `RuntimeError` if a required
algorithm is unavailable. Leading zeroes are part of the hashed input.

## Development and Tests

Run the regression suite from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

Tests cover canonical formatting, leading zeroes, checksum edge cases, fixed
hash values, range boundaries, CSV output, CLI messages and exit codes, and
simulated restricted or unavailable hashing algorithms. Positive examples use
the two published RvIG test values above; other inputs exercise malformed data,
checksum failures, and numeric boundaries. Generated CLI output is captured
in memory and no lookup-table artifacts are written.

GitHub Actions is configured to run this command on Python 3.11, 3.12, 3.13,
and 3.14. Python bytecode caches and local `.venv`/`venv` directories are ignored
by Git.
