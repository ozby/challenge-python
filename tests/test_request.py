import unittest

from server.request import Request


class TestParserInput(unittest.TestCase):
    def test_parse_actions(self) -> None:
        # Test SIGN_IN action
        self.assertEqual(
            vars(Request.from_line("ougmcim|SIGN_IN|janedoe")),
            vars(Request(request_id="ougmcim", action="SIGN_IN", params=["janedoe"])),
        )

        self.assertEqual(
            vars(Request.from_line("iwhygsi|WHOAMI")),
            vars(Request(request_id="iwhygsi", action="WHOAMI")),
        )

        self.assertEqual(
            vars(Request.from_line("cadlsdo|SIGN_OUT")),
            vars(Request(request_id="cadlsdo", action="SIGN_OUT")),
        )

        self.assertEqual(
            vars(Request.from_line("cadlsdo|SIGN_OUT")),
            vars(Request(request_id="cadlsdo", action="SIGN_OUT")),
        )

    def test_parse_failures(self) -> None:
        with self.assertRaises(ValueError):
            Request.from_line("abc|SIGN_IN|janedoe")

        with self.assertRaises(ValueError):
            Request.from_line("abc123d|SIGN_IN|janedoe")

        with self.assertRaises(ValueError):
            Request.from_line("abcdefg")

        with self.assertRaises(ValueError):
            Request.from_line("cadlsdo|INVALID")

        with self.assertRaises(ValueError):
            Request.from_line("abcdefg|SIGN_IN")

        with self.assertRaises(ValueError):
            Request.from_line("abcdefg|SIGN_IN|invalid@id")

        with self.assertRaises(ValueError):
            Request.from_line("abcdefg|SIGN_IN|invalid id")

        with self.assertRaises(ValueError):
            Request.from_line("abcdefg|SIGN_IN|")


if __name__ == "__main__":
    unittest.main(verbosity=2)
