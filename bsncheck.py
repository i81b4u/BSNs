#!/usr/bin/env python3
import argparse

from bsn import is_canonical_bsn, passes_bsn_checksum


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether a candidate passes the BSN checksum; does not verify issuance."
    )
    parser.add_argument("bsn", help="9-digit BSN candidate")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not is_canonical_bsn(args.bsn):
        print(f"{args.bsn} has invalid formatting: must be exactly 9 ASCII digits.")
        return 1

    if passes_bsn_checksum(args.bsn):
        print(f"{args.bsn} passes the BSN checksum.")
        return 0

    print(f"{args.bsn} does not pass the BSN checksum.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
