# modules/blacklist.py
from app import app
from pyrogram import filters
from pyrogram.enums import ChatType
import json
import os
import asyncio
from datetime import datetime
from modules.styles import success, error, info, result_box, bold, mono

print("✅ Blacklist module loaded!")

BLACKLIST_FILE = "data/blacklist.json"
os.makedirs("data", exist_ok=True)

def get_blacklist():
    try:
        with open(BLACKLIST_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"groups": []}

def save_blacklist(data):
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.on_message(filters.command("bl", ".") & filters.me)
async def add_blacklist(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await message.reply(error("🚫 Perintah ini hanya bisa di dalam Grup!"))
    
    bl = get_blacklist()
    chat_id = message.chat.id
    chat_title = message.chat.title or "Grup Tanpa Nama"
    
    if chat_id in bl["groups"]:
        return await message.reply(info(f"📌 Grup **{chat_title}** sudah ada di blacklist.", title="SUDAH ADA"))
    
    bl["groups"].append(chat_id)
    save_blacklist(bl)
    await message.reply(success(f"✅ **{chat_title}**\nBerhasil ditambahkan ke blacklist.", title="BLACKLIST BERHASIL"))

@app.on_message(filters.command("unbl", ".") & filters.me)
async def del_blacklist(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await message.reply(error("🚫 Perintah ini hanya bisa di dalam Grup!"))
    
    bl = get_blacklist()
    chat_id = message.chat.id
    chat_title = message.chat.title or "Grup Tanpa Nama"
    
    if chat_id not in bl["groups"]:
        return await message.reply(error(f"❌ Grup **{chat_title}** tidak ditemukan di blacklist."))
    
    bl["groups"].remove(chat_id)
    save_blacklist(bl)
    await message.reply(success(f"✅ **{chat_title}**\nBerhasil dihapus dari blacklist.", title="UNBLACKLIST BERHASIL"))

@app.on_message(filters.command("listbl", ".") & filters.me)
async def list_blacklist(client, message):
    bl = get_blacklist()
    if not bl["groups"]:
        return await message.reply(info("📭 Belum ada grup yang di-blacklist.\nGunakan `.bl` di grup target.", title="KOSONG"))
    
    text = ""
    for i, gid in enumerate(bl["groups"], 1):
        try:
            chat = await client.get_chat(gid)
            name = chat.title or "Grup Tidak Dikenal"
            text += f"{i}. **{name}**\n   `{gid}`\n\n"
        except:
            text += f"{i}. `{gid}` (Grup tidak dapat diakses)\n\n"
    
    result = f"📋 **DAFTAR BLACKLIST**\n━━━━━━━━━━━━━━━━━━━━━━━\n{text}━━━━━━━━━━━━━━━━━━━━━━━\n📌 **Total:** `{len(bl['groups'])}` grup"
    await message.reply(result)

@app.on_message(filters.command("gcast", ".") & filters.me)
async def gcast_command(client, message):
    # Cek reply atau teks langsung
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    elif len(message.command) > 1:
        text = message.text.split(None, 1)[1]
    else:
        return await message.reply(error(
            " **Cara penggunaan GCAST:**\n"
            "1️⃣ Reply pesan + `.gcast`\n"
            "2️⃣ `.gcast [teks]`\n\n"
            "Contoh: `.gcast Halo semua!`"
        ))
    
    if not text or not text.strip():
        return await message.reply(error("⚠️ Pesan tidak boleh kosong!"))
    
    status = await message.reply("**Broadcast dimulai...**\n⏳ Mohon tunggu.")
    sent, failed, skipped = 0, 0, 0
    blacklist = get_blacklist()["groups"]
    start = datetime.now()
    
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            if dialog.chat.id in blacklist:
                skipped += 1
                continue
            try:
                await client.send_message(dialog.chat.id, text)
                sent += 1
                await asyncio.sleep(0.5)
            except Exception:
                failed += 1
    
    elapsed = (datetime.now() - start).seconds
    result = (
        f"📊 **LAPORAN BROADCAST**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ Berhasil: `{sent}` grup\n"
        f"❌ Gagal: `{failed}` grup\n"
        f"🚫 Di-skip: `{skipped}` grup\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 Total diproses: `{sent+failed+skipped}`\n"
        f"⏱️ Waktu: `{elapsed}` detik"
    )
    await status.edit(result)
