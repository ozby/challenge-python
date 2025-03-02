import pytest

from server.di import Container


@pytest.mark.asyncio
async def test_create_discussion(container: Container) -> None:
    discussion_service = container.discussion_service()
    discussion_id = await discussion_service.create_discussion(
        reference="test.30s", comment="Test comment", client_id="user1"
    )

    discussion = await discussion_service.get_discussion(discussion_id)
    assert discussion is not None
    assert discussion.reference_prefix == "test"
    assert discussion.time_marker == "30s"
    assert discussion.client_id == "user1"
    assert len(discussion.replies) == 1
    assert discussion.replies[0].comment == "Test comment"


@pytest.mark.asyncio
async def test_create_reply(container: Container) -> None:
    discussion_service = container.discussion_service()
    discussion_id = await discussion_service.create_discussion(
        reference="test.33s", comment="Initial comment", client_id="user1"
    )

    # Add reply
    await discussion_service.create_reply(
        discussion_id=discussion_id, comment="Reply comment", client_id="user2"
    )

    # Verify reply was added
    discussion = await discussion_service.get_discussion(discussion_id)
    assert len(discussion.replies) == 2
    assert discussion.replies[1].client_id == "user2"
    assert discussion.replies[1].comment == "Reply comment"


@pytest.mark.asyncio
async def test_list_discussions(container: Container) -> None:
    discussion_service = container.discussion_service()
    # Create discussions with different prefixes
    await discussion_service.create_discussion("test1.15s", "Comment 1", "user1")
    await discussion_service.create_discussion("test1.32s", "Comment 2", "user1")
    await discussion_service.create_discussion("test2.59s", "Comment 3", "user2")

    # List discussions with prefix filter
    test1_discussions = await discussion_service.list_discussions(
        reference_prefix="test1"
    )
    assert len(test1_discussions) == 2

    # List all discussions
    all_discussions = await discussion_service.list_discussions()
    assert len(all_discussions) == 3


@pytest.mark.asyncio
async def test_get_discussion(container: Container) -> None:
    discussion_service = container.discussion_service()
    discussion_id = await discussion_service.create_discussion(
        "ref.30s", "test comment 3", "user1"
    )
    discussion = await discussion_service.get_discussion(discussion_id)

    assert discussion is not None
    assert discussion.discussion_id == discussion_id
    assert discussion.reference_prefix == "ref"
    assert discussion.time_marker == "30s"
    assert discussion.client_id == "user1"
    assert discussion.replies[0].comment == "test comment 3"
