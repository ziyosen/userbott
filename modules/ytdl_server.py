import os
import uuid
import threading
import asyncio
import yt_dlp
from flask import Flask, request, jsonify
from pyrogram import filters
from concurrent.futures import ThreadPoolExecutor

# Mengambil objek 'app' dari app.py
from app import app
from modules.styles import result_box, error, success

# --- KONFIGURASI ---
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

executor = ThreadPoolExecutor(max_workers=3)
progress_store = {}

# --- MINI FLASK SERVER ---
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "<h1>Benxx YTDL Dashboard Running</h1>"

# Jalankan Flask di Thread terpisah
def run_flask():
    flask_app.run(host="0.0.0.0", port=7860, debug=False, use_reloader=False)

threading.Thread(target=run_flask, daemon=True).start()

# --- LOGIKA DOWNLOAD (YT-DLP) ---
def sync_download(url, job_id, fmt="mp4"):
    try:
        out_template = os.path.join(DOWNLOAD_DIR, f"{job_id}-----%(title)s.%(ext)s")
        ydl_opts = {
            "outtmpl": out_template,
            "nocheckcertificate": True,
            "quiet": True,
        }

        if fmt == "mp3":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            })
        else:
            ydl_opts.update({"format": "bestvideo[height<=720]+bestaudio/best"})

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if fmt == "mp3":
                filename = os.path.splitext(filename)[0] + ".mp3"
            return filename
    except Exception as e:
        progress_store[job_id] = {"error": str(e)}
        return None

# --- COMMAND USERBOT (.yt & .yta) ---
@app.on_message(filters.command("yt", ".") & filters.me)
async def youtube_video(client, message):
    if len(message.command) < 2:
        return await message.edit(error("Masukkan URL YouTube!"))
    
    url = message.command[1]
    await message.edit("📥 **Memproses Video (MP4)...**")
    
    loop = asyncio.get_event_loop()
    file_path = await loop.run_in_executor(executor, sync_download, url, "vid")

    if file_path and os.path.exists(file_path):
        await message.edit("📤 **Mengirim Video...**")
        await client.send_video(chat_id=message.chat.id, video=file_path)
        os.remove(file_path)
        await message.delete()
    else:
        await message.edit(error("Gagal mendownload video."))

@app.on_message(filters.command("yta", ".") & filters.me)
async def youtube_audio(client, message):
    if len(message.command) < 2:
        return await message.edit(error("Masukkan URL YouTube!"))
    
    url = message.command[1]
    await message.edit("🎵 **Memproses Audio (MP3)...**")
    
    loop = asyncio.get_event_loop()
    file_path = await loop.run_in_executor(executor, sync_download, url, "aud", "mp3")

    if file_path and os.path.exists(file_path):
        await message.edit("📤 **Mengirim Audio...**")
        await client.send_audio(chat_id=message.chat.id, audio=file_path)
        os.remove(file_path)
        await message.delete()
    else:
        await message.edit(error("Gagal mendownload audio."))
