from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from app import app
import asyncio
from .styles import status_report, error, bold, mono

@app.on_message(filters.command("gcast", ".") & filters.me)
async def gcast_cmd(client, message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.edit(error("Berikan pesan atau reply pesan untuk Gcast!"))

    msg = message.reply_to_message if message.reply_to_message else message.text.split(None, 1)[1]
    await message.edit(bold(" Memulai Global Broadcast..."))
    
    done, failed = 0, 0
    
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            try:
                if message.reply_to_message:
                    await msg.copy(dialog.chat.id)
                else:
                    await client.send_message(dialog.chat.id, msg)
                
                done += 1
                await asyncio.sleep(0.3) 
            except FloodWait as e:
                await asyncio.sleep(e.value) # Handle limit otomatis
                if message.reply_to_message: await msg.copy(dialog.chat.id)
                else: await client.send_message(dialog.chat.id, msg)
                done += 1
            except Exception:
                failed += 1

    await message.edit(status_report(done, failed, process_name="GCAST"))
