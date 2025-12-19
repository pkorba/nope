from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.types import EventType, ReactionEvent, BaseRoomEvent
from typing import Tuple


class NopeBot(Plugin):
    @command.new("nope", help="Remove the bot's response to your own message")
    async def nope(self, evt: MessageEvent) -> None:
        """
        Remove the bot's response to your own message by using !nope command in reply to bot's message.
        :param evt: message event
        """
        await evt.mark_read()
        bot_message_id = evt.content.get_reply_to()
        if bot_message_id is None:
            # Message that user wants to delete is not direct reply to his previous command
            await evt.respond("> **Usage:**  \n"
                              "> Reply to the bot's message that you want to remove with `!nope` or react to it with ❌ emoji.  \n"
                              "> It only works with messages that are direct reply to your own command "
                              "or reply to a command in general if you have permission to delete messages of other users in this room.")
            return
        bot_message: MessageEvent = await self.client.get_event(room_id=evt.room_id, event_id=bot_message_id)
        await self.try_redact(evt, bot_message)

    @command.passive(regex="❌", field=lambda evt: evt.content.relates_to.key, event_type=EventType.REACTION, msgtypes=[])
    async def nope_react(self, evt: ReactionEvent, key: Tuple[str]) -> None:
        """
        Remove the bot's response to your own message by reacting with ❌ emoji to the bot's message.
        :param evt: message event
        """
        bot_message_id = evt.content.relates_to.event_id
        bot_message = await self.client.get_event(room_id=evt.room_id, event_id=bot_message_id)
        await self.try_redact(evt, bot_message)

    async def try_redact(self, evt: BaseRoomEvent, bot_message: MessageEvent) -> None:
        """
        Remove message if user has sufficient permissions
        :param evt: event initiating deletion process
        :param bot_message: message to be deleted
        """
        if bot_message.sender != self.client.mxid:
            return
        user_message_id = bot_message.content.get_reply_to()
        if user_message_id is None:
            # Bot's response is not a reply so it wasn't initiated by the caller. Ignore silently
            return
        user_message = await self.client.get_event(room_id=evt.room_id, event_id=user_message_id)
        user_level = 0
        power_levels = None
        try:
            power_levels = await self.client.get_state_event(evt.room_id, EventType.ROOM_POWER_LEVELS)
            # Create event contains information about the room owner in rooms v12
            # Their power level cannot be determined from PowerLevelStateEventContent alone
            state_events = await self.client.get_state(evt.room_id)
            create_event = next((s_evt for s_evt in state_events if s_evt.type == EventType.ROOM_CREATE), None)
            user_level = power_levels.get_user_level(evt.sender, create_event)
        except Exception as e:
            self.log.error(f"Failed to check user power level: {e}")

        if user_message.sender == evt.sender or user_level and power_levels and user_level >= power_levels.redact:
            await self.client.redact(room_id=evt.room_id, event_id=bot_message.event_id, reason=f"Message redacted with !nope by {evt.sender}")
