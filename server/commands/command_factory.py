from typing import ClassVar, Type, Union, cast

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
    _commands: ClassVar[dict[str, Type[Command]]] = {
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
        
        command_class = cls._commands[action]
        
        if command_class in (CreateDiscussionCommand, CreateReplyCommand, 
                            GetDiscussionCommand, ListDiscussionsCommand):
            discussion_service = get_container().discussion_service()
            
            if command_class == CreateDiscussionCommand:
                command = cast(Command, CreateDiscussionCommand(context, discussion_service))
            elif command_class == CreateReplyCommand:
                command = cast(Command, CreateReplyCommand(context, discussion_service))
            elif command_class == GetDiscussionCommand:
                command = cast(Command, GetDiscussionCommand(context, discussion_service))
            elif command_class == ListDiscussionsCommand:
                command = cast(Command, ListDiscussionsCommand(context, discussion_service))
            else:
                raise RuntimeError("Unexpected command class")
        else:
            command = command_class(context)
            
        cls._command_history.append(command)
        return command

    @classmethod
    def get_last_command(cls) -> Command | None:
        """Get the last executed command"""
        return cls._command_history[-1] if cls._command_history else None

    @classmethod
    def clear_history(cls) -> None:
        """Clear the command history"""
        cls._command_history.clear()
