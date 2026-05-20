import os
import json
from pyrogram import filters
from pyrogram.types import Message
from app import app

# JALUR ABSOLUT PREMIUM (Style Benxx Project)
from modules.styles import result_box, error, success, bold, mono, info

print("👥 System: Clones & Reverts Module loading...")

BACKUP_DIR = "profile_backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

# 🛡️ ID DEVELOPER UTAMA (BENXX) - TIDAK BOLEH DIKLONING OLEH SIAPAPUN
DEV_ID = 7687084316

@app.on_message(filters.text, group=-1)
async def jalur_clones(client, message: Message):
    text = message.text
    if not text:
        return

    # Ambil ID pengirim pesan dengan aman
    sender_id = message.from_user.id if message.from_user else None
    if not sender_id:
        return

    # Ambil info akun userbot yang sedang berjalan
    me = await client.get_me()

    # --- PROSES CLONES ---
    if text.startswith(".clones"):
        # KEAMANAN 1: Cek apakah yang ngetik itu beneran pemilik ubot ini
        if sender_id != me.id:
            return await message.reply(info(f"Yeee mau ngerjain ya? Perintah ini cuma bisa dikendalikan oleh {bold('Owner')}! 😜", title="NOT ALLOWED"))

        await message.edit(bold("🔄 Memproses..."))
        
        user_target = None
        cmd_args = text.split()

        if message.reply_to_message and message.reply_to_message.from_user:
            user_target = message.reply_to_message.from_user
        elif len(cmd_args) > 1:
            try:
                user_target = await client.get_users(cmd_args[1])
            except Exception as e:
                return await message.edit(error(f"Target gagal diambil: {e}"))

        if not user_target:
            return await message.edit(error("Reply orangnya atau ketik `.clones @username` Ben!"))

        # 👑 KEAMANAN 2: PROTEKSI AKUN DEVELOPER (BENXX ANTI-CLONE)
        if user_target.id == DEV_ID:
            return await message.edit(error(
                f"Peringatan: Akun {bold('Developer')} dilindungi! Tidak bisa dikloning oleh siapapun.", 
                title="PROTECTED ACCOUNT"
            ))

        try:
            backup_file = os.path.join(BACKUP_DIR, f"{me.id}.json")

            # Ambil backup profil asli ubot kalau belum ada
            if not os.path.exists(backup_file):
                my_full = await client.get_chat(me.id)
                my_photo = None
                if me.photo:
                    try:
                        my_photo = await client.download_media(me.photo.big_file_id, file_name=os.path.join(BACKUP_DIR, f"{me.id}_ori.jpg"))
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

            # Eksekusi ngebajak profil target
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
                    if os.path.exists(target_photo):
                        os.remove(target_photo)
                except Exception as e:
                    return await message.edit(error(f"Nama/Bio sukses, tapi foto gagal: {e}"))

            res_text = f"👤 {bold('Kloning Ke:')} {user_target.first_name}\n📌 Ketik `.reverts` buat balik semula."
            await message.edit(result_box("CLONING SUCCESS", res_text, icon="🎭"))

        except Exception as e:
            await message.edit(error(str(e), title="EROR SISTEM"))

    # --- PROSES REVERTS ---
    elif text.startswith(".reverts"):
        if sender_id != me.id:
            return

        await message.edit(bold("🔄 Mengembalikan..."))
        backup_file = os.path.join(BACKUP_DIR, f"{me.id}.json")

        if not os.path.exists(backup_file):
            return await message.edit(error("Data backup asli gak ketemu."))

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
                try:
                    await client.set_profile_photo(photo=photo_path)
                    if os.path.exists(photo_path):
                        os.remove(photo_path)
                except:
                    pass

            if os.path.exists(backup_file):
                os.remove(backup_file)

            await message.edit(success("Profil userbot sudah kembali normal", title="REVERT SUCCESS"))

        except Exception as e:
            await message.edit(error(str(e), title="EROR REVERT"))

print("✅ System: Clones & Reverts Module Ready with Dev Protection!")
