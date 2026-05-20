import asyncio
import os
from PIL import Image
from pyrogram import filters
from pyrogram.types import Message
from app import app
from .styles import error, info

print("🎨 System: Sticker & Creative Module loading...")

@app.on_message(filters.command(["stiker", "sticker"], ".") & filters.me)
async def sticker_handler(client, message: Message):
    if not message.reply_to_message or not (message.reply_to_message.photo or message.reply_to_message.sticker):
        return await message.edit(error("Reply ke Foto atau Stiker untuk convert!"))

    status = await message.edit(info("Processing sticker..."))
    download_path = await client.download_media(message.reply_to_message)
    sticker_webp = "temp_sticker.webp"

    try:
        img = Image.open(download_path).convert("RGBA")
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        img.save(sticker_webp, "WEBP")
        await client.send_sticker(message.chat.id, sticker_webp)
        await status.delete()
    except Exception as e:
        await status.edit(error(str(e)))
    finally:
        if os.path.exists(download_path): os.remove(download_path)
        if os.path.exists(sticker_webp): os.remove(sticker_webp)

@app.on_message(filters.command(["bulge", "penyok"], ".") & filters.me)
async def bulge_handler(client, message: Message):
    """
    Efek Bulge (cembung ekstrim) untuk foto atau stiker.
    Bisa tambahkan strength: .bulge 1.2  (default 1.5, semakin besar makin parah)
    """
    # Cek input
    if not message.reply_to_message or not (message.reply_to_message.photo or message.reply_to_message.sticker):
        return await message.edit(error("Reply ke Foto atau Stiker untuk efek Bulge!"))

    # Ambil parameter strength (opsional)
    parts = message.text.split()
    strength = 1.5  # default parah
    if len(parts) > 1:
        try:
            strength = float(parts[1])
            strength = max(0.5, min(3.0, strength))  # batasan 0.5 - 3.0
        except ValueError:
            pass

    status = await message.edit(info(f"Applying Bulge effect (strength={strength})..."))
    download_path = await client.download_media(message.reply_to_message)
    bulge_webp = "bulge.webp"

    try:
        img = Image.open(download_path).convert("RGBA")
        # Resize ke 512x512 (thumbnail proporsional)
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        w, h = img.size
        cx, cy = w // 2, h // 2
        max_radius = min(cx, cy)

        result = Image.new("RGBA", (w, h))
        orig = img.load()
        new = result.load()

        # Loop transformasi
        for y in range(h):
            for x in range(w):
                dx = x - cx
                dy = y - cy
                r = (dx*dx + dy*dy) ** 0.5
                if r < max_radius and r > 0:
                    t = r / max_radius
                    # Rumus bulge: r_source = r / (1 + strength * (1 - t^2))
                    r_source = r / (1 + strength * (1 - t*t))
                    scale = r_source / r
                    sx = cx + dx * scale
                    sy = cy + dy * scale
                    if 0 <= sx < w-1 and 0 <= sy < h-1:
                        x0, y0 = int(sx), int(sy)
                        x1, y1 = min(x0+1, w-1), min(y0+1, h-1)
                        fx, fy = sx - x0, sy - y0

                        def lerp(c1, c2, f):
                            return tuple(int(c1[i] + (c2[i]-c1[i])*f) for i in range(4))

                        c00 = orig[x0, y0]
                        c10 = orig[x1, y0]
                        c01 = orig[x0, y1]
                        c11 = orig[x1, y1]
                        top = lerp(c00, c10, fx)
                        bottom = lerp(c01, c11, fx)
                        color = lerp(top, bottom, fy)
                        new[x, y] = color
                    else:
                        new[x, y] = orig[x, y]
                else:
                    new[x, y] = orig[x, y]

        result.save(bulge_webp, "WEBP")
        await client.send_sticker(message.chat.id, bulge_webp)
        await status.delete()
    except Exception as e:
        await status.edit(error(str(e)))
    finally:
        if os.path.exists(download_path): os.remove(download_path)
        if os.path.exists(bulge_webp): os.remove(bulge_webp)

print("✅ System: Sticker & Creative Module ready!")
