import pytest

from server.commands.command_context import CommandContext
from server.di import Container
from tests.conftest import TEST_PEER_ID


def test_parse_actions(container: Container) -> None:
    # Test SIGN_IN action
    assert vars(CommandContext.from_line(container, "ougmcim|SIGN_IN|janedoe")) == vars(
        CommandContext(
            container=container,
            request_id="ougmcim",
            action="SIGN_IN",
            params=["janedoe"],
        )
    )

    # Test SIGN_IN action
    assert vars(CommandContext.from_line(container, "ougmcim|SIGN_IN|janedoe")) == vars(
        CommandContext(
            container, request_id="ougmcim", action="SIGN_IN", params=["janedoe"]
        )
    )

    assert vars(CommandContext.from_line(container, "iwhygsi|WHOAMI")) == vars(
        CommandContext(container, request_id="iwhygsi", action="WHOAMI")
    )

    assert vars(CommandContext.from_line(container, "cadlsdo|SIGN_OUT")) == vars(
        CommandContext(container, request_id="cadlsdo", action="SIGN_OUT")
    )

    assert vars(CommandContext.from_line(container, "cadlsdo|SIGN_OUT")) == vars(
        CommandContext(container, request_id="cadlsdo", action="SIGN_OUT")
    )

    assert vars(
        CommandContext.from_line(
            container,
            'ykkngzx|CREATE_DISCUSSION|iofetzv.0s|Hey, folks. What do you think of my video? Does it have enough "polish"?',
            TEST_PEER_ID,
        )
    ) == vars(
        CommandContext(
            container,
            request_id="ykkngzx",
            action="CREATE_DISCUSSION",
            params=[
                "iofetzv.0s",
                'Hey, folks. What do you think of my video? Does it have enough "polish"?',
            ],
            peer_id=TEST_PEER_ID,
        )
    )

    assert vars(
        CommandContext.from_line(
            container,
            "sqahhfj|CREATE_REPLY|iztybsd|I think it's great!",
            TEST_PEER_ID,
        )
    ) == vars(
        CommandContext(
            container,
            request_id="sqahhfj",
            action="CREATE_REPLY",
            params=["iztybsd", "I think it's great!"],
            peer_id=TEST_PEER_ID,
        )
    )

    assert vars(
        CommandContext.from_line(container, "xthbsuv|GET_DISCUSSION|iztybsd")
    ) == vars(
        CommandContext(
            container, request_id="xthbsuv", action="GET_DISCUSSION", params=["iztybsd"]
        )
    )

    assert vars(
        CommandContext.from_line(container, "xthbsuv|LIST_DISCUSSIONS")
    ) == vars(
        CommandContext(
            container, request_id="xthbsuv", action="LIST_DISCUSSIONS", params=[]
        )
    )

    assert vars(
        CommandContext.from_line(container, "xthbsuv|LIST_DISCUSSIONS|refprefix")
    ) == vars(
        CommandContext(
            container,
            request_id="xthbsuv",
            action="LIST_DISCUSSIONS",
            params=["refprefix"],
        )
    )


def test_parse_failures(container: Container) -> None:
    with pytest.raises(ValueError):
        CommandContext.from_line(container, "abc|SIGN_IN|janedoe")

    with pytest.raises(ValueError):
        CommandContext.from_line(container, "abc123d|SIGN_IN|janedoe")

    with pytest.raises(ValueError):
        CommandContext.from_line(container, "abcdefg")

    # with pytest.raises(ValueError):
    #     CommandContext.from_line(container, "cadlsdo|INVALID")
