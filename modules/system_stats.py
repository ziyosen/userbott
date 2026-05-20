import platform
import os
import time
import psutil
from datetime import datetime
from pyrogram import filters, enums
from app import app
# Import styles milik Benxx Project
from .styles import result_box, info, bold, mono, progress_bar, list_items

# Catat waktu mulai
START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    """Format detik ke waktu yang enak dibaca."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    res = ""
    if d > 0: res += f"{d}h "
    if h > 0: res += f"{h}h "
    if m > 0: res += f"{m}m "
    res += f"{s}s"
    return res

@app.on_message(filters.command("stats", ".") & filters.me)
async def bot_stats(client, message):
    status = await message.edit(bold("📊 Sedang menghitung data..."))
    
    # Counter cepat
    groups = 0
    channels = 0
    users = 0
    
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            groups += 1
        elif dialog.chat.type == enums.ChatType.CHANNEL:
            channels += 1
        elif dialog.chat.type == enums.ChatType.PRIVATE:
            users += 1

    uptime = get_readable_time(int(time.time() - START_TIME))
    
    res = (
        f"⏱ {bold('Uptime:')} {mono(uptime)}\n"
        f"👥 {bold('User:')} {mono(users)}\n"
        f"👥 {bold('Grup:')} {mono(groups)}\n"
        f"📢 {bold('Channel:')} {mono(channels)}"
    )
    
    await status.edit(result_box("STATISTIK AKUN", res, icon="📈"))

@app.on_message(filters.command("sysinfo", ".") & filters.me)
async def system_info(client, message):
    await message.edit(bold("📡 Mengambil data server..."))
    
    # RAM Info
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    ram_usage = f"{ram.used / (1024**3):.1f}/{ram.total / (1024**3):.1f} GB"
    
    # Storage Info
    st = os.statvfs('/')
    total_st = st.f_frsize * st.f_blocks / (1024**3)
    free_st = st.f_frsize * st.f_bfree / (1024**3)
    used_st = total_st - free_st
    st_percent = (used_st / total_st) * 100

    res = (
        f"🖥 {bold('OS:')} {mono(f'{platform.system()} {platform.release()}')}\n"
        f"🐍 {bold('Python:')} {mono(platform.python_version())}\n\n"
        f"🗄️ {bold('RAM:')} {mono(ram_usage)}\n"
        f"{progress_bar(ram.used, ram.total, length=15)}\n\n"
        f"💾 {bold('Disk:')} {mono(f'{used_st:.1f}/{total_st:.1f} GB')}\n"
        f"{progress_bar(used_st, total_st, length=15)}"
    )
    
    await message.edit(result_box("SYSTEM RESOURCES", res, icon="💻"))

@app.on_message(filters.command("botinfo", ".") & filters.me)
async def bot_info(client, message):
    me = await client.get_me()
    
    content = (
        f"👤 {bold('Nama:')} {me.first_name}\n"
        f"🆔 {bold('ID:')} {mono(me.id)}\n"
        f"🌐 {bold('Username:')} @{me.username or '-'}\n"
        f"🛡 {bold('Version:')} {mono('v2.5-Benxx')}\n"
        f"📦 {bold('Library:')} {mono('Pyrogram')}"
    )
    
    await message.edit(result_box("BOT INFORMATION", content, icon="🤖"))
