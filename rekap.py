import os
import requests
from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import credentials, db

# 1. Inisialisasi Koneksi ke Firebase menggunakan Environment Variables atau konfigurasi langsung
# (Disarankan menggunakan Firebase Service Account JSON yang disimpan di GitHub Secrets)
cred_dict = {
    "type": "service_account",
    "project_id": os.environ.get("FIREBASE_PROJECT_ID", "komentar-web-f9e2e"),
    "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID", ""),
    "private_key": os.environ.get("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n'),
    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL", ""),
    "client_id": os.environ.get("FIREBASE_CLIENT_ID", ""),
    "auth_uri": "https://accounts.google.com/oauth/v2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get("FIREBASE_CERT_URL", "")
}

# Jika dijalankan tanpa service account JSON lengkap, bisa menggunakan Database URL langsung
database_url = "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app"

if not firebase_admin._apps:
    # Alternatif inisialisasi dengan Database URL saja (menggunakan aturan auth public/secret token jika diizinkan)
    firebase_admin.initialize_app(options={
        'databaseURL': database_url
    })

def jalankan_rekap_otomatis():
    # Set waktu zona WIB (Jakarta)
    tz_wib = pytz.timezone('Asia/Jakarta')
    waktu_sekarang = datetime.now(tz_wib)
    tanggal_hari_ini = waktu_sekarang.strftime('%Y-%m-%d')
    
    print(f"Memulai proses rekap otomatis untuk tanggal: {tanggal_hari_ini} (WIB)")

    # 1. Ambil data result resmi Cambodia hari ini (contoh endpoint atau dari node live/cambodia)
    ref_live = db.reference(f"live/cambodia/{tanggal_hari_ini}")
    result_str = ref_live.get()
    
    match_2d = None
    if result_str and isinstance(result_str, str):
        parts = [p.strip() for p in result_str.split(",") if p.strip()]
        if parts:
            last_4d = parts[-1]
            if len(last_4d) >= 4:
                match_2d = last_4d[-2:]
                print(f"Result 4D Sah: {last_4d} -> 2D Acuan: {match_2d}")

    # 2. Ambil data komentar/peserta lomba
    halaman_id = "lomba-cambodia"
    ref_komentar = db.reference(f"komentar/{halaman_id}")
    data_komentar = ref_komentar.get()

    if not data_komentar:
        print("Tidak ada data peserta lomba ditemukan.")
        return

    updates = {}
    for key, item in data_komentar.items():
        raw_date = item.get("rawDate", "")
        
        # Validasi jika postingan adalah hari ini dan ada result 2D
        if raw_date == tanggal_hari_ini and match_2d and "isi" in item:
            tebakan_str = item.get("isi", "")
            # Bersihkan format angka tebakan
            deret_angka = [x for x in tebakan_str.replace("*", " ").replace("-", " ").split() if len(x) == 2]
            
            if match_2d in deret_angka:
                current_streak = item.get("streakCount", 1)
                # Update status goal dan tingkatkan streak jika tembus
                updates[f"{key}/isGoal"] = True
                updates[f"{key}/streakCount"] = current_streak + 1
                print(f"User {item.get('nama')} JP! Streak bertambah.")

    # Terapkan pembaruan status ke Firebase jika ada yang JP
    if updates:
        ref_komentar.update(updates)
        print("Database Firebase berhasil diperbarui untuk status JP hari ini.")
    else:
        print("Tidak ada peserta yang JP atau result belum lengkap.")

if __name__ == "__main__":
    jalankan_rekap_otomatis()
