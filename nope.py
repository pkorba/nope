from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.types import EventType, ReactionEvent
from typing import Tuple


class NopeBot(Plugin):
    @command.new("nope", help="Remove the bot's response to your own message")
    async def nope(self, evt: MessageEvent) -> None:
        """
        Remove the bot's response to your own message by using !nope command in reply to bot's message.
        :param evt: message event
        """
        await evt.mark_read()
        user_id = evt.sender
        bot_message_id = evt.content.get_reply_to()
        if bot_message_id is None:
            # Message that user wants to delete is not direct reply to his previous command
            await evt.respond("> **Usage:**  \n"
                              "> Reply to the bot's message that you want to remove with `!nope` or react to it with ❌ emoji.  \n"
                              "> It only works with messages that are direct reply to your own command "
                              "or if you have permission to delete others messages in this room.")
            return
        bot_message: MessageEvent = await self.client.get_event(room_id=evt.room_id, event_id=bot_message_id)
        if bot_message.sender != self.client.mxid:
            return
        user_message_id = bot_message.content.get_reply_to()
        if user_message_id is None:
            # Bot's response is not a reply so it wasn't initiated by the caller. Ignore silently
            return
        user_message = await self.client.get_event(room_id=evt.room_id, event_id=user_message_id)
        try:
            power_levels = await self.client.get_state_event(evt.room_id, EventType.ROOM_POWER_LEVELS)
            user_level = power_levels.get_user_level(user_id)
        except Exception as e:
            self.log.error(f"Failed to check user power level: {e}")

        if user_message.sender == user_id or user_level and user_level >= power_levels.redact:
            await self.client.redact(room_id=evt.room_id, event_id=bot_message_id, reason=f"Message redacted with !nope by {user_id}")

    @command.passive(regex="❌", field=lambda evt: evt.content.relates_to.key, event_type=EventType.REACTION, msgtypes=[])
    async def nope_react(self, evt: ReactionEvent, key: Tuple[str]) -> None:
        """
        Remove the bot's response to your own message by reacting with ❌ emoji to the bot's message.
        :param evt: message event
        """
        user_id = evt.sender
        bot_message_id = evt.content.relates_to.event_id
        bot_message  = await self.client.get_event(room_id=evt.room_id, event_id=bot_message_id)
        if bot_message.sender != self.client.mxid:
            return
        user_message_id = bot_message.content.get_reply_to()
        if user_message_id is None:
            # Bot's response is not a reply so it wasn't initiated by the caller. Ignore silently
            return
        user_message = await self.client.get_event(room_id=evt.room_id, event_id=user_message_id)
        try:
            power_levels = await self.client.get_state_event(evt.room_id, EventType.ROOM_POWER_LEVELS)
            user_level = power_levels.get_user_level(user_id)
        except Exception as e:
            self.log.error(f"Failed to check user power level: {e}")

        if user_message.sender == user_id or user_level and user_level >= power_levels.redact:
            await self.client.redact(room_id=evt.room_id, event_id=bot_message_id, reason=f"Message redacted with !nope by {user_id}")