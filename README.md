# Nope Bot

A maubot plugin that redacts its own messages.

![bot_nope](https://github.com/user-attachments/assets/e600ba59-c834-44ee-8dc4-20a2fe273ee7)


## Usage

Reply to the bot's message that you want to redact with `!nope` or react to it with ❌ emoji.  
It only works with messages that are direct reply to your own command or reply to a command in general if you have permission to delete messages of other users.

## Notes

It only works with plugins that send bot's messages as `reply`, not as `response`. It's by design, to prevent users from deleting bot's messages that were not intended for them.
