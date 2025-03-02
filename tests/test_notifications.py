import time
from collections.abc import AsyncGenerator

import pytest

from server.di import Container
from server.entities.notification import NotificationType

# Test data
TEST_PEER_1 = "127.0.0.1:8001"
TEST_PEER_2 = "127.0.0.1:8002"
TEST_PEER_3 = "127.0.0.1:8003"
TEST_PEER_4 = "127.0.0.1:8004"


@pytest.fixture(autouse=True)
async def setup(container: Container) -> AsyncGenerator[None, None]:
    session_service = container.session_service()
    # Setup test users
    await session_service.set(TEST_PEER_1, "user1")
    await session_service.set(TEST_PEER_2, "user2")
    await session_service.set(TEST_PEER_3, "user3")
    await session_service.set(TEST_PEER_4, "user4")
    yield


@pytest.mark.asyncio
async def test_reply_notifications(container: Container) -> None:
    discussion_service = container.discussion_service()
    notification_service = container.notification_service()
    # Create initial discussion by user1
    discussion_id = await discussion_service.create_discussion(
        reference="test.33s", comment="Initial discussion", client_id="user1"
    )

    # User2 replies
    await discussion_service.create_reply(
        discussion_id=discussion_id, comment="First reply", client_id="user2"
    )

    # Check notifications for user1 (should get notification from user2's reply)
    user1_notifications = await notification_service.get_notifications("user1")
    assert len(user1_notifications) == 1
    assert user1_notifications[0].notification_type == NotificationType.REPLY
    assert user1_notifications[0].sender_id == "user2"
    assert user1_notifications[0].recipient_id == "user1"

    # User3 replies
    await discussion_service.create_reply(
        discussion_id=discussion_id, comment="Second reply", client_id="user3"
    )

    # Check notifications for user1 and user2
    user1_notifications = await notification_service.get_notifications("user1")
    user2_notifications = await notification_service.get_notifications("user2")

    assert (
        len(user1_notifications) == 2
    )  # Should have notifications from user2 and user3
    assert len(user2_notifications) == 1  # Should have notification from user3


@pytest.mark.asyncio
async def test_mention_notifications(container: Container) -> None:
    discussion_service = container.discussion_service()
    notification_service = container.notification_service()
    # Create discussion with mentions
    await discussion_service.create_discussion(
        reference="test.456",
        comment="Hey @user2 and @user3, check this out!",
        client_id="user1",
    )

    # Check notifications for mentioned users
    user2_notifications = await notification_service.get_notifications("user2")
    user3_notifications = await notification_service.get_notifications("user3")

    assert len(user2_notifications) == 1
    assert user2_notifications[0].notification_type == NotificationType.MENTION
    assert user2_notifications[0].sender_id == "user1"
    assert user2_notifications[0].recipient_id == "user2"

    assert len(user3_notifications) == 1
    assert user3_notifications[0].notification_type == NotificationType.MENTION
    assert user3_notifications[0].sender_id == "user1"
    assert user3_notifications[0].recipient_id == "user3"


@pytest.mark.asyncio
async def test_combined_reply_and_mention_notifications(container: Container) -> None:
    discussion_service = container.discussion_service()
    notification_service = container.notification_service()
    # User1 creates discussion mentioning user4
    discussion_id = await discussion_service.create_discussion(
        reference="test.789",
        comment="Hey @user4, what do you think?",
        client_id="user1",
    )

    # User4 should have a mention notification
    user4_notifications = await notification_service.get_notifications("user4")
    assert len(user4_notifications) == 1
    assert user4_notifications[0].notification_type == NotificationType.MENTION

    # User2 replies and mentions user3
    await discussion_service.create_reply(
        discussion_id=discussion_id,
        comment="@user3 might have some insights here too!",
        client_id="user2",
    )

    # User1 should have a reply notification (from user2)
    user1_notifications = await notification_service.get_notifications("user1")
    assert len(user1_notifications) == 1
    assert user1_notifications[0].notification_type == NotificationType.REPLY
    assert user1_notifications[0].sender_id == "user2"

    # User3 should have a mention notification (from user2)
    user3_notifications = await notification_service.get_notifications("user3")
    assert len(user3_notifications) == 1
    assert user3_notifications[0].notification_type == NotificationType.MENTION
    assert user3_notifications[0].sender_id == "user2"


