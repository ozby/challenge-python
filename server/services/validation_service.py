from re import compile


class ValidationService:
    REQUEST_ID_PATTERN = compile(r"^[a-z]{7}$")
    ALPHANUMERIC_PATTERN = compile(r"^[a-zA-Z0-9]+$")

    @classmethod
    def validate_request_id(cls, request_id: str) -> bool:
        return bool(cls.REQUEST_ID_PATTERN.match(request_id))

    @classmethod
    def validate_alphanumeric(cls, client_id: str) -> bool:
        return bool(cls.ALPHANUMERIC_PATTERN.match(client_id))

    @classmethod
    def validate_reference(cls, reference: str) -> bool:
        parts = reference.split(".")
        if len(parts) != 2:
            return False

        if not cls.validate_alphanumeric(parts[0]):
            return False
        time_pattern = compile(r"^(?:\d+m)?(?:\d+s)$")
        return bool(time_pattern.match(parts[1]))
