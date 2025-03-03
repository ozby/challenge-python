import pytest

from server.commands.auth_commands import SignInCommand
from server.commands.command_context import CommandContext
from server.di import Container


async def test_create_discussion_validates_params(container: Container) -> None:
    with pytest.raises(ValueError):
        await SignInCommand(
            CommandContext.from_line(container, "abcdefg|SIGN_IN")
        ).execute()

    with pytest.raises(ValueError):
        await SignInCommand(
            CommandContext.from_line(container, "abcdefg|SIGN_IN|invalid@id")
        ).execute()

    with pytest.raises(ValueError):
        await SignInCommand(
            CommandContext.from_line(container, "abcdefg|SIGN_IN|invalid id")
        ).execute()

    with pytest.raises(ValueError):
        await SignInCommand(
            CommandContext.from_line(container, "abcdefg|SIGN_IN|")
        ).execute()
