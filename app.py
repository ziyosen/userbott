import pyromod # Wajib paling atas untuk fitur percakapan bot
from pyrogram import Client
from config import API_ID, API_HASH

app = Client(
    "myuserbot",             # Pastikan ini sesuai dengan nama file .session kamu
    api_id=API_ID,
    api_hash=API_HASH,
    workers=20,              # Biar bot bisa multitasking (goreng foto + clone sekaligus)
    plugins=dict(root="modules") # OTOMATIS membaca semua file .py di dalam folder modules
)
