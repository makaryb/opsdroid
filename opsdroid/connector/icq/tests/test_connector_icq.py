import logging

from opsdroid.connector.icq import ConnectorICQ

connector_config = {
    "token": "test:token",
    "base-url": "test:base-url",
}


def test_init(opsdroid):
    config = {
        "token": "test:token",
        "whitelisted-users": ["sam", 12345],
        "base-url": "https://test.com",
    }

    connector = ConnectorICQ(config, opsdroid=opsdroid)

    assert "icq" == connector.name
    assert "test:token" == connector.token
    assert ["sam", 12345] == connector.whitelisted_users
    assert "https://test.com" == connector.base_url


def test_init_no_token(opsdroid, caplog):
    connector_config_without_token = {
        "base-url": "test:base-url",
    }
    connector = ConnectorICQ(connector_config_without_token, opsdroid=opsdroid)
    caplog.set_level(logging.ERROR)

    assert "icq" == connector.name
    assert connector.whitelisted_users is None
    assert "test:base-url" == connector.base_url
    assert "Unable to login: Access token is missing" in caplog.text


def test_init_no_base_url(opsdroid, caplog):
    connector_config_without_base_url = {
        "token": "test:token",
    }
    connector = ConnectorICQ(connector_config_without_base_url, opsdroid=opsdroid)
    caplog.set_level(logging.ERROR)

    assert connector.name == "icq"
    assert connector.token == "test:token"
    assert connector.whitelisted_users is None
    assert connector.base_url is None


def test_get_user_from_pm(opsdroid):
    response = {
        "eventId": 2,
        "payload": {
            "chat": {"chatId": "765432100", "type": "private"},
            "from": {
                "firstName": "Samuel",
                "lastName": "B",
                "nick": "samb",
                "userId": "765432100",
            },
            "msgId": "12345678901234567890",
            "text": "123 text",
            "timestamp": 1666609676,
        },
        "type": "newMessage",
    }

    connector = ConnectorICQ(connector_config, opsdroid=opsdroid)

    chat_id, user_id = connector.get_user(response)

    assert chat_id == "765432100"
    assert user_id == "765432100"


def test_get_user_from_group_chat(opsdroid):
    response = {
        "eventId": 4,
        "payload": {
            "chat": {
                "chatId": "687147040@chat.agent",
                "title": "testGroup opsdroid",
                "type": "group",
            },
            "from": {
                "firstName": "Samuel",
                "lastName": "B",
                "nick": "samb",
                "userId": "765432100",
            },
            "msgId": "12345678901234567890",
            "text": "12345 text",
            "timestamp": 1666610077,
        },
        "type": "newMessage",
    }

    connector = ConnectorICQ(connector_config, opsdroid=opsdroid)

    chat_id, user_id = connector.get_user(response)

    assert chat_id == "687147040@chat.agent"
    assert user_id == "765432100"


def test_get_user_from_channel(opsdroid):
    response = {
        "eventId": 6,
        "payload": {
            "chat": {
                "chatId": "687147090@chat.agent",
                "title": "testChannel opsdroid",
                "type": "channel",
            },
            "from": {
                "firstName": "Samuel",
                "lastName": "B",
                "nick": "samb",
                "userId": "765432100",
            },
            "msgId": "12345678901234567890",
            "text": "1234567890 text",
            "timestamp": 1666610239,
        },
        "type": "newMessage",
    }

    connector = ConnectorICQ(connector_config, opsdroid=opsdroid)

    chat_id, user_id = connector.get_user(response)

    assert chat_id == "687147090@chat.agent"
    assert user_id == "765432100"


def test_handle_user_permission_empty_whitelist(opsdroid):
    connector = ConnectorICQ(connector_config, opsdroid=opsdroid)

    permission = connector.handle_user_permission("687147040@chat.agent", "765432100")

    assert permission is True


def test_handle_user_permission_present_in_white_list(opsdroid):
    connector_config["whitelisted-users"] = ["687147040@chat.agent"]
    connector = ConnectorICQ(connector_config, opsdroid=opsdroid)

    permission = connector.handle_user_permission("687147040@chat.agent", "765432100")

    assert permission is True


def test_handle_user_permission_not_empty_white_list(opsdroid):
    connector_config["whitelisted-users"] = ["12341234@chat.agent"]
    connector = ConnectorICQ(connector_config, opsdroid=opsdroid)

    permission = connector.handle_user_permission("687147040@chat.agent", "765432100")

    assert permission is False


def test_build_url(opsdroid):
    connector_config["base-url"] = "api.icq.net/bot/v1/"
    connector = ConnectorICQ(connector_config, opsdroid=opsdroid)

    url = connector.build_url("events/get")

    assert url == "https://api.icq.net/bot/v1/events/get"
