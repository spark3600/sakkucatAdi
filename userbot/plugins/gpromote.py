## By @sakku_cute

import asyncio
import random
from datetime import datetime

from telethon import events
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
)
from telethon.utils import get_display_name

from userbot import catub

from ..core.managers import eod, eor
from ..helpers.utils import _format
from ..helpers.utils.events import get_user_from_event
from ..sql_helper import gban_sql_helper
from ..sql_helper.globals import gvarstatus
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID, admin_groups, gban_pic 

plugin_category = "admin"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


async def get_full_user(event):
    args = event.pattern_match.group(1).split(":", 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await eor(event, "Need a user to do this...")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await eor(event, f"**ERROR !!**\n\n`{str(err)}`")
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj
    
    
    @catub.cat_cmd(
    pattern="gpromote(?:\s|$)([\s\S]*)",
    command=("gpromote", plugin_category),
    info={
        "header": "To promote user in every group where you are admin(have a right to promote).",
        "description": "Will promote the person in every group where you are admin(have a right to promote).",
        "usage": [
            "{tr}gpromote <username/reply/userid> <reason (optional)>",
        ],
    },
)
async def _(event):
    i = 0
    await event.get_sender()
    me = await event.client.get_me()
    event = await eor(event, "`Promoting globally...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await event.get_chat()
    if event.is_private:
        user = event.chat
        rank = event.pattern_match.group(1)
    else:
        event.chat.title
    try:
        user, rank = await get_full_user(event)
    except:
        pass
    if me == user:
        await event.edit("You can't promote yourself...")
        return
    try:
        if not rank:
            rank = "event"
    except:
        return await event.edit("**ERROR !!**")
    if user:
        telchanel = [
            d.entity.id
            for d in await event.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        rgt = ChatAdminRights(
            add_admins=True,
            invite_users=True,
            change_info=True,
            ban_users=True,
            delete_messages=True,
            pin_messages=True,
        )
        for x in telchanel:
            try:
                await event.client(EditAdminRequest(x, user, rgt, rank))
                i += 1
                await event.edit(f"**Promoting User in :**  `{i}` Chats...")
            except:
                pass
    else:
        await event.edit(f"**Reply to a user !!**")
    await event.edit(
        f"[{user.first_name}](tg://user?id={user.id}) **Was Promoted Globally In** `{i}` **Chats !!**"
    )
    await event.client.send_message(
        BOTLOG_CHATID,
        f"#GPROMOTE \n\n**Globally Promoted User :** [{user.first_name}](tg://user?id={user.id}) \n\n**Total Chats :** `{i}`",
    )


@catub.cat_cmd(
    pattern="gdemote(?:\s|$)([\s\S]*)",
    command=("gdemote", plugin_category),
    info={
        "header": "To demote user in that group where you promote person to admin.",
        "description": "Will demote the person in that group where you promote person to admin",
        "usage": [
            "{tr}gdemote <username/reply/userid> <reason (optional)>",
        ],
    },
)
async def _(event):
    i = 0
    await event.get_sender()
    me = await event.client.get_me()
    event = await eor(event, "`Demoting Globally...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    if event.is_private:
        user = event.chat
        rank = event.pattern_match.group(1)
    else:
        event.chat.title
    try:
        user, rank = await get_full_user(event)
    except:
        pass
    if me == user:
        await event.edit("You can't Demote yourself !!")
        return
    try:
        if not rank:
            rank = "event"
    except:
        return await event.edit("**ERROR !!**")
    if user:
        telchanel = [
            d.entity.id
            for d in await event.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        rgt = ChatAdminRights(
            add_admins=None,
            invite_users=None,
            change_info=None,
            ban_users=None,
            delete_messages=None,
            pin_messages=None,
        )
        for x in telchanel:
            try:
                await event.client(EditAdminRequest(x, user, rgt, rank))
                i += 1
                await event.edit(f"**Demoting Globally In Chats :** `{i}`")
            except:
                pass
    else:
        await event.edit(f"**Reply to a user !!**")
    await event.edit(
        f"[{user.first_name}](tg://user?id={user.id}) **Was Demoted Globally In** `{i}` **Chats !!**"
    )
    await event.client.send_message(
        BOTLOG_CHATID,
        f"#GDEMOTE \n\n**Globally Demoted :** [{user.first_name}](tg://user?id={user.id}) \n\n**Total Chats :** `{i}`",
    )

