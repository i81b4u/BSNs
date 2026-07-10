# BSN Hash Awareness PoC

This repository demonstrates why hashing Dutch BSNs (Burgerservicenummers)
with unsalted MD5, SHA-1, or SHA-256 is not enough to make them safe.

The scripts intentionally generate only mathematically valid BSN candidates.
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
issued or belongs to a person.

The responsible-use guidance in this README and the disclaimer is not a
licence restriction. See [LICENSE](LICENSE) for the applicable licence.

## Test Data

For tests and examples, use the official [RvIG test BSN and A-number table]
(https://www.rvig.nl/test-bsn-a-nummers-omnummertabel), not a real person's
BSN. RvIG states that its omnummertabel BSNs are never coupled to existing
people. It recommends values beginning with `99999` for general testing and
values beginning with `0000` for leading-zero cases.

This repository uses `999990019` (RvIG Test-BSN 910) as its general example
and `000000012` (RvIG Test-BSN 1) for a leading-zero case. The table is not
bundled here; always use the current official source and observe any notices
published with it.

## Files

- `bsn.py`: shared BSN formatting, validation, and hashing helpers.
- `bsncheck.py`: checks one BSN candidate.
- `genbsnlist.py`: streams valid-looking BSN candidates and unsalted hashes for
  a numeric range.

## Usage

Check one candidate:

```sh
python3 bsncheck.py 999990019
```

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
