# By @sakku
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import catub

from ..helpers.utils import reply_id

plugin_category = "tools"


@catub.cat_cmd(
    pattern="limit$",
    command=("limit", plugin_category),
    info={
        "header": "Check the limit of an account",
        "usage": [
            "{tr}limit",
        ],
    },
)
async def _(event):
    "Check account limit if any"
    text = "/start"
    reply_to_id = await reply_id(event)
    await event.edit("`Processing ...`")
    chat = "@SpamBot"
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(text)
            message = await conv.get_response(1)
            await event.client.send_message(
                event.chat_id, message, reply_to=reply_to_id
            )
            await event.delete()
        except YouBlockedUserError:
            await event.edit("**Error:**\nUnblock @SpamBot and try again")
