from app import app
from pyrogram import filters
import time
import os
import platform
from datetime import datetime
# Import styles milik Benxx
from .styles import result_box, bold, mono, italic, link

print("✅ Utils module loaded!")

# Ambil waktu start bot
START_TIME = datetime.now()

def get_uptime():
    """Fungsi hitung uptime yang rapi."""
    delta = datetime.now() - START_TIME
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    
    res = ""
    if days > 0: res += f"{days}d "
    if hours > 0: res += f"{hours}h "
    if minutes > 0: res += f"{minutes}m "
    res += f"{seconds}s"
    return res

@app.on_message(filters.command("ping", ".") & filters.me)
async def ping_command(client, message):
    start = time.time()
    # Edit awal pakai style italic biar estetik
    await message.edit(italic("📡 Pinging..."))
    
    end = time.time()
    ping_ms = round((end - start) * 1000)
    
    # Hasil ping dibungkus result_box
    content = f"🚀 {bold('Pong!!')}\n⏱️ {bold('Latency:')} {mono(f'{ping_ms}ms')}\n🌐 {bold('Status:')} {mono('Online')}"
    await message.edit(result_box("CONNECTION SPEED", content, icon="⚡"))

@app.on_message(filters.command("alive", ".") & filters.me)
async def alive_command(client, message):
    # Hitung jumlah file .py di folder modules
    try:
        mod_count = len([f for f in os.listdir("modules") if f.endswith('.py')])
    except:
        mod_count = "Unknown"
        
    dev_link = link("Benxx", "https://t.me/Bleszh") # Pakai username lo
    
    content = (
        f"👤 {bold('User:')} {client.me.first_name}\n"
        f"👨‍💻 {bold('Owner:')} {dev_link}\n"
        f"⏱️ {bold('Uptime:')} {mono(get_uptime())}\n"
        f"📦 {bold('Modules:')} {mono(f'{mod_count} active')}\n"
        f"🛡️ {bold('Security:')} {mono('Protected')}"
    )
    
    # Pakai icon 🌟 buat tanda bot hidup
    await message.edit(result_box(" USERBOT ACTIVE", content, icon="🌟"))

@app.on_message(filters.command("restart", ".") & filters.me)
async def restart_bot(client, message):
    await message.edit(result_box("RESTARTING", f"🔄 {italic('Bot sedang direstart, tunggu sebentar...')}", icon="⚙️"))
    # Bot bakal direstart otomatis sama PM2 kalau prosesnya mati
    os._exit(0)
