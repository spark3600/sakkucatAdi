#By @sakku_cute
#Don't use the plugin to make fun and be aware no one should fall in trouble...
#Kangers keep credit else u are kids....

from userbot import catub

from userbot.utils import admin_cmd

plugin_category = "extra"


@catub.cat_cmd(
    pattern="sdes ?(.*)",
    command=("sdes", plugin_category),
    info={
        "header": " Save self destruct pic",
        "usage": [
            "{tr}sdes",
        ],
    },
)
async def sakshi(event):
    if not event.is_reply:
        return await event.edit("Reply to a self distructing pic !.!.!")
    k = await event.get_reply_message()
    pic = await k.download_media()
    await bot.send_file(
        event.chat_id,
        pic,
        caption=f"""
  Sed! Your pic is saved
  """,
    )
    await event.delete()
