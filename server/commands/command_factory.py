from typing import ClassVar

from server.commands.auth_commands import SignInCommand, SignOutCommand, WhoAmICommand
from server.commands.command import Command
from server.commands.command_context import CommandContext
from server.commands.discussion_commands import (
    CreateDiscussionCommand,
    CreateReplyCommand,
    GetDiscussionCommand,
    ListDiscussionsCommand,
)


class CommandFactory:
    commands: ClassVar[dict[str, type[Command]]] = {
        "SIGN_IN": SignInCommand,
        "SIGN_OUT": SignOutCommand,
        "WHOAMI": WhoAmICommand,
        "CREATE_DISCUSSION": CreateDiscussionCommand,
        "CREATE_REPLY": CreateReplyCommand,
        "GET_DISCUSSION": GetDiscussionCommand,
        "LIST_DISCUSSIONS": ListDiscussionsCommand,
    }

    @classmethod
    def create_command(cls, context: CommandContext) -> Command:
        if context.action not in cls.commands:
            raise ValueError(f"Invalid action: {context.action}")

        command_class = cls.commands[context.action]
        return command_class(context)
