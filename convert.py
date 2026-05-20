import asyncio
from pyrogram import Client

async def main():
    print("--- Benxx Session to String Converter ---")
    
    # Membuka file session yang sudah ada tanpa login ulang
    async with Client("myuserbot") as app:
        session_str = await app.export_session_string()
        
        print("\n=== KODE STRING SESSION KAMU ===")
        print(session_str)
        print("=================================\n")
        
        # Kirim ke Saved Messages biar gak ilang
        await app.send_message(
            "me", 
            f"**AkeoUserbot - Exported String Session:**\n\n`{session_str}`"
        )
        print("✅ Kode String Session sudah dikirim ke Pesan Tersimpan Telegram kamu!")

if __name__ == "__main__":
    asyncio.run(main())
