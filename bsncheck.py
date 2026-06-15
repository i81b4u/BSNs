#!/usr/bin/env python3
import argparse

from bsn import BSN_LENGTH, is_valid_bsn


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether a BSN candidate is mathematically valid."
    )
    parser.add_argument("bsn", help="9-digit BSN candidate")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not (args.bsn.isdigit() and len(args.bsn) == BSN_LENGTH):
        print(f"{args.bsn} is not a valid BSN: must be exactly 9 digits.")
        return 1

    if is_valid_bsn(args.bsn):
        print(f"{args.bsn} is a mathematically valid BSN.")
        return 0

    print(f"{args.bsn} is not a mathematically valid BSN.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
