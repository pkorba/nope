from maubot import Plugin, MessageEvent
from maubot.handlers import command


class NopeBot(Plugin):
    @command.new("nope", help="Remove the bot's response to your own message")
    async def nope(self, evt: MessageEvent) -> None:
        await evt.mark_read()
        user_id = evt.sender
        bot_message_id = evt.content.get_reply_to()
        if bot_message_id is None:
            # Message that user wants to delete is not direct reply to his previous command
            await evt.respond("**Usage:**  \n"
                              "Reply to the bot's message that you want to redact with !nope  \n"
                              "It only works with messages that are direct reply to your own command.")
            return
        bot_message: MessageEvent = await self.client.get_event(room_id=evt.room_id, event_id=bot_message_id)
        if bot_message.sender != self.client.mxid:
            return
        user_message_id = bot_message.content.get_reply_to()
        if user_message_id is None:
            # Bot's response is not a reply so it wasn't initiated by the caller. Ignore silently
            return
        user_message = await self.client.get_event(room_id=evt.room_id, event_id=user_message_id)
        if user_message.sender == user_id:
            await self.client.redact(room_id=evt.room_id, event_id=bot_message_id, reason=f"Message redacted with !nope by {user_id}")
