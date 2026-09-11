"""Regression tests using published RvIG fixtures and explicit edge cases."""
import contextlib
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from bsn import format_bsn, hash_bsn, is_canonical_bsn, is_valid_bsn, passes_bsn_checksum
import genbsnlist

ROOT = Path(__file__).resolve().parents[1]
# Independently verified with OpenSSL, hashing ASCII bytes without a newline.
DIGESTS = {
    "999990019": {
        "md5": "31eab5921ffd56c890338b3e5764a823",
        "sha1": "1039fcbb1b58ac124e8d4ed8995f57bc334c98e8",
        "sha256": "b554d7c7f2357ba2ac037a697ff379a104ccb6599f65be83aa0f938c3c105cf2",
    },
    "000000012": {
        "md5": "0c3f2275ea9dcd2ea182c6c0d2e8ac87",
        "sha1": "00354506a952f7eefb9818870e8ad4cbe7cf9194",
        "sha256": "f2a2fd588510d1966fc8ec9c876259d24e041c905bdba67d0ceeb050dd62e651",
    },
}


class HelperTests(unittest.TestCase):
    def test_formatting_and_bounds(self):
        for value, expected in ((0, "000000000"), (12, "000000012"),
                                (999999999, "999999999")):
            with self.subTest(value=value):
                self.assertEqual(format_bsn(value), expected)
        for value in (-1, 1000000000):
            with self.subTest(value=value), self.assertRaises(ValueError):
                format_bsn(value)

    def test_canonical_input(self):
        for value in ("", "12345678", "0000000012", "９９９９９００１９",
                      "٩٩٩٩٩٠٠١٩", "99999001x", "999990019\n", " 00000012"):
            with self.subTest(value=value):
                self.assertFalse(is_canonical_bsn(value))
                self.assertFalse(passes_bsn_checksum(value))
                with self.assertRaises(ValueError):
                    hash_bsn(value)

    def test_checksum_and_compatibility(self):
        # Zero is a checksum edge case, not an assertion of BSN issuance.
        for value, expected in (("999990019", True), ("000000012", True),
                                ("000000000", True), ("999990018", False)):
            with self.subTest(value=value):
                self.assertTrue(is_canonical_bsn(value))
                self.assertEqual(passes_bsn_checksum(value), expected)
                self.assertEqual(is_valid_bsn(value), expected)

    def test_known_hashes(self):
        for value, expected in DIGESTS.items():
            with self.subTest(value=value):
                self.assertEqual(hash_bsn(value), expected)

    def test_hashing_does_not_require_checksum(self):
        self.assertEqual(set(hash_bsn("999990018")), {"md5", "sha1", "sha256"})

    def test_restricted_hash_provider(self):
        import hashlib
        original_new = hashlib.new

        def restricted_new(name, data, *, usedforsecurity=True):
            if usedforsecurity:
                raise ValueError("blocked for security use")
            return original_new(name, data, usedforsecurity=False)

        with patch("bsn.hashlib.new", side_effect=restricted_new):
            self.assertEqual(hash_bsn("000000012"), DIGESTS["000000012"])

    def test_unavailable_algorithm(self):
        with patch("bsn.hashlib.new", side_effect=ValueError("unavailable")):
            with self.assertRaisesRegex(RuntimeError, "'md5'.*unavailable"):
                hash_bsn("000000012")

    def test_range_bounds(self):
        for begin, end in ((0, 0), (0, 1), (999999999, 1000000000),
                           (1000000000, 1000000000)):
            with self.subTest(begin=begin, end=end):
                genbsnlist.validate_range(begin, end)
        for begin, end in ((-1, 1), (0, -1), (2, 1), (0, 1000000001),
                           (1000000001, 1000000001)):
            with self.subTest(begin=begin, end=end), self.assertRaises(ValueError):
                genbsnlist.validate_range(begin, end)


class CliTests(unittest.TestCase):
    def run_cli(self, script, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / script), *args], cwd=ROOT,
            capture_output=True, text=True, timeout=10,
        )

    def test_checker_messages_and_exit_codes(self):
        for value, code, message in (
            ("999990019", 0, "passes the BSN checksum."),
            ("000000012", 0, "passes the BSN checksum."),
            ("000000000", 0, "passes the BSN checksum."),
            ("999990018", 2, "does not pass the BSN checksum."),
            ("12345678", 1, "has invalid formatting: must be exactly 9 ASCII digits."),
        ):
            with self.subTest(value=value):
                result = self.run_cli("bsncheck.py", value)
                self.assertEqual(result.returncode, code)
                self.assertEqual(result.stdout, f"{value} {message}\n")
                self.assertEqual(result.stderr, "")

    def test_generator_formats_and_half_open_range(self):
        for flags, separator in (((), " "), (("--csv",), ",")):
            with self.subTest(flags=flags):
                result = self.run_cli("genbsnlist.py", *flags, "--header",
                                      "999990018", "999990020")
                expected = separator.join(("bsn", "md5", "sha1", "sha256")) + "\n"
                expected += separator.join(("999990019", *DIGESTS["999990019"].values())) + "\n"
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout, expected)
                self.assertEqual(result.stderr, "")
        result = self.run_cli("genbsnlist.py", "999990018", "999990019")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_generator_preserves_leading_zeroes_without_header(self):
        result = self.run_cli("genbsnlist.py", "12", "13")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, " ".join(("000000012", *DIGESTS["000000012"].values())) + "\n")

    def test_empty_range_at_upper_bound(self):
        result = self.run_cli("genbsnlist.py", "1000000000", "1000000000")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_invalid_range(self):
        result = self.run_cli("genbsnlist.py", "-1", "1")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "error: range bounds must be non-negative\n")

    def test_argument_errors(self):
        for script, args in (("bsncheck.py", ()), ("genbsnlist.py", ("abc", "1"))):
            with self.subTest(script=script):
                result = self.run_cli(script, *args)
                self.assertEqual(result.returncode, 2)
                self.assertIn("usage:", result.stderr)

    def test_generator_reports_unavailable_algorithm(self):
        output = io.StringIO()
        with patch.object(sys, "argv", ["genbsnlist.py", "12", "13"]), \
                patch("bsn.hashlib.new", side_effect=ValueError("unavailable")), \
                contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as raised:
                genbsnlist.main()
        self.assertEqual(str(raised.exception),
                         "error: Required hash algorithm 'md5' is unavailable in this Python build")
        self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
