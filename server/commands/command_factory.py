from typing import ClassVar, cast

from server import get_container
from server.commands.auth_commands import (
    SignInCommand,
    SignOutCommand,
    WhoAmICommand,
)
from server.commands.command import Command, CommandContext
from server.commands.discussion_commands import (
    CreateDiscussionCommand,
    CreateReplyCommand,
    GetDiscussionCommand,
    ListDiscussionsCommand,
)


class CommandFactory:
    _commands: ClassVar[dict[str, type[Command]]] = {
        "SIGN_IN": SignInCommand,
        "SIGN_OUT": SignOutCommand,
        "WHOAMI": WhoAmICommand,
        "CREATE_DISCUSSION": CreateDiscussionCommand,
        "CREATE_REPLY": CreateReplyCommand,
        "GET_DISCUSSION": GetDiscussionCommand,
        "LIST_DISCUSSIONS": ListDiscussionsCommand,
    }

    _command_history: ClassVar[list[Command]] = []

    @classmethod
    def create_command(
        cls,
        action: str,
        request_id: str,
        params: list[str],
        peer_id: str | None = None,
    ) -> Command:
        if action not in cls._commands:
            raise ValueError(f"Unknown action: {action}")

        context = CommandContext(request_id=request_id, params=params, peer_id=peer_id)
        container = get_container()
        command_class = cls._commands[action]
        discussion_service = container.discussion_service()
        session_service = container.session_service()

        if command_class == SignInCommand:
            command = cast(Command, SignInCommand(context, session_service))
        elif command_class == SignOutCommand:
            command = cast(Command, SignOutCommand(context, session_service))
        elif command_class == WhoAmICommand:
            command = cast(Command, WhoAmICommand(context, session_service))
        elif command_class == CreateDiscussionCommand:
            command = cast(
                Command,
                CreateDiscussionCommand(context, discussion_service, session_service),
            )
        elif command_class == CreateReplyCommand:
            command = cast(
                Command,
                CreateReplyCommand(context, discussion_service, session_service),
            )
        elif command_class == GetDiscussionCommand:
            command = cast(Command, GetDiscussionCommand(context, discussion_service))
        elif command_class == ListDiscussionsCommand:
            command = cast(Command, ListDiscussionsCommand(context, discussion_service))
        else:
            command = command_class(context)

        cls._command_history.append(command)
        return command