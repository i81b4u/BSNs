#!/usr/bin/env python3
import argparse

from bsn import BSN_MAX_EXCLUSIVE, format_bsn, hash_bsn, is_valid_bsn


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate mathematically valid BSN candidates and unsalted hash "
            "values for awareness demonstrations."
        )
    )
    parser.add_argument("begin", type=int, help="inclusive range start")
    parser.add_argument("end", type=int, help="exclusive range end")
    parser.add_argument(
        "--csv",
        action="store_true",
        help="write comma-separated output instead of space-separated output",
    )
    parser.add_argument(
        "--header",
        action="store_true",
        help="include a header row",
    )
    return parser.parse_args()


def validate_range(begin: int, end: int) -> None:
    if begin < 0 or end < 0:
        raise ValueError("range bounds must be non-negative")

    if begin > end:
        raise ValueError("range start must be less than or equal to range end")

    if end > BSN_MAX_EXCLUSIVE:
        raise ValueError("range end must be at most 1000000000 for 9-digit BSNs")


def main() -> int:
    args = parse_args()

    try:
        validate_range(args.begin, args.end)
    except ValueError as exc:
        raise SystemExit(f"error: {exc}") from exc

    separator = "," if args.csv else " "
    if args.header:
        print(separator.join(("bsn", "md5", "sha1", "sha256")))

    for value in range(args.begin, args.end):
        bsn = format_bsn(value)
        if not is_valid_bsn(bsn):
            continue

        digests = hash_bsn(bsn)
        print(separator.join((bsn, digests["md5"], digests["sha1"], digests["sha256"])))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
