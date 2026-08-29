import os
import requests
from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import credentials, db

# Konfigurasi Database Firebase
database_url = "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app"

if not firebase_admin._apps:
    firebase_admin.initialize_app(options={
        'databaseURL': database_url
    })

# Daftar seluruh pasaran (Cambodia, Sydney, China, Japan, Singapore, Taiwan, Hongkong)
PASARAN_LIST = [
    {"id": "lomba-cambodia", "db_key": "cambodia"},
    {"id": "lomba-sydney-pools", "db_key": "sydneypools"},
    {"id": "lomba-sydney-lotto", "db_key": "sydneylotto"},
    {"id": "lomba-china", "db_key": "china"},
    {"id": "lomba-japan", "db_key": "japan"},
    {"id": "lomba-singapore", "db_key": "singapore"},
    {"id": "lomba-taiwan", "db_key": "taiwan"},
    {"id": "lomba-hongkong-pools", "db_key": "hongkongpools"},
    {"id": "lomba-hongkong-lotto", "db_key": "hongkonglotto"}
]

def proses_rekap_pasaran(pasaran, tanggal_hari_ini):
    halaman_id = pasaran["id"]
    db_key = pasaran["db_key"]
    
    print(f"\n--- Memeriksa Pasaran: {halaman_id.upper()} ---")

    # 1. Ambil data result resmi dari Firebase (live/{db_key})
    ref_live = db.reference(f"live/{db_key}/{tanggal_hari_ini}")
    result_str = ref_live.get()
    
    match_2d = None
    if result_str and isinstance(result_str, str):
        parts = [p.strip() for p in result_str.split(",") if p.strip()]
        if parts:
            last_4d = parts[-1]
            if len(last_4d) >= 4:
                match_2d = last_4d[-2:]
                print(f"[{halaman_id}] Result 4D Sah: {last_4d} -> 2D Acuan: {match_2d}")

    if not match_2d:
        print(f"[{halaman_id}] Result resmi belum tersedia untuk tanggal {tanggal_hari_ini}.")
        return

    # 2. Ambil data komentar peserta lomba
    ref_komentar = db.reference(f"komentar/{halaman_id}")
    data_komentar = ref_komentar.get()

    if not data_komentar:
        print(f"[{halaman_id}] Tidak ada data peserta lomba.")
        return

    updates = {}
    for key, item in data_komentar.items():
        raw_date = item.get("rawDate", "")
        
        if raw_date == tanggal_hari_ini and "isi" in item:
            tebakan_str = item.get("isi", "")
            deret_angka = [x for x in tebakan_str.replace("*", " ").replace("-", " ").split() if len(x) == 2]
            
            # Cek apakah angka peserta cocok dengan 2D result
            if match_2d in deret_angka:
                current_streak = item.get("streakCount", 1)
                updates[f"{key}/isGoal"] = True
                updates[f"{key}/streakCount"] = current_streak + 1  # Dikoreksi agar streak bertambah dengan benar
                print(f"[{halaman_id}] User {item.get('nama')} JP! Streak menjadi {current_streak + 1}.")

    # Terapkan pembaruan ke Firebase
    if updates:
        ref_komentar.update(updates)
        print(f"[{halaman_id}] Database Firebase berhasil diperbarui untuk status JP.")
    else:
        print(f"[{halaman_id}] Tidak ada peserta yang tembus (JP) hari ini.")

def jalankan_semua_rekap():
    tz_wib = pytz.timezone('Asia/Jakarta')
    waktu_sekarang = datetime.now(tz_wib)
    tanggal_hari_ini = waktu_sekarang.strftime('%Y-%m-%d')
    
    print(f"Menjalankan pengecekan multi-pasaran otomatis pada: {waktu_sekarang.strftime('%Y-%m-%d %H:%M:%S')} WIB")

    for pasaran in PASARAN_LIST:
        try:
            proses_rekap_pasaran(pasaran, tanggal_hari_ini)
        except Exception as e:
            print(f"Error pada pasaran {pasaran['id']}: {str(e)}")

if __name__ == "__main__":
    jalankan_semua_rekap()
