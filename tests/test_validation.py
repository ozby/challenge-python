import unittest

from server.validation import Validator


class TestValidator(unittest.TestCase):
    def test_validate_request_id(self) -> None:
        self.assertTrue(Validator.validate_request_id("abcdefg"))

        self.assertFalse(Validator.validate_request_id("abc"))  # too short
        self.assertFalse(Validator.validate_request_id("abcdefgh"))  # too long
        self.assertFalse(Validator.validate_request_id("ABCDEFG"))
        self.assertFalse(Validator.validate_request_id("abc123"))  # numbers not allowed

    def test_validate_client_id(self) -> None:
        self.assertTrue(Validator.validate_alphanumeric("janedoe"))
        self.assertTrue(Validator.validate_alphanumeric("jane123"))
        self.assertTrue(Validator.validate_alphanumeric("JANE123"))

        self.assertFalse(Validator.validate_alphanumeric("jane@doe"))
        self.assertFalse(
            Validator.validate_alphanumeric("jane doe")
        )  # spaces not allowed
        self.assertFalse(Validator.validate_alphanumeric(""))  # empty not allowed

    def test_validate_reference(self) -> None:
        self.assertTrue(Validator.validate_reference("xqunqcc.1m30s"))
        self.assertTrue(Validator.validate_reference("abc123.xyz789"))
        self.assertTrue(Validator.validate_reference("TEST.123"))

        self.assertFalse(Validator.validate_reference("ref1.ref2.ref3"))
        self.assertFalse(Validator.validate_reference("single"))
        self.assertFalse(Validator.validate_reference(""))  # empty not allowed
        self.assertFalse(
            Validator.validate_reference(".abc")
        )  # leading dot not allowed
        self.assertFalse(
            Validator.validate_reference("abc.")
        )  # trailing dot not allowed
        self.assertFalse(
            Validator.validate_reference("abc..def")
        )  # empty parts not allowed
        self.assertFalse(
            Validator.validate_reference("abc.@.def")
        )  # special chars not allowed
        self.assertFalse(
            Validator.validate_reference("abc.def ghi")
        )  # spaces not allowed


if __name__ == "__main__":
    unittest.main()
