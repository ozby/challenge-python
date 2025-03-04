from collections.abc import AsyncGenerator

import pytest

from server.commands.command_context import CommandContext
from server.commands.discussion_commands import (
    CreateDiscussionCommand,
    CreateReplyCommand,
    GetDiscussionCommand,
    ListDiscussionsCommand,
)
from server.di import Container
from server.services.validation_service import ValidationService
from tests.conftest import TEST_PEER_ID


@pytest.fixture(autouse=True)
async def client_id(container: Container) -> AsyncGenerator[str, None]:
    session_service = container.session_service()
    client_id = "tester_client_1"
    await session_service.set(TEST_PEER_ID, client_id)
    yield client_id


async def test_create_discussion_validates_params(container: Container) -> None:
    context = CommandContext(
        container, "abcdefg", ["ref.30s", "test comment"], TEST_PEER_ID
    )
    await CreateDiscussionCommand(context).execute()

    with pytest.raises(ValueError, match="action requires two parameters"):
        await CreateDiscussionCommand(
            CommandContext(container, "abcdefg", [], TEST_PEER_ID),
        ).execute()

    with pytest.raises(ValueError, match="action requires two parameters"):
        await CreateDiscussionCommand(
            CommandContext(container, "abcdefg", ["ref.30s"], TEST_PEER_ID),
        ).execute()

    with pytest.raises(
        ValueError, match="reference must be period-delimited alphanumeric"
    ):
        await CreateDiscussionCommand(
            CommandContext(
                container, "abcdefg", ["ref,123", "test comment"], TEST_PEER_ID
            ),
        ).execute()

    with pytest.raises(ValueError):
        await CreateDiscussionCommand(
            CommandContext.from_line(container, "ykkngzx|CREATE_DISCUSSION|iofetzv.0s")
        ).execute()

    with pytest.raises(ValueError):
        await CreateDiscussionCommand(
            CommandContext.from_line(container, "ykkngzx|CREATE_DISCUSSION|iofetzv.0s|")
        ).execute()

    with pytest.raises(ValueError):
        await CreateDiscussionCommand(
            CommandContext.from_line(
                container, "ykkngzx|CREATE_DISCUSSION|iofetzv|zaaa"
            )
        ).execute()


async def test_create_discussion_executes(container: Container) -> None:
    context = CommandContext(
        container, "abcdefg", ["ref.30s", "test comment"], TEST_PEER_ID
    )
    command = CreateDiscussionCommand(context)
    result = (await command.execute()).rstrip("\n")
    parts = result.split("|")
    assert len(parts) == 2
    assert parts[0] == "abcdefg"

    assert ValidationService.validate_request_id(parts[0])
    assert ValidationService.validate_alphanumeric(parts[1])


async def test_create_reply_executes(container: Container) -> None:
    created = CreateDiscussionCommand(
        CommandContext(container, "abcdefg", ["ref.30s", "test comment"], TEST_PEER_ID),
    )
    created_discussion_id = (await created.execute()).strip("\n").split("|")[1]

    await CreateReplyCommand(
        CommandContext(
            container,
            "abcdefg",
            [created_discussion_id, "test reply yooo"],
            TEST_PEER_ID,
        ),
    ).execute()

    returned_discussion = await GetDiscussionCommand(
        CommandContext(container, "abcdefg", [created_discussion_id], TEST_PEER_ID),
    ).execute()
    assert '"' not in returned_discussion


async def test_create_reply_executes_with_comma(container: Container) -> None:
    created = CreateDiscussionCommand(
        CommandContext(container, "abcdefg", ["ref.30s", "test comment"], TEST_PEER_ID),
    )
    created_discussion_id = (await created.execute()).strip("\n").split("|")[1]

    reply = CreateReplyCommand(
        CommandContext(
            container,
            "abcdefg",
            [created_discussion_id, "test reply, yooo"],
            TEST_PEER_ID,
        ),
    )
    await reply.execute()

    returned_discussion = GetDiscussionCommand(
        CommandContext(container, "abcdefg", [created_discussion_id], TEST_PEER_ID),
    )
    returned = await returned_discussion.execute()
    assert '"' in returned


