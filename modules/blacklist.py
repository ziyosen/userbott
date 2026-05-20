import json
import os
import asyncio
from datetime import datetime
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message
from app import app


from modules.styles import success, error, info, result_box, bold, mono

print("System: Blacklist & Gcast Module loading...")

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

@app.on_message(filters.command("bl", ["."]) & filters.me, group=-1)
async def add_blacklist(client, message: Message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await message.edit(error("🚫 Perintah ini hanya bisa di dalam Grup!"))
    
    bl = get_blacklist()
    chat_id = message.chat.id
    chat_title = message.chat.title or "Grup Tanpa Nama"
    
    if chat_id in bl["groups"]:
        return await message.edit(info(f"📌 Grup **{chat_title}** sudah ada di blacklist.", title="SUDAH ADA"))
    
    bl["groups"].append(chat_id)
    save_blacklist(bl)
    await message.edit(success(f"✅ **{chat_title}**\nBerhasil ditambahkan ke blacklist.", title="BLACKLIST BERHASIL"))

@app.on_message(filters.command("unbl", ["."]) & filters.me, group=-1)
async def del_blacklist(client, message: Message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await message.edit(error("🚫 Perintah ini hanya bisa di dalam Grup!"))
    
    bl = get_blacklist()
    chat_id = message.chat.id
    chat_title = message.chat.title or "Grup Tanpa Nama"
    
    if chat_id not in bl["groups"]:
        return await message.edit(error(f"❌ Grup **{chat_title}** tidak ditemukan di blacklist."))
    
    bl["groups"].remove(chat_id)
    save_blacklist(bl)
    await message.edit(success(f"✅ **{chat_title}**\nBerhasil dihapus dari blacklist.", title="UNBLACKLIST BERHASIL"))

@app.on_message(filters.command("listbl", ["."]) & filters.me, group=-1)
async def list_blacklist(client, message: Message):
    bl = get_blacklist()
    if not bl["groups"]:
        return await message.edit(info("📭 Belum ada grup yang di-blacklist.\nGunakan `.bl` di grup target.", title="KOSONG"))
    
    text = ""
    for i, gid in enumerate(bl["groups"], 1):
        try:
            chat = await client.get_chat(gid)
            name = chat.title or "Grup Tidak Dikenal"
            text += f"{i}. **{name}**\n   `{gid}`\n\n"
        except:
            text += f"{i}. `{gid}` (Grup tidak dapat diakses)\n\n"
    
    result = f"📋 **DAFTAR BLACKLIST**\n━━━━━━━━━━━━━━━━━━━━━━━\n{text}━━━━━━━━━━━━━━━━━━━━━━━\n📌 **Total:** `{len(bl['groups'])}` grup"
    await message.edit(result)

@app.on_message(filters.command("gcast", ["."]) & filters.me, group=-1)
async def gcast_command(client, message: Message):
    # Cek apakah ada target broadcast (bisa berupa teks langsung atau reply media/teks)
    has_reply = message.reply_to_message
    
    if not has_reply and len(message.command) < 2:
        return await message.edit(error(
            " **Cara penggunaan GCAST:**\n"
            "1️⃣ Reply pesan (Teks/Foto/Video/Stiker) + `.gcast`\n"
            "2️⃣ `.gcast [teks]`\n\n"
            "Contoh: `.gcast Halo semua!`"
        ))
    
    status = await message.edit("**Broadcast dimulai...**\n⏳ Mohon tunggu sebentar...")
    sent, failed, skipped = 0, 0, 0
    blacklist = get_blacklist()["groups"]
    start = datetime.now()
    
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            # Skip jika grup masuk daftar blacklist Benxx
            if dialog.chat.id in blacklist:
                skipped += 1
                continue
            try:
                # 🚀 FITUR CANGGIH: Jika reply, copy pesan aslinya (Bisa Kirim Foto/Video/Stiker/Teks)
                if has_reply:
                    await has_reply.copy(dialog.chat.id)
                else:
                    # Jika cuma teks langsung bawaan perintah
                    broadcast_text = message.text.split(None, 1)[1]
                    await client.send_message(dialog.chat.id, broadcast_text)
                
                sent += 1
                await asyncio.sleep(0.7) # Delay aman anti-floodwaits / limit Telegram
            except Exception:
                failed += 1
    
    elapsed = (datetime.now() - start).seconds
    result = (
        f"📊 {bold('LAPORAN BROADCAST')}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ {bold('Berhasil:')} {mono(f'{sent} grup')}\n"
        f"❌ {bold('Gagal:')} {mono(f'{failed} grup')}\n"
        f"🚫 {bold('Di-skip:')} {mono(f'{skipped} grup')}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 {bold('Total Diproses:')} {mono(sent+failed+skipped)}\n"
        f"⏱️ {bold('Waktu Tempuh:')} {mono(f'{elapsed} detik')}"
    )
    await status.edit(result_box("BROADCAST RESULT", result, icon="💠"))

print("✅ System: Blacklist & Gcast Module Ready!")
