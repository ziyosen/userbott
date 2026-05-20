import sqlite3
import os

session_file = "myuserbot.session"  # Ganti dengan nama session Anda
target_id = -1003974077283

if not os.path.exists(session_file):
    print(f"File {session_file} tidak ditemukan!")
    exit()

conn = sqlite3.connect(session_file)
cursor = conn.cursor()

# Cek struktur tabel peers
cursor.execute("PRAGMA table_info(peers);")
columns = [col[1] for col in cursor.fetchall()]
print("Kolom yang tersedia:", columns)

# Hapus berdasarkan kolom yang tersedia
if 'peer_id' in columns:
    cursor.execute("DELETE FROM peers WHERE peer_id = ?", (target_id,))
    print(f"Deleted peer_id: {target_id}")
elif 'id' in columns:
    cursor.execute("DELETE FROM peers WHERE id = ?", (target_id,))
    print(f"Deleted id: {target_id}")
elif 'input_id' in columns:
    cursor.execute("DELETE FROM peers WHERE input_id = ?", (target_id,))
    print(f"Deleted input_id: {target_id}")
else:
    # Jika tidak tahu kolomnya, tampilkan semua data
    cursor.execute("SELECT * FROM peers")
    rows = cursor.fetchall()
    print("Isi tabel peers:")
    for row in rows:
        print(row)

conn.commit()
conn.close()
print("Selesai!")