async def test_get_discussion_executes(
    client_id: str,
    container: Container,
) -> None:
    created = CreateDiscussionCommand(
        CommandContext(container, "abcdefg", ["ref.30s", "test comment"], TEST_PEER_ID),
    )
    created_discussion_id = (await created.execute()).strip("\n").split("|")[1]

    returned_discussion = await GetDiscussionCommand(
        CommandContext(container, "abcdefg", [created_discussion_id], TEST_PEER_ID),
    ).execute()
    assert (
        returned_discussion
        == f"abcdefg|{created_discussion_id}|ref.30s|({client_id}|test comment)\n"
    )


async def test_create_reply_validates_params(container: Container) -> None:
    created = CreateDiscussionCommand(
        CommandContext(container, "abcdefg", ["ref.30s", "test comment"], TEST_PEER_ID),
    )
    created_discussion_id = (await created.execute()).strip("\n").split("|")[1]

    context = CommandContext(
        container, "abcdefg", [created_discussion_id, "test reply"], TEST_PEER_ID
    )
    await CreateReplyCommand(context).execute()

    with pytest.raises(ValueError, match="action requires two parameters"):
        await CreateReplyCommand(
            CommandContext(container, "abcdefg", [], TEST_PEER_ID),
        ).execute()

    with pytest.raises(ValueError, match="action requires two parameters"):
        await CreateReplyCommand(
            CommandContext(container, "abcdefg", ["disc123"], TEST_PEER_ID),
        ).execute()


async def test_get_discussion_validates_params(container: Container) -> None:
    created = CreateDiscussionCommand(
        CommandContext(container, "abcdefg", ["ref.30s", "test comment"], TEST_PEER_ID),
    )
    created_discussion_id = (await created.execute()).strip("\n").split("|")[1]

    context = CommandContext(
        container, "abcdefg", [created_discussion_id], TEST_PEER_ID
    )
    await GetDiscussionCommand(context).execute()

    with pytest.raises(ValueError, match="action requires one parameter"):
        await GetDiscussionCommand(
            CommandContext(container, "abcdefg", [], TEST_PEER_ID)
        ).execute()

    with pytest.raises(ValueError, match="action requires one parameter"):
        await GetDiscussionCommand(
            CommandContext(
                container, "abcdefg", [created_discussion_id, "extra"], TEST_PEER_ID
            )
        ).execute()


async def test_list_discussion_validates_params(container: Container) -> None:
    created = CreateDiscussionCommand(
        CommandContext(
            container, "abcdefg", ["ndgdojs.15s", "test comment"], TEST_PEER_ID
        )
    )
    created_discussion_id = (await created.execute()).strip("\n").split("|")[1]

    await CreateReplyCommand(
        CommandContext(
            container,
            "replyaa",
            [created_discussion_id, "I love this video. What did you use to make it?"],
            TEST_PEER_ID,
        ),
    ).execute()

    await CreateReplyCommand(
        CommandContext(
            container,
            "replybb",
            [
                created_discussion_id,
                'I used something called "ozbys amazing tool", it\'s pretty cool!',
            ],
            TEST_PEER_ID,
        )
    ).execute()

    created = CreateDiscussionCommand(
        CommandContext(
            container, "zzzzccs", ["asdasds.15s", "test comment"], TEST_PEER_ID
        ),
    )
    created_discussion_id = (await created.execute()).strip("\n").split("|")[1]

    await CreateReplyCommand(
        CommandContext(
            container, "replyaa", [created_discussion_id, "sadsdsadas"], TEST_PEER_ID
        ),
    ).execute()

    await CreateReplyCommand(
        CommandContext(
            container, "replybb", [created_discussion_id, "pdskfdsjfds"], TEST_PEER_ID
        ),
    ).execute()


async def test_list_discussion_executes(container: Container) -> None:
    await ListDiscussionsCommand(
        CommandContext(container, "abcdefg", [], TEST_PEER_ID),
    ).execute()
