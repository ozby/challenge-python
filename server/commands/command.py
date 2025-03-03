from abc import abstractmethod
from typing import final

from server.commands.command_context import CommandContext


class Command:
    def __init__(self, context: CommandContext):
        self.context = context
        self.container = context.container

    @abstractmethod
    async def _validate(self) -> None:
        """validation logic to be implemented by derived classes"""
        pass

    @abstractmethod
    async def _execute_impl(self) -> str:
        """execution logic to be implemented by derived classes"""
        pass

    @final
    async def execute(self) -> str:
        """Final method that executes validation before implementation"""
        await self._validate()
        return await self._execute_impl()