@pytest.mark.asyncio
async def test_self_mention_and_reply(container: Container) -> None:
    discussion_service = container.discussion_service()
    notification_service = container.notification_service()
    # User1 creates discussion mentioning themselves
    discussion_id = await discussion_service.create_discussion(
        reference="test.self",
        comment="I'm talking to myself @user1 here",
        client_id="user1",
    )

    # User1 shouldn't have a mention notification
    user1_notifications = await notification_service.get_notifications("user1")
    assert len(user1_notifications) == 0

    # User1 replies to their own discussion
    await discussion_service.create_reply(
        discussion_id=discussion_id,
        comment="Replying to myself",
        client_id="user1",
    )

    # User1 still shouldn't have any notifications
    user1_notifications = await notification_service.get_notifications("user1")
    assert len(user1_notifications) == 0


@pytest.mark.asyncio
async def test_mark_notifications_as_read(container: Container) -> None:
    discussion_service = container.discussion_service()
    notification_service = container.notification_service()
    # Create discussion with mentions and replies
    discussion_id = await discussion_service.create_discussion(
        reference="test.33s", comment="Hey @user2, check this out!", client_id="user1"
    )

    await discussion_service.create_reply(
        discussion_id=discussion_id,
        comment="Replying and mentioning @user3",
        client_id="user2",
    )

    # Verify initial notifications
    user1_notifications = await notification_service.get_notifications("user1")
    user2_notifications = await notification_service.get_notifications("user2")
    user3_notifications = await notification_service.get_notifications("user3")

    assert len(user1_notifications) == 1  # Reply notification
    assert len(user2_notifications) == 1  # Mention notification
    assert len(user3_notifications) == 1  # Mention notification

    # Mark notifications as read for user1
    await notification_service.mark_as_read("user1", discussion_id)

    # Verify notifications after marking as read
    user1_notifications = await notification_service.get_notifications("user1")
    user2_notifications = await notification_service.get_notifications("user2")
    assert len(user1_notifications) == 0  # Should be cleared
    assert len(user2_notifications) == 1  # Should remain unchanged


@pytest.mark.asyncio
async def test_notification_ordering(container: Container) -> None:
    discussion_service = container.discussion_service()
    notification_service = container.notification_service()
    # Create discussion
    discussion_id = await discussion_service.create_discussion(
        reference="test.33s",
        comment="Initial discussion mentioning @user2",
        client_id="user1",
    )

    # Add replies with small time gaps
    time.sleep(0.1)
    await discussion_service.create_reply(
        discussion_id=discussion_id,
        comment="First reply mentioning @user2",
        client_id="user3",
    )

    time.sleep(0.1)
    await discussion_service.create_reply(
        discussion_id=discussion_id,
        comment="Second reply mentioning @user2",
        client_id="user4",
    )

    # Get notifications for user2
    notifications = await notification_service.get_notifications("user2")

    # Verify notifications are ordered by created_at descending
    assert len(notifications) == 3
    for i in range(len(notifications) - 1):
        assert notifications[i].created_at > notifications[i + 1].created_at


@pytest.mark.asyncio
async def test_invalid_mentions(container: Container) -> None:
    discussion_service = container.discussion_service()
    notification_service = container.notification_service()
    # Test mentions with various edge cases
    await discussion_service.create_discussion(
        reference="test.33s",
        comment="""
        @user2, @user3@invalid @not_a_user
        @@user4 @@ @
        """,
        client_id="user1",
    )

    # Only valid mentions should create notifications
    user2_notifications = await notification_service.get_notifications("user2")
    user3_notifications = await notification_service.get_notifications("user3")
    user4_notifications = await notification_service.get_notifications("user4")

    assert len(user2_notifications) == 1  # Valid mention: @user2,
    assert len(user3_notifications) == 0  # Invalid: @user3@invalid
    assert len(user4_notifications) == 0  # Invalid: @@user4


