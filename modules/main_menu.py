from app import app
from pyrogram import filters
from pyrogram.types import Message
import os
import time

# Import styles Benxx Project
from modules.styles import bold, mono, italic, border, link

print("⚙️ System: Professional Help Module loading...")

@app.on_message(filters.command("comandlist", ["."]) & filters.me, group=-1)
async def help_pro_handler(client, message: Message):
    # Penanda di log Termux
    start_time = time.time()
    
    # Hitung jumlah modul yang terpasang
    try:
        modules_list = [f for f in os.listdir("modules") if f.endswith('.py') and not f.startswith('__')]
        mod_count = len(modules_list)
    except Exception:
        mod_count = "N/A"

    # --- KONSTRUKSI VISUAL ---
    header = (
        f"📋 {bold('USERBOT COMMANDS')}\n"
        f" {italic(f'Status: {mod_count} Modules Loaded')}\n"
        f"{border('━', 23)}\n\n"
    )

    downloader = (
        f"📥 {bold('DOWNLOADER')}\n"
        f"• {mono('.yt')}  — {italic('Video (720p)')}\n"
        f"• {mono('.yta')} — {italic('Audio (MP3)')}\n\n"
    )

    broadcast = (
        f"📢 {bold('BROADCAST')}\n"
        f"• {mono('.gcast')} — {italic('Global Broadcast')}\n"
        f"• {mono('.bl')}    — {italic('Add Blacklist')}\n"
        f"• {mono('.unbl')}  — {italic('Remove Blacklist')}\n\n"
    )

    admin = (
        f"🛡️ {bold('ADMIN & GRUP')}\n"
        f"• {mono('.adminlist')} — {italic('Daftar semua admin grup')}\n"
        f"• {mono('.info')}      — {italic('Group Detail')}\n"
        f"• {mono('.ban')}       | {mono('.kick')} | {mono('.unban')}\n"
        f"• {mono('.promote')}   — {italic('Jadikan admin')}\n"
        f"• {mono('.demote')}    — {italic('Cabut admin')}\n"
        f"• {mono('.purge')}     | {mono('.del')}\n\n"
    )

    osint = (
        f"🔍 {bold('OSINT & TRACKER')}\n"
        f"• {mono('.ip')}    — {italic('IP Tracker')}\n"
        f"• {mono('.ipsakti')} — {italic('Advanced IP')}\n"
        f"• {mono('.nomer')}  — {italic('Check Operator')}\n"
        f"• {mono('.finduser')} — {italic('Social Search')}\n\n"
    )

    system = (
        f"📊 {bold('SYSTEM & INFO')}\n"
        f"• {mono('.ping')}  | {mono('.alive')} | {mono('.id')}\n"
        f"• {mono('.stats')} — {italic('Performance')}\n"
        f"• {mono('.sysinfo')} — {italic('Server Spec')}\n\n"
    )

    creative = (
        f"🎨 {bold('CREATIVE')}\n"
        f"• {mono('.stiker')} — {italic('Image to Sticker (WebP)')}\n"
        f"• {mono('.penyok')} — {italic('Face Distortion')}\n"
        f"• {mono('.bulge')} [strength] - {italic('Efek cembung ekstrim (default 1.5)')}\n"
        f"   Contoh: {mono('.bulge 2.5')} untuk efek parah, reply ke foto/stiker\n"
        f"• {mono('.emoji')}  — {italic('Text to Emoji')}\n"
        f"• {mono('.whois')}  — {italic('User Profiling')}\n\n"
    )

    footer = (
        f"{border('━', 23)}\n"
        f"👨‍💻 {bold('Dev:')} {link('Benxx Project', 'https://t.me/Bleszh')}\n"
        f"⏱️ {italic(f'Response: {round(time.time() - start_time, 3)}s')}"
    )

    final_text = header + downloader + broadcast + admin + osint + system + creative + footer

    try:
        await message.edit(final_text, disable_web_page_preview=True)
        print(f"✅ [HELP] Sent successfully to {message.chat.id}")
    except Exception as e:
        print(f"⚠️ [HELP] Edit failed, sending new message: {e}")
        await client.send_message(message.chat.id, final_text, disable_web_page_preview=True)

print("✅ System: Help Module Ready!")
