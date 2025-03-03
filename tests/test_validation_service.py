import unittest

from server.services.validation_service import ValidationService


class TestValidator(unittest.TestCase):
    def test_validate_request_id(self) -> None:
        self.assertTrue(ValidationService.validate_request_id("abcdefg"))

        self.assertFalse(ValidationService.validate_request_id("abc"))  # too short
        self.assertFalse(ValidationService.validate_request_id("abcdefgh"))  # too long
        self.assertFalse(ValidationService.validate_request_id("ABCDEFG"))
        self.assertFalse(
            ValidationService.validate_request_id("abc123")
        )  # numbers not allowed

    def test_validate_client_id(self) -> None:
        self.assertTrue(ValidationService.validate_alphanumeric("janedoe"))
        self.assertTrue(ValidationService.validate_alphanumeric("jane123"))
        self.assertTrue(ValidationService.validate_alphanumeric("JANE123"))

        self.assertFalse(ValidationService.validate_alphanumeric("jane@doe"))
        self.assertFalse(
            ValidationService.validate_alphanumeric("jane doe")
        )  # spaces not allowed
        self.assertFalse(
            ValidationService.validate_alphanumeric("")
        )  # empty not allowed

    def test_validate_reference(self) -> None:
        self.assertTrue(ValidationService.validate_reference("xqunqcc.1m30s"))
        self.assertTrue(ValidationService.validate_reference("abc123.20s"))
        self.assertTrue(ValidationService.validate_reference("test.33s"))

        self.assertFalse(ValidationService.validate_reference("ref1.ref2.ref3"))
        self.assertFalse(ValidationService.validate_reference("single"))
        self.assertFalse(ValidationService.validate_reference(""))  # empty not allowed
        self.assertFalse(
            ValidationService.validate_reference(".abc")
        )  # leading dot not allowed
        self.assertFalse(
            ValidationService.validate_reference("abc.")
        )  # trailing dot not allowed
        self.assertFalse(
            ValidationService.validate_reference("abc..def")
        )  # empty parts not allowed
        self.assertFalse(
            ValidationService.validate_reference("abc.@.def")
        )  # special chars not allowed
        self.assertFalse(
            ValidationService.validate_reference("abc.def ghi")
        )  # spaces not allowed
