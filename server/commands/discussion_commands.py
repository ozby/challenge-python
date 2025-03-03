from server.commands.command import Command
from server.response import Response
from server.services.validation_service import ValidationService


class CreateDiscussionCommand(Command):

    async def _validate(self) -> None:
        if len(self.context.params) != 2:
            raise ValueError("action requires two parameters")

        reference, comment = self.context.params[0], self.context.params[1]
        if not ValidationService.validate_reference(reference):
            raise ValueError("reference must be period-delimited alphanumeric")

        if len(comment) >= 250:
            raise ValueError("comment must be less than 250 characters")

        self.client_id = await self.container.session_service().get_client_id(
            self.context.peer_id
        )
        if self.client_id is None:
            raise ValueError("authentication is required")

    async def _execute_impl(self) -> str:
        created_id = await self.container.discussion_service().create_discussion(
            self.context.params[0],
            self.context.params[1],
            self.client_id,  # type: ignore
        )
        self._created_discussion_id = created_id
        return Response(
            request_id=self.context.request_id, params=[created_id]
        ).serialize()


class CreateReplyCommand(Command):

    async def _validate(self) -> None:
        if len(self.context.params) != 2:
            raise ValueError("action requires two parameters")

        self.client_id = await self.container.session_service().get_client_id(
            self.context.peer_id
        )
        if self.client_id is None:
            raise ValueError("authentication is required")

    async def _execute_impl(self) -> str:
        discussion_id, comment = self.context.params[0], self.context.params[1]
        self._discussion_id = discussion_id
        reply_id = await self.container.discussion_service().create_reply(
            discussion_id, comment, self.client_id  # type: ignore
        )
        self._reply_id = reply_id
        return Response(request_id=self.context.request_id).serialize()


class GetDiscussionCommand(Command):

    async def _validate(self) -> None:
        if len(self.context.params) != 1:
            raise ValueError("action requires one parameter")

    async def _execute_impl(self) -> str:
        discussion = await self.container.discussion_service().get_discussion(
            self.context.params[0]
        )
        if discussion is None:
            raise ValueError("Discussion not found")

        replies = []
        for reply in discussion.replies:
            replies.append(f"{reply.client_id}|{reply.comment}")
        params = [
            discussion.discussion_id,
            f"{discussion.reference_prefix}.{discussion.time_marker}",
            "(" + ",".join(replies) + ")",
        ]
        return Response(request_id=self.context.request_id, params=params).serialize()


class ListDiscussionsCommand(Command):

    async def _validate(self) -> None:
        if len(self.context.params) > 1:
            raise ValueError("action can't have more than one parameter")

    async def _execute_impl(self) -> str:
        discussions = await self.container.discussion_service().list_discussions()

        discussion_list = []
        for discussion in discussions:
            replies = []
            for reply in discussion.replies:
                replies.append(f"{reply.client_id}|{reply.comment}")

            discussion_list.append(
                f"{discussion.discussion_id}|{discussion.reference_prefix}.{discussion.time_marker}|({','.join(replies)})"
            )
        return Response(
            request_id=self.context.request_id, params=discussion_list
        ).serialize_list()
