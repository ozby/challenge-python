from server.services.validation_service import ValidationService

INVALID_REQUEST_ID = "Invalid request_id. Must be 7 lowercase letters (a-z)"


class Response:
    def __init__(self, request_id: str, params: list[str] | None = None):
        if params is None:
            params = []
        self.request_id = request_id
        self.params = params

    def serialize(self) -> str:
        if not ValidationService.validate_request_id(self.request_id):
            raise ValueError(INVALID_REQUEST_ID)

        parts = [self.request_id]
        if len(self.params) > 0:
            parts.extend(self.params)

        return "|".join(parts) + "\n"

    def serialize_list(self) -> str:
        if not ValidationService.validate_request_id(self.request_id):
            raise ValueError(INVALID_REQUEST_ID)

        return self.request_id + "|(" + ",".join(self.params) + ")\n"
