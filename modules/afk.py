import json
import os
import time
from app import app
from pyrogram import filters
from pyrogram.types import Message
# Import styles milik Benxx Project
from .styles import result_box, mono, bold, italic

# ========== DATABASE LOGIC ==========
AFK_FILE = "data/afk.json"

def get_afk_data():
    """Ambil data AFK dari file JSON."""
    if not os.path.exists(AFK_FILE):
        return {"is_afk": False, "reason": "", "time": 0, "media": None}
    try:
        with open(AFK_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"is_afk": False, "reason": "", "time": 0, "media": None}

def set_afk_data(status, reason="", media=None):
    """Simpan data AFK ke file JSON."""
    os.makedirs(os.path.dirname(AFK_FILE), exist_ok=True)
    data = {
        "is_afk": status, 
        "reason": reason, 
        "time": time.time() if status else 0,
        "media": media
    }
    with open(AFK_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ========== FUNGSI BANTU ==========
def get_media_info(msg: Message):
    """Ekstrak file_id dan tipe media."""
    for attr in ["sticker", "photo", "animation", "video", "voice", "audio"]:
        media = getattr(msg, attr)
        if media:
            return (media.file_id, attr)
    return None

async def send_afk_message(client, chat_id, text, media_info):
    """Kirim notifikasi AFK dengan gaya styles.py"""
    if not media_info:
        return await client.send_message(chat_id, text)
    
    file_id, media_type = media_info
    method = getattr(client, f"send_{media_type}")
    if media_type == "sticker":
        return await method(chat_id, file_id)
    else:
        return await method(chat_id, file_id, caption=text)

def format_duration(start_time):
    """Format waktu biar estetik."""
    dur = int(time.time() - start_time)
    if dur < 60: return f"{dur} detik"
    if dur < 3600: return f"{dur // 60} menit {dur % 60} detik"
    return f"{dur // 3600} jam {(dur % 3600) // 60} menit"

# ========== PERINTAH .afk ==========
@app.on_message(filters.command("afk", ".") & filters.me)
async def set_afk(client, message: Message):
    reason = " ".join(message.command[1:]) if len(message.command) > 1 else "Mode Bersemedi"
    media_info = get_media_info(message.reply_to_message) if message.reply_to_message else None
    
    # Simpan ke JSON Database
    set_afk_data(True, reason, media_info)
    
    await message.delete()
    pesan = f"📝 Alasan: {mono(reason)}"
    if media_info: pesan += "\n📎 Media: Tersimpan"
    
    await client.send_message(
        message.chat.id, 
        result_box("AFK DIAKTIFKAN", pesan, icon="🔴")
    )

# ========== AUTO OFF SAAT OWNER CHAT ==========
@app.on_message(filters.me & ~filters.command("afk", "."))
async def auto_deactivate_afk(client, message: Message):
    afk = get_afk_data()
    if not afk["is_afk"]: return
    
    dur_str = format_duration(afk["time"])
    set_afk_data(False) # Matikan di JSON
    
    await client.send_message(
        message.chat.id,
        result_box("KEMBALI ONLINE", f"⏱ Berhasil kembali setelah: {mono(dur_str)}", icon="✅")
    )

# ========== AUTO REPLY (PM / MENTION / REPLY) ==========
@app.on_message(filters.incoming & ~filters.me & (filters.private | filters.mentioned | filters.reply) & ~filters.bot)
async def auto_reply_afk(client, message: Message):
    afk = get_afk_data()
    if not afk["is_afk"]: return

    me = await client.get_me()
    is_reply_to_me = message.reply_to_message and message.reply_to_message.from_user.id == me.id
    
    if message.chat.type != "private" and not (message.mentioned or is_reply_to_me):
        return

    dur_str = format_duration(afk["time"])
    info_afk = f"⏱ {bold('Sejak:')} {mono(dur_str)} yang lalu\n"
    info_afk += f"📝 {bold('Alasan:')} {afk['reason']}"
    
    reply_text = result_box(f"{me.first_name} SEDANG AFK", info_afk, icon="💤")
    await send_afk_message(client, message.chat.id, reply_text, afk["media"])
