#!/usr/bin/env python3
import hashlib

BSN_LENGTH = 9
BSN_MIN = 0
BSN_MAX_EXCLUSIVE = 1_000_000_000

HASH_ALGORITHMS = ("md5", "sha1", "sha256")
BSN_WEIGHTS = (9, 8, 7, 6, 5, 4, 3, 2, -1)


def format_bsn(value: int) -> str:
    """Return a number as a zero-padded 9-digit BSN candidate."""
    if not (BSN_MIN <= value < BSN_MAX_EXCLUSIVE):
        raise ValueError("BSN candidate must be between 0 and 999999999")

    return f"{value:0{BSN_LENGTH}d}"


def is_valid_bsn(bsn: str) -> bool:
    """Return whether a 9-digit string passes the BSN 11-proof checksum."""
    if not (bsn.isdigit() and len(bsn) == BSN_LENGTH):
        return False

    total = sum(int(digit) * weight for digit, weight in zip(bsn, BSN_WEIGHTS))
    return total % 11 == 0


def hash_bsn(bsn: str) -> dict[str, str]:
    """Return MD5, SHA-1, and SHA-256 hex digests for a 9-digit BSN string."""
    if not (bsn.isdigit() and len(bsn) == BSN_LENGTH):
        raise ValueError("BSN must be exactly 9 digits")

    bsn_bytes = bsn.encode("utf-8")
    return {
        algorithm: hashlib.new(algorithm, bsn_bytes).hexdigest()
        for algorithm in HASH_ALGORITHMS
    }