@pytest.mark.asyncio
async def test_duplicate_mentions(container: Container) -> None:
    discussion_service = container.discussion_service()
    notification_service = container.notification_service()
    # Create discussion with duplicate mentions
    await discussion_service.create_discussion(
        reference="test.33s",
        comment="Hey @user2 @user2 @user2, multiple mentions!",
        client_id="user1",
    )

    # Should only create one notification despite multiple mentions
    user2_notifications = await notification_service.get_notifications("user2")
    assert len(user2_notifications) == 1


@pytest.mark.asyncio
async def test_mention_in_reply_to_own_discussion(container: Container) -> None:
    discussion_service = container.discussion_service()
    notification_service = container.notification_service()
    # User1 creates discussion
    discussion_id = await discussion_service.create_discussion(
        reference="test.33s", comment="Initial discussion", client_id="user1"
    )

    # User1 replies to their own discussion mentioning others
    await discussion_service.create_reply(
        discussion_id=discussion_id,
        comment="Mentioning @user2 and @user3 in my own discussion",
        client_id="user1",
    )

    # Check notifications
    user1_notifications = await notification_service.get_notifications("user1")
    user2_notifications = await notification_service.get_notifications("user2")
    user3_notifications = await notification_service.get_notifications("user3")

    assert len(user1_notifications) == 0  # No self notifications
    assert len(user2_notifications) == 1
    assert len(user3_notifications) == 1


@pytest.mark.asyncio
async def test_performance_many_notifications(container: Container) -> None:
    discussion_service = container.discussion_service()
    notification_service = container.notification_service()
    # Create discussion
    discussion_id = await discussion_service.create_discussion(
        reference="test.33s", comment="Initial discussion", client_id="user1"
    )

    # Add many replies (testing bulk notification creation)
    for i in range(50):
        await discussion_service.create_reply(
            discussion_id=discussion_id,
            comment=f"Reply {i} mentioning @user2",
            client_id="user3",
        )

    # Verify notifications were created correctly
    user1_notifications = await notification_service.get_notifications("user1")
    user2_notifications = await notification_service.get_notifications("user2")

    assert len(user1_notifications) == 50  # Reply notifications
    assert len(user2_notifications) == 50  # Mention notifications


@pytest.mark.asyncio
async def test_mark_all_as_read(container: Container) -> None:
    discussion_service = container.discussion_service()
    notification_service = container.notification_service()
    # Create multiple discussions with notifications
    discussion_id1 = await discussion_service.create_discussion(
        reference="test.33s",
        comment="First discussion mentioning @user2",
        client_id="user1",
    )

    discussion_id2 = await discussion_service.create_discussion(
        reference="test.456",
        comment="Second discussion mentioning @user2",
        client_id="user1",
    )

    # Mark all notifications as read for user2
    await notification_service.mark_as_read("user2", discussion_id1)
    await notification_service.mark_as_read("user2", discussion_id2)

    # Verify all notifications are cleared
    user2_notifications = await notification_service.get_notifications("user2")
    assert len(user2_notifications) == 0


@pytest.mark.asyncio
async def test_notification_after_mark_as_read(container: Container) -> None:
    discussion_service = container.discussion_service()
    notification_service = container.notification_service()
    # Create discussion
    discussion_id = await discussion_service.create_discussion(
        reference="test.33s",
        comment="Initial discussion mentioning @user2",
        client_id="user1",
    )

    # Mark as read
    await notification_service.mark_as_read("user2", discussion_id)

    # Add new reply with mention
    await discussion_service.create_reply(
        discussion_id=discussion_id,
        comment="New reply mentioning @user2",
        client_id="user3",
    )

    # Verify new notifications are created after mark as read
    user2_notifications = await notification_service.get_notifications("user2")
    assert len(user2_notifications) == 1
