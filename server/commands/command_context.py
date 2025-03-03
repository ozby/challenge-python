from server.di import Container
from server.services.validation_service import ValidationService

MIN_PART = 2


class CommandContext:

    def __init__(
        self,
        container: Container,
        request_id: str,
        params: list[str] | None = None,
        peer_id: str | None = None,
        action: str | None = None,
    ):
        self.container = container
        self.request_id = request_id
        self.params = params or []
        self.peer_id = peer_id
        self.action = action

    @staticmethod
    def from_line(
        container: Container, line: str, peer_id: str | None = None
    ) -> "CommandContext":
        parts = [part for part in line.strip().split("|") if part]

        if len(parts) < MIN_PART:
            raise ValueError("Invalid format. Expected: request_id|action[|params]")

        request_id = parts[0]
        if not ValidationService.validate_request_id(request_id):
            raise ValueError("Invalid request_id. Must be 7 lowercase letters (a-z)")

        action = parts[1]
        params = parts[2:] if len(parts) >= MIN_PART else []

        return CommandContext(container, request_id, params, peer_id, action)
