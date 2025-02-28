from server.commands.command import Command, CommandContext
from server.response import Response
from server.services.session_service import SessionService
from server.validation import Validator

class SignInCommand(Command):
    def _validate(self) -> None:
        if len(self.context.params) != 1:
            raise ValueError("SIGN_IN action requires exactly one parameter")

        if not Validator.validate_client_id(self.context.params[0]):
            raise ValueError("client_id must be alphanumeric")

    def execute(self) -> str:
        if self.context.peer_id is None:
            raise ValueError("peer_id is required")
            
        session_service = SessionService()
        session_service.set(
            peer_id=self.context.peer_id,
            user_id=self.context.params[0]
        )
        return Response(request_id=self.context.request_id).serialize()
    
    def undo(self) -> None:
        if self.context.peer_id:
            session_service = SessionService()
            session_service.delete(peer_id=self.context.peer_id)
    
    def can_undo(self) -> bool:
        return True

class SignOutCommand(Command):
    def _validate(self) -> None:
        pass

    def execute(self) -> str:
        session_service = SessionService()
        # Store the current user_id for potential undo
        self._previous_user_id = session_service.get_client_id(self.context.peer_id)
        session_service.delete(peer_id=self.context.peer_id)
        return Response(request_id=self.context.request_id).serialize()
    
    def undo(self) -> None:
        if hasattr(self, '_previous_user_id') and self._previous_user_id and self.context.peer_id:
            session_service = SessionService()
            session_service.set(
                peer_id=self.context.peer_id,
                user_id=self._previous_user_id
            )
    
    def can_undo(self) -> bool:
        return True

class WhoAmICommand(Command):
    def _validate(self) -> None:
        pass

    def execute(self) -> str:
        session_service = SessionService()
        client_id = session_service.get_client_id(self.context.peer_id)
        params = [client_id] if client_id is not None else None
        return Response(request_id=self.context.request_id, params=params).serialize()
    
    def undo(self) -> None:
        pass