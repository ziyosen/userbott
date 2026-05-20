from app import app
from pyrogram import filters, enums
from pyrogram.types import Message

# Fallback styles (lengkap)
try:
    from .styles import result_box, error, success, bold, mono, info, italic
except ImportError:
    def result_box(title, content, icon="📊"):
        return f"{icon} **{title}**\n━━━━━━━━━━━━━━━━━━━━━━━━━\n{content}"
    def error(text, title="GAGAL"):
        return f"❌ **{title}**\n━━━━━━━━━━━━━━━━━━━━━━━━━\n`{text}`"
    def success(text, title="BERHASIL"):
        return f"✅ **{title}**\n━━━━━━━━━━━━━━━━━━━━━━━━━\n{text}"
    def info(text, title="INFO"):
        return f"ℹ️ **{title}**\n━━━━━━━━━━━━━━━━━━━━━━━━━\n{text}"
    def bold(text): return f"**{text}**"
    def mono(text): return f"`{text}`"
    def italic(text): return f"__{text}__"

@app.on_message(filters.command("id", ".") & filters.me)
async def id_handler(client, message: Message):
    if message.reply_to_message:
        target = message.reply_to_message.from_user or message.reply_to_message.sender_chat
        name = getattr(target, "first_name", getattr(target, "title", "Unknown"))
        content = f"👤 {bold('Name:')} {name}\n🆔 {bold('ID:')} {mono(target.id)}"
        await message.edit(result_box("USER ID", content))
    else:
        content = f"📌 {bold('Chat:')} {message.chat.title or 'Private'}\n🆔 {bold('ID:')} {mono(message.chat.id)}"
        await message.edit(result_box("CHAT ID", content))

@app.on_message(filters.command("whois", ".") & filters.me)
async def whois_handler(client, message: Message):
    # Tentukan target user
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]
    else:
        user_id = message.from_user.id

    status = await message.edit(info("Searching user data..."))
    try:
        user = await client.get_users(user_id)
        full = await client.get_chat(user.id)
        teks = (
            f"🆔 {bold('User ID:')} {mono(user.id)}\n"
            f"🌐 {bold('User:')} @{user.username or '-'}\n"
            f"📡 {bold('DC ID:')} {user.dc_id or '?'}\n"
            f"📝 {bold('Bio:')} {italic(full.bio or '-')}"
        )
        if user.photo:
            try:
                await client.send_photo(message.chat.id, user.photo.big_file_id, caption=result_box("WHOIS INFO", teks))
                await status.delete()
            except Exception:
                await status.edit(result_box("WHOIS INFO", teks))
        else:
            await status.edit(result_box("WHOIS INFO", teks))
    except Exception as e:
        await status.edit(error(str(e)))

@app.on_message(filters.command("info", ".") & filters.me)
async def info_handler(client, message: Message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit(error("Harus di dalam Grup!"))
    status = await message.edit(info("Loading group info..."))
    try:
        full = await client.get_chat(message.chat.id)
        count = await client.get_chat_members_count(message.chat.id)
        # Perbaikan: menggunakan atribut call_active dari objek Chat
        vc_status = 'Active' if getattr(full, 'call_active', False) else 'Off'
        teks = (
            f"🆔 {bold('Group ID:')} {mono(full.id)}\n"
            f"👥 {bold('Members:')} {count}\n"
            f"🌐 {bold('User:')} @{full.username or '-'}\n"
            f"🎤 {bold('VC:')} {vc_status}"
        )
        if full.photo:
            try:
                await client.send_photo(message.chat.id, full.photo.big_file_id, caption=result_box("GROUP INFO", teks))
                await status.delete()
            except Exception:
                await status.edit(result_box("GROUP INFO", teks))
        else:
            await status.edit(result_box("GROUP INFO", teks))
    except Exception as e:
        await status.edit(error(str(e)))
