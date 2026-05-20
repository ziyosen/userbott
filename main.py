# main.py
from app import app
import os
import importlib
from config import OWNER_ID

# Cek apakah OWNER_ID sudah terisi
if not OWNER_ID:
    print("⚠️ PERINGATAN: OWNER_ID masih kosong di config.py!")
else:
    print(f"👤 Owner ID Terdeteksi: {OWNER_ID}")

# Load semua modules dari folder modules/
for file in os.listdir("modules"):
    if file.endswith(".py") and file != "__init__.py":
        module_name = file[:-3]
        try:
            importlib.import_module(f"modules.{module_name}")
            print(f"✅ Loaded module: {module_name}")
        except Exception as e:
            print(f"❌ Gagal load {module_name}: {e}")

print("🔥 Userbot Started!")
app.run()
