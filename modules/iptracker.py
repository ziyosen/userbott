import requests
import asyncio
from pyrogram import filters
from app import app
# Import style Benxx Project
from .styles import result_box, error, success, bold, mono, info as style_info

# --- LOGIKA IP TRACKER ---
@app.on_message(filters.command(["ip", "ipsakti"], ".") & filters.me)
async def track_ip(client, message):
    if len(message.command) < 2:
        return await message.edit(error("Masukkan IP! Contoh: `.ipsakti 8.8.8.8`"))
    
    ip = message.command[1]
    is_sakti = message.command[0] == "ipsakti"
    status = await message.edit(bold(f"🔍 Menganalisis IP {ip}..."))
    
    try:
        # Field diperlengkap untuk ipsakti
        fields = "status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting"
        r = requests.get(f"http://ip-api.com/json/{ip}?fields={fields}", timeout=10).json()
        
        if r.get("status") == "fail":
            return await status.edit(error(f"Gagal: {r.get('message', 'IP tidak valid')}"))

        # Logika VPN/Proxy
        vpn = "YA" if r.get("proxy") or r.get("hosting") else "TIDAK"
        
        res = (
            f"📍 {bold('Lokasi:')} {r.get('city')}, {r.get('regionName')}\n"
            f"🏳️ {bold('Negara:')} {r.get('country')} ({r.get('zip')})\n"
            f"📡 {bold('ISP:')} {r.get('isp')}\n"
            f"🏢 {bold('Org:')} {r.get('org') or '-'}\n"
            f"🛡️ {bold('VPN/Proxy:')} {mono(vpn)}"
        )

        if is_sakti:
            res += (
                f"\n🌐 {bold('ASN:')} {r.get('as')}\n"
                f"⏰ {bold('Timezone:')} {r.get('timezone')}\n"
                f"📱 {bold('Mobile:')} {'YA' if r.get('mobile') else 'TIDAK'}\n"
                f"🗺️ {bold('Koord:')} {mono(f'{r.get('lat')},{r.get('lon')}')}"
            )
        
        await status.edit(result_box(f"IP INFO: {ip}", res, icon="🌐"))
            
    except Exception as e:
        await status.edit(error(str(e)))

# --- LOGIKA INFO NOMOR ---
@app.on_message(filters.command("nomer", ".") & filters.me)
async def info_nomer(client, message):
    if len(message.command) < 2:
        return await message.edit(error("Masukkan nomor! Contoh: `.nomer 62812xxx`"))
    
    num = message.command[1]
    pref = num[:5]
    operator = "Tidak Dikenal"

    # Database Prefiks Indonesia
    tsel = ["62811", "62812", "62813", "62821", "62822", "62852", "62853", "62851"]
    isat = ["62814", "62815", "62816", "62855", "62856", "62857", "62858"]
    xl_ax = ["62817", "62818", "62819", "62859", "62877", "62878", "62831", "62838"]
    tri = ["62895", "62896", "62897", "62898", "62899"]
    sfren = ["62881", "62882", "62883", "62884", "62885", "62886", "62887", "62888", "62889"]

    if any(pref.startswith(x) for x in tsel): operator = "Telkomsel"
    elif any(pref.startswith(x) for x in isat): operator = "Indosat Ooredoo"
    elif any(pref.startswith(x) for x in xl_ax): operator = "XL Axiata / Axis"
    elif any(pref.startswith(x) for x in tri): operator = "Tri (H3I)"
    elif any(pref.startswith(x) for x in sfren): operator = "Smartfren"

    content = f"📞 {bold('Nomor:')} {mono(num)}\n📡 {bold('Operator:')} {operator}"
    await message.edit(result_box("INFO NOMOR", content, icon="📱"))

# --- LOGIKA FINDUSER ---
@app.on_message(filters.command("finduser", ".") & filters.me)
async def find_user(client, message):
    if len(message.command) < 2:
        return await message.edit(error("Masukkan username! Contoh: `.finduser benxx`"))
    
    u = message.command[1]
    status = await message.edit(bold(f"🔍 Mencari jejak @{u}..."))
    
    # Daftar sosmed yang mau di-scan
    sites = {
        "Instagram": f"https://www.instagram.com/{u}",
        "GitHub": f"https://github.com/{u}",
        "Twitter": f"https://twitter.com/{u}",
        "Facebook": f"https://facebook.com/{u}",
        "TikTok": f"https://www.tiktok.com/@{u}"
    }
    
    found = []
    for name, url in sites.items():
        try:
            # Pengecekan sederhana via status code
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                found.append(f"✅ {bold(name)}: [Klik Di Sini]({url})")
            else:
                found.append(f"❌ {name}: {mono('Tidak Ada')}")
        except:
            found.append(f"⚠️ {name}: {mono('Error')}")

    res = "\n".join(found)
    await status.edit(result_box(f"OSINT: {u}", res, icon="🕵️"))
