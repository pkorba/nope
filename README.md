# Nope Bot

A maubot for Matrix messaging that redacts it's own messages.

![bot_nope](https://github.com/user-attachments/assets/e600ba59-c834-44ee-8dc4-20a2fe273ee7)


## Usage

Reply to the bot's message that you want to redact with `[p]nope`  
It only works with messages that are direct reply to your own command.

## Notes

It only works with plugins that send bot's messages as `reply`, not as `response`. It's by design, to prevent users from deleting bot's messages that were not intended for them.
