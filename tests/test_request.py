from server.commands.command_context import CommandContext
from server.di import Container


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

    # # Test SIGN_IN action
    # pytest.assertEqual(
    #     vars(CommandContext.from_line(container, "ougmcim|SIGN_IN|janedoe")),
    #     vars(CommandContext(CommandContext_id="ougmcim", action="SIGN_IN", params=["janedoe"])),
    # )

    # pytest.assertEqual(
    #     vars(CommandContext.from_line(container, "iwhygsi|WHOAMI")),
    #     vars(CommandContext(CommandContext_id="iwhygsi", action="WHOAMI")),
    # )

    # pytest.assertEqual(
    #     vars(CommandContext.from_line(container, "cadlsdo|SIGN_OUT")),
    #     vars(CommandContext(CommandContext_id="cadlsdo", action="SIGN_OUT")),
    # )

    # pytest.assertEqual(
    #     vars(CommandContext.from_line(container, "cadlsdo|SIGN_OUT")),
    #     vars(CommandContext(CommandContext_id="cadlsdo", action="SIGN_OUT")),
    # )

    # pytest.assertEqual(
    #     vars(
    #         CommandContext.from_line(
    #             container,
    #             'ykkngzx|CREATE_DISCUSSION|iofetzv.0s|Hey, folks. What do you think of my video? Does it have enough "polish"?',
    #             TEST_PEER_ID,
    #         )
    #     ),
    #     vars(
    #         CommandContext(
    #             CommandContext_id="ykkngzx",
    #             action="CREATE_DISCUSSION",
    #             params=[
    #                 "iofetzv.0s",
    #                 'Hey, folks. What do you think of my video? Does it have enough "polish"?',
    #             ],
    #             peer_id=TEST_PEER_ID,
    #         )
    #     ),
    # )

    # pytest.assertEqual(
    #     vars(
    #         CommandContext.from_line(
    #             container,
    #             "sqahhfj|CREATE_REPLY|iztybsd|I think it's great!",
    #             TEST_PEER_ID,
    #         )
    #     ),
    #     vars(
    #         CommandContext(
    #             CommandContext_id="sqahhfj",
    #             action="CREATE_REPLY",
    #             params=["iztybsd", "I think it's great!"],
    #             peer_id=TEST_PEER_ID,
    #         )
    #     ),
    # )

    # pytest.assertEqual(
    #     vars(CommandContext.from_line(container, "xthbsuv|GET_DISCUSSION|iztybsd")),
    #     vars(
    #         CommandContext(
    #             CommandContext_id="xthbsuv", action="GET_DISCUSSION", params=["iztybsd"]
    #         )
    #     ),
    # )

    # pytest.assertEqual(
    #     vars(CommandContext.from_line(container, "xthbsuv|LIST_DISCUSSIONS")),
    #     vars(CommandContext(CommandContext_id="xthbsuv", action="LIST_DISCUSSIONS", params=[])),
    # )

    # pytest.assertEqual(
    #     vars(CommandContext.from_line(container, "xthbsuv|LIST_DISCUSSIONS|refprefix")),
    #     vars(
    #         CommandContext(
    #             CommandContext_id="xthbsuv",
    #             action="LIST_DISCUSSIONS",
    #             params=["refprefix"],
    #         )
    #     ),
    # )


# def test_parse_failures(container: Container) -> None:
#     with pytest.assertRaises(ValueError):
#         CommandContext.from_line(container, "abc|SIGN_IN|janedoe")

#     with pytest.assertRaises(ValueError):
#         CommandContext.from_line(container, "abc123d|SIGN_IN|janedoe")

#     with pytest.assertRaises(ValueError):
#         CommandContext.from_line(container, "abcdefg")

#     with pytest.assertRaises(ValueError):
#         CommandContext.from_line(container, "cadlsdo|INVALID")

#     with pytest.assertRaises(ValueError):
#         CommandContext.from_line(container, "abcdefg|SIGN_IN")

#     with pytest.assertRaises(ValueError):
#         CommandContext.from_line(container, "abcdefg|SIGN_IN|invalid@id")

#     with pytest.assertRaises(ValueError):
#         CommandContext.from_line(container, "abcdefg|SIGN_IN|invalid id")

#     with pytest.assertRaises(ValueError):
#         CommandContext.from_line(container, "abcdefg|SIGN_IN|")

#     with pytest.assertRaises(ValueError):
#         CommandContext.from_line(container, "ykkngzx|CREATE_DISCUSSION|iofetzv.0s")

#     with pytest.assertRaises(ValueError):
#         CommandContext.from_line(container, "ykkngzx|CREATE_DISCUSSION|iofetzv.0s|")

#     with pytest.assertRaises(ValueError):
#         CommandContext.from_line(container, "ykkngzx|CREATE_DISCUSSION|iofetzv|zaaa")


# if __name__ == "__main__":
#     unittest.main(verbosity=2)
