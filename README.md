Benxx Userbot adalah userbot Telegram modular yang ringan, cepat, dan didesain khusus untuk dijalankan pada environment **Termux**. Menggunakan base **Pyrogram V2** dengan sistem manajemen modul yang rapi.

---

## 🛠️ Persiapan & Instalasi (Termux)

Pastikan Termux kamu sudah up-to-date sebelum memulai instalasi. Salin dan tempel perintah berikut:

```bash
# 1. Update sistem & Install paket pendukung
pkg update && pkg upgrade -y
pkg install python nodejs ffmpeg git -y

# 2. Clone repository
git clone https://github.com/ziyosen/AkeoUserbot.git
cd AkeoUserbot

# 3. Instalasi Library Python
cp config.example.py config.py
nano config.py
pip install -r requirements.txt
# Install screen
pkg install screen -y

# Menjalankan bot dalam sesi baru
screen -S ubot python main.py
Tekan Ctrl + A lalu D untuk keluar dari tampilan bot tanpa mematikannya. Gunakan screen -r ubot untuk kembali melihat proses bot.

Kategori,Perintah,Deskripsi
📥 Download,.yt [url],Download video YouTube (MP4)
.yta [url],Download audio YouTube (MP3)
📢 Broadcast,.gcast [reply/text],Kirim pesan ke semua grup
🔍 OSINT,.ip [alamat_ip],Lacak lokasi & ISP alamat IP
.ipsakti [ip],Lacak IP dengan informasi mendalam
.myip,Cek IP publik Termux kamu
📊 System,.alive,Cek status bot & kartu nama Developer
.ping,Cek latensi/kecepatan respon bot
.sysinfo,Cek spek HP & sisa memori (Storage)
.stats,Statistik penggunaan bot
🛠️ Tools,.stiker,(Reply foto) Ubah jadi stiker
.whois,Ambil info detail profil pengguna
.purge,Hapus banyak pesan sekaligus
.del,Hapus pesan yang di-reply
🛡️ Admin,.ban / .kick,Blokir atau tendang user dari grup
.mute / .unmute,Bungkam atau buka suara user
