# modules/styles.py
"""
Style profesional untuk pesan userbot
- border otomatis
- progress bar
- list template
- status report
- inline formatting
"""

def border(char="━", length=25):
    """Garis pembatas dengan karakter dan panjang tertentu."""
    return char * length

def success(text, title="✅ BERHASIL"):
    """Template pesan sukses."""
    return f"{title}\n{border()}\n{text}"

def error(text, title="❌ GAGAL"):
    """Template pesan error (teks monospace)."""
    return f"{title}\n{border()}\n`{text}`"

def info(text, title="ℹ️ INFO"):
    """Template pesan informasi biasa."""
    return f"{title}\n{border()}\n{text}"

def warning(text, title="⚠️ PERINGATAN"):
    """Template pesan peringatan."""
    return f"{title}\n{border()}\n{text}"

def result_box(title, content, icon="📊", use_border=True):
    """Kotak hasil dengan ikon kustom dan border opsional."""
    if use_border:
        return f"{icon} **{title}**\n{border()}\n{content}\n{border()}"
    else:
        return f"{icon} **{title}**\n{content}"

def progress_bar(current, total, length=10, fill="█", empty="░"):
    """Buat progress bar sederhana (misal: [████░░░░] 40%)."""
    percent = current / total
    filled = int(length * percent)
    bar = fill * filled + empty * (length - filled)
    return f"`[{bar}]` {int(percent*100)}%"

def list_items(items, title="📋 DAFTAR", numbered=False, empty_msg="_Tidak ada data_"):
    """Buat daftar item dengan format rapi (bullet atau nomor)."""
    if not items:
        return f"{title}\n{border()}\n{empty_msg}\n{border()}"
    lines = []
    for i, item in enumerate(items, 1):
        prefix = f"{i}. " if numbered else "• "
        lines.append(f"{prefix}{item}")
    return f"{title}\n{border()}\n" + "\n".join(lines) + f"\n{border()}"

def status_report(success_count, fail_count, total=None, process_name="PROSES"):
    """Laporan hasil eksekusi suatu proses (GCAST, GBAN, dll)."""
    if total is None:
        total = success_count + fail_count
    return result_box(
        f"HASIL {process_name.upper()}",
        f"✅ Berhasil: `{success_count}`\n❌ Gagal: `{fail_count}`\n📊 Total: `{total}`",
        icon="📈"
    )

def inline_code(text):
    """Alias untuk monospace inline."""
    return f"`{text}`"

def bold(text):
    return f"**{text}**"

def italic(text):
    return f"__{text}__"

def mono(text):
    return f"`{text}`"

def link(text, url):
    return f"[{text}]({url})"


# Contoh penggunaan jika dijalankan langsung (testing)
if __name__ == "__main__":
    print(success("File berhasil disimpan"))
    print(error("Koneksi terputus"))
    print(info("Memproses 5 item..."))
    print(warning("Batasi jumlah permintaan"))
    print(progress_bar(7, 10))
    print(list_items(["Item A", "Item B", "Item C"], numbered=True))
    print(status_report(15, 3, process_name="GCAST"))
