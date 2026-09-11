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


def is_canonical_bsn(bsn: str) -> bool:
    """Return whether *bsn* is a canonical, nine-character ASCII digit string."""
    return len(bsn) == BSN_LENGTH and bsn.isascii() and bsn.isdecimal()


def passes_bsn_checksum(bsn: str) -> bool:
    """Check canonical formatting and the 11-proof, not issuance or identity.

    The all-zero string passes this mathematical check too.
    """
    if not is_canonical_bsn(bsn):
        return False

    total = sum(int(digit) * weight for digit, weight in zip(bsn, BSN_WEIGHTS))
    return total % 11 == 0


def is_valid_bsn(bsn: str) -> bool:
    """Compatibility wrapper for passes_bsn_checksum; checks no issuance rules."""
    return passes_bsn_checksum(bsn)


def hash_bsn(bsn: str) -> dict[str, str]:
    """Hash a canonical candidate for demonstration, without checking its checksum.

    Raise RuntimeError if a required algorithm is unavailable.
    """
    if not is_canonical_bsn(bsn):
        raise ValueError("BSN must be exactly 9 ASCII digits")

    bsn_bytes = bsn.encode("utf-8")
    digests = {}
    for algorithm in HASH_ALGORITHMS:
        try:
            # These hashes demonstrate enumeration; they provide no protection.
            digests[algorithm] = hashlib.new(
                algorithm, bsn_bytes, usedforsecurity=False
            ).hexdigest()
        except ValueError as exc:
            raise RuntimeError(
                f"Required hash algorithm '{algorithm}' is unavailable in this Python build"
            ) from exc
    return digests
