import os
import json
from pyrogram import filters
from pyrogram.types import Message
from app import app

BACKUP_DIR = "profile_backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

# HAPUS filters.me biar akun mana aja bisa nge-trigger buat tes!
@app.on_message()
async def jalur_clones(client, message: Message):
    text = message.text
    if not text:
        return

    # --- PROSES CLONES ---
    if text.startswith(".clones"):
        await message.edit("🔄 **[Benxx Project] Memproses kloning profil...**")
        
        user_target = None
        cmd_args = text.split()

        if message.reply_to_message and message.reply_to_message.from_user:
            user_target = message.reply_to_message.from_user
        elif len(cmd_args) > 1:
            try:
                user_target = await client.get_users(cmd_args[1])
            except Exception as e:
                return await message.edit(f"❌ **Target gagal diambil:** {e}")

        if not user_target:
            return await message.edit("⚠️ **Gagal:** Reply orangnya atau ketik `.clones @username` Ben!")

        try:
            my_id = message.from_user.id
            backup_file = os.path.join(BACKUP_DIR, f"{my_id}.json")

            if not os.path.exists(backup_file):
                me = await client.get_me()
                my_full = await client.get_chat(me.id)
                my_photo = None
                if me.photo:
                    try:
                        my_photo = await client.download_media(me.photo.big_file_id, file_name=os.path.join(BACKUP_DIR, f"{my_id}_ori.jpg"))
                    except:
                        pass

                backup_data = {
                    "first_name": me.first_name or "",
                    "last_name": me.last_name or "",
                    "bio": my_full.bio or "",
                    "photo_path": my_photo
                }
                with open(backup_file, 'w') as f:
                    json.dump(backup_data, f)

            target_full = await client.get_chat(user_target.id)
            await client.update_profile(
                first_name=user_target.first_name or "",
                last_name=user_target.last_name or "",
                bio=target_full.bio or ""
            )

            if user_target.photo:
                try:
                    target_photo = await client.download_media(user_target.photo.big_file_id, file_name="temp_clones.jpg")
                    await client.set_profile_photo(photo=target_photo)
                    os.remove(target_photo)
                except Exception as e:
                    await message.edit(f"⚠️ Nama/Bio sukses, tapi foto gagal: {e}")
                    return

            await message.edit(f"✅ **Sukses Kloning!** Sekarang profil userbot lo berubah.\nKetik `.reverts` buat balik asli.")

        except Exception as e:
            await message.edit(f"💥 **Eror Sistem:** {str(e)}")

    # --- PROSES REVERTS ---
    elif text.startswith(".reverts"):
        await message.edit("🔄 **Mengembalikan profil asli...**")
        my_id = message.from_user.id
        backup_file = os.path.join(BACKUP_DIR, f"{my_id}.json")

        if not os.path.exists(backup_file):
            return await message.edit("❌ **Gagal:** Data backup asli gak ketemu.")

        try:
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)

            await client.update_profile(
                first_name=backup_data.get("first_name", ""),
                last_name=backup_data.get("last_name", ""),
                bio=backup_data.get("bio", "")
            )

            photo_path = backup_data.get("photo_path")
            if photo_path and os.path.exists(photo_path):
                await client.set_profile_photo(photo=photo_path)
                os.remove(photo_path)

            if os.path.exists(backup_file):
                os.remove(backup_file)

            await message.edit("✅ **Profil userbot sudah kembali normal!**")

        except Exception as e:
            await message.edit(f"❌ **Eror Revert:** {str(e)}")
