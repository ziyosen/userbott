from app import app
from pyrogram import filters
from pyrogram.types import Message
import time
import os

from modules.styles import result_box, bold, mono, italic, link

print("📡 System: Benxx Utils Module loading...")

START_TIME_EPOCH = time.time()

@app.on_message(filters.command("ping", ["."]) & filters.me, group=-1)
async def ping_command(client, message: Message):
    start = time.time()
    await message.edit(italic("📡 Pinging..."))
    
    end = time.time()
    ping_ms = round((end - start) * 1000)
    
    content = f"🚀 {bold('Pong!!')}\n⏱️ {bold('Latency:')} {mono(f'{ping_ms}ms')}\n🌐 {bold('Status:')} {mono('Online')}"
    await message.edit(result_box("CONNECTION SPEED", content, icon="⚡"))

@app.on_message(filters.command("alive", ["."]) & filters.me, group=-1)
async def alive_command(client, message: Message):
    # Hitung uptime sederhana pake time bawaan
    uptime_seconds = round(time.time() - START_TIME_EPOCH)
    hours, rem = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"

    try:
        mod_count = len([f for f in os.listdir("modules") if f.endswith('.py') and not f.startswith('__')])
    except:
        mod_count = "Unknown"
        
    dev_link = link("Benxx", "https://t.me/Bleszh")
    
    content = (
        f"👤 {bold('User:')} {client.me.first_name}\n"
        f"👨‍💻 {bold('Owner:')} {dev_link}\n"
        f"⏱️ {bold('Uptime:')} {mono(uptime_str)}\n"
        f"📦 {bold('Modules:')} {mono(f'{mod_count} active')}\n"
        f"🛡️ {bold('Security:')} {mono('Protected')}"
    )
    
    await message.edit(result_box("USERBOT ACTIVE", content, icon="🌟"))

print("✅ System: Utils Module Ready!")
