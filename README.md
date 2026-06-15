# BSN Hash Awareness PoC

This repository demonstrates why hashing Dutch BSNs (Burger Service Nummers)
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

## Files

- `bsn.py`: shared BSN formatting, validation, and hashing helpers.
- `bsncheck.py`: checks one BSN candidate.
- `genbsnlist.py`: streams valid-looking BSN candidates and unsalted hashes for
  a numeric range.

## Usage

Check one candidate:

```sh
python3 bsncheck.py 123456782
```

Generate a small demo range:

```sh
python3 genbsnlist.py 0 10000
```

Generate CSV with a header:

```sh
python3 genbsnlist.py --csv --header 0 10000
```

For a simple lookup demonstration:

```sh
grep -m 1 '<hash>' demo-output.txt
grep -m 1 '<hash>' demo-output.txt | awk '{print $1}'
```

The point of the demo is that this lookup requires no special tooling once the
candidate hashes exist.
