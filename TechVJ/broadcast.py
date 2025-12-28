from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked
import asyncio

from config import ADMINS, WAITING_TIME
from database.db import db


@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast_handler(client, message):

    if not message.reply_to_message:
        return await message.reply_text(
            "❌ Reply to a message with /broadcast"
        )

    sent = 0
    failed = 0

    users = await db.get_all_users()

    async for user in users:
        try:
            await message.reply_to_message.copy(
                chat_id=user["id"]
            )
            sent += 1
            await asyncio.sleep(WAITING_TIME)

        except UserIsBlocked:
            await db.delete_user(user["id"])
            failed += 1

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception:
            failed += 1

    await message.reply_text(
        f"📢 Broadcast Completed\n\n"
        f"✅ Sent: {sent}\n"
        f"❌ Failed: {failed}"
    )
