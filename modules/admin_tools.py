import asyncio
from pyrogram import filters, enums
from pyrogram.types import Message, ChatPrivileges
from app import app

# Fallback styles jika modul styles.py tidak ada
try:
    from .styles import result_box, error, success, bold, mono, italic, info
except ImportError:
    def result_box(title, content, icon="📊"):
        return f"{icon} **{title}**\n━━━━━━━━━━━━━━━━━━━━━━━\n{content}"
    def error(text, title="GAGAL"):
        return f"❌ **{title}**\n━━━━━━━━━━━━━━━━━━━━━━━\n`{text}`"
    def success(text, title="BERHASIL"):
        return f"✅ **{title}**\n━━━━━━━━━━━━━━━━━━━━━━━\n{text}"
    def info(text, title="INFO"):
        return f"ℹ️ **{title}**\n━━━━━━━━━━━━━━━━━━━━━━━\n{text}"
    def bold(text): return f"**{text}**"
    def mono(text): return f"`{text}`"
    def italic(text): return f"__{text}__"

@app.on_message(filters.command("adminlist", ".") & filters.me)
async def adminlist_handler(client, message: Message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit(error("Fitur ini khusus untuk Grup!"))
    
    status = await message.edit(info("Mengambil daftar admin..."))
    try:
        owner = ""
        admins = []
        async for m in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            name = m.user.first_name if not m.user.is_deleted else "Akun Terhapus"
            user_link = f"[{name}](tg://user?id={m.user.id})"
            if m.status == enums.ChatMemberStatus.OWNER:
                owner = f"👑 {bold('Owner:')} {user_link}\n"
            else:
                admins.append(f"🔹 {user_link}")
        
        content = f"{owner}\n" + "\n".join(admins)
        await status.edit(result_box(f"ADMIN LIST: {message.chat.title[:15]}", content, icon="🛡️"))
    except Exception as e:
        await status.edit(error(str(e)))

@app.on_message(filters.command(["ban", "kick", "unban", "promote", "demote"], ".") & filters.me)
async def member_mod_handler(client, message: Message):
    cmd = message.command[0]
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit(error("Gunakan fitur ini di dalam Grup!"))

    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]
    
    if not user_id:
        return await message.edit(error(f"Gunakan: {mono(f'.{cmd} [reply/id]')}"))

    status = await message.edit(info(f"Memproses {cmd}..."))
    try:
        if cmd == "ban":
            await client.ban_chat_member(message.chat.id, user_id)
            await status.edit(success(f"User {mono(str(user_id))} telah di-{bold('Banned')}."))
        elif cmd == "kick":
            await client.ban_chat_member(message.chat.id, user_id)
            await client.unban_chat_member(message.chat.id, user_id)
            await status.edit(success(f"User {mono(str(user_id))} telah di-{bold('Kick')}."))
        elif cmd == "unban":
            await client.unban_chat_member(message.chat.id, user_id)
            await status.edit(success(f"User {mono(str(user_id))} dapat bergabung lagi."))
        elif cmd == "promote":
            await client.promote_chat_member(
                message.chat.id,
                user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_invite_users=True,
                    can_restrict_members=True,
                    can_pin_messages=True
                )
            )
            await status.edit(success("User dipromosikan menjadi Admin!"))
        elif cmd == "demote":
            await client.promote_chat_member(
                message.chat.id,
                user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_invite_users=False,
                    can_restrict_members=False,
                    can_pin_messages=False
                )
            )
            await status.edit(success("Hak admin telah dicabut."))
    except Exception as e:
        await status.edit(error(str(e)))

@app.on_message(filters.command(["purge", "del"], ".") & filters.me)
async def cleaner_handler(client, message: Message):
    cmd = message.command[0]
    if cmd == "del":
        if message.reply_to_message:
            await message.reply_to_message.delete()
            await message.delete()
        else:
            await message.edit(error("Reply ke pesan target!"))
    elif cmd == "purge":
        if not message.reply_to_message:
            return await message.edit(error("Reply ke pesan awal untuk purge!"))
        msg_ids = list(range(message.reply_to_message.id, message.id))
        if not msg_ids:
            return await message.edit(error("Tidak ada pesan untuk dihapus."))
        await message.edit(info(f"Menghapus {len(msg_ids)} pesan..."))
        await client.delete_messages(message.chat.id, msg_ids)
        final = await message.edit(success(f"Bersih {len(msg_ids)} pesan."))
        await asyncio.sleep(2)
        await final.delete()
