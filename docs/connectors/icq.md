# opsdroid connector ICQ

A connector for [ICQ](https://icq.com/).

## Requirements

- ICQ account - to create a bot
- [Bot API Token](https://icq.com/botapi/?lang=en)

_Note: To register a new bot, open ICQ, write **@metabot** and press `START` button. 
Then in `metabot` help menu select `Create a new bot`.
Provide username (ending in bot) and metabot will give you your Bot API Token._

## Configuration

```yaml
connectors:
  icq:
    # required
    token: "001.3333333333.1111111111:1007654321"  # ICQ bot token
    # optional
    base-url: "https://api.icq.net/bot/v1/"
    whitelisted-users:  # List of users who can speak to the bot, if not set anyone can speak
      - user1 # nick or userId
      - user2 # for example 'sam' or '766543245'
```

## Usage

You can add your bot and this connector to:

- Direct Messages
- Groups
- Channels

If you want opsdroid to work on your group or channel, you should allow bot to join chats. You can do it with metabot: in `metabot` help menu select `(Dis)Allow bot to join chats`. Then you should add it by opening your channel/group details and select the _Add Members_ button, then search for your bot username and add it. It's a good idea to add the bot as admin or at least allow bot to write. You can do it in your channel/group details in `Subscribers`/`Members`.

## Whitelisting users

This is an optional config option that you can include on your `configuration.yaml` to prevent unauthorized users to interact with your bot.
Currently, you can specify a user `nick` or a `userId`. Using the `userId` method is preferable as it will increase the security of the connector since users can't change this ID.

Here is how you can whitelist a user:

```yaml
  icq:
    token: <your bot token>
    whitelisted-users:
      - sam
      - 766543245 # this is a userId
```

Finding your `userId` is not straight forward. This value is sent by ICQ when a user sends a private message to someone (the bot in this case) or when someone calls the `events/get` from the API.
To find a `userId` by a private message, set the `logging` level to `debug` and start a new private message to the bot. You will see the API response on your console - it will look similar to this:

```json
{
   "eventId": 1,
    "payload": {
        "chat": {
          "chatId": "766543245", 
          "type": "private"
        },
        "from": {
            "firstName": "Samuel",
            "lastName": "B",
            "nick": "sam",
            "userId": "766543245"
        },
        "msgId": "12345678901234567890",
        "text": "123 text",
        "timestamp": 1666609676
    },
    "type": "newMessage"
}
```

Use the `userId` value from the `payload["from"]` field and add it to your `whitelisted-users` config option.