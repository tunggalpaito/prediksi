import random
import time
import requests
from datetime import datetime

# Mengambil tanggal, bulan, dan tahun secara otomatis hari ini
sekarang = datetime.now()
raw_date_hari_ini = sekarang.strftime("%Y-%m-%d")       # Contoh: "2026-08-26"
tgl_format_hari_ini = sekarang.strftime("%d/%m/%Y")     # Contoh: "26/08/2026"

# Konversi nama bulan ke format teks Indonesia
nama_bulan = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nov", "Des"]
format_waktu_teks = f"{sekarang.day} {nama_bulan[sekarang.month - 1]} {sekarang.year}"

# Daftar 10 Pasaran lengkap dengan Jam Result (Jam Tutup) dan URL Firebase yang sudah disesuaikan
pasaran_result = {
    "Cambodia": {"url": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-cambodia.json", "hour": 11, "minute": 50},
    "Sydney Pools": {"url": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-sydney.json", "hour": 13, "minute": 35},
    "Sydney Lotto": {"url": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-sdylotto.json", "hour": 13, "minute": 50},
    "China": {"url": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-china.json", "hour": 15, "minute": 15},
    "Macau": {"url": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-macau.json", "hour": 16, "minute": 0},
    "Japan": {"url": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-japan.json", "hour": 17, "minute": 20},
    "SGP": {"url": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-singapore.json", "hour": 17, "minute": 30},
    "Taiwan": {"url": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-taiwan.json", "hour": 20, "minute": 35},
    "Hongkong Pools": {"url": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-hongkong.json", "hour": 22, "minute": 45},
    "Hongkong Lotto": {"url": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-hklotto.json", "hour": 23, "minute": 0}
}

daftar_nama = [
    "Dimas Pratama", "Rizky Ramadhan", "Bayu Saputra", "Arya Nugraha", "Aditya Wicaksono",
    "Fajar Hidayat", "Rehan Mahendra", "Gilang Permana", "Andika Putra", "Eko Prasetyo",
    "Rendy Saputra", "Bagus Firmansyah", "Yoga Pratama", "Rian Hidayat", "Galih Kusuma",
    "Iqbal Ramadhan", "Hendra Gunawan", "Diki Wahyudi", "Wahyu Setiawan", "Arif Munandar",
    "Doni Setiawan", "Fauzi Rahman", "Geri Pratama", "Haris Maulana", "Ilham Maulana",
    "Jefri Al Buchori", "Kevin Sanjaya", "Lukman Hakim", "Mochammad Rizki", "Naufal Abiyyu",
    "Oscar Pratama", "Putra Mahardika", "Qori Sandioriva", "Rama Wijaya", "Surya Saputra",
    "Tegar Pambudi", "Umar Faruq", "Vicky Prasetyo", "Wahyu Hidayat", "Yogi Saputra",
    "Zulfikar Ali", "Bima Sakti", "Candra Kirana", "Dani Setiawan", "Feri Irawan",
    "Guntur Bumi", "Heru Setiawan", "Irfan Bachdim", "Joko Widodo", "Krisna Murti"
]

print(f"🤖 Memulai sistem bot otomatis untuk tanggal: {tgl_format_hari_ini}...")

for nama_pasaran, info in pasaran_result.items():
    url_firebase = info["url"]
    target_hour = info["hour"]
    target_minute = info["minute"]
    
    # Mengacak waktu mundur dari jam result (antara 15 sampai 60 menit sebelum tutup)
    pengurangan_menit = random.randint(15, 60)
    total_target_menit = (target_hour * 60 + target_minute) - pengurangan_menit
    jam_mulai = total_target_menit // 60
    menit_mulai = total_target_menit % 60
    
    print(f"\n🚀 Pasaran {nama_pasaran}: Result asli {target_hour:02d}:{target_minute:02d}. Bot mulai posting sekitar jam {jam_mulai:02d}:{menit_mulai:02d}")
    
    jumlah_bot = random.randint(25, 35)
    
    for i in range(1, jumlah_bot + 1):
        nama_bot = random.choice(daftar_nama)
        
        jumlah_line = random.randint(2, 15)
        tebakan_list = [f"{random.randint(0, 99):02d}" for _ in range(jumlah_line)]
        isi_tebakan = " ".join(tebakan_list)
        
        # Menggunakan tanggal otomatis hari ini
        menit_acak = random.randint(0, 59)
        data_payload = {
            "nama": nama_bot,
            "email": f"bot_{nama_pasaran.lower().replace(' ', '_')}_{i}@gmail.com",
            "isi": isi_tebakan,
            "rawDate": raw_date_hari_ini,
            "tglFormat": tgl_format_hari_ini,
            "timestamp": int(time.time() * 1000),
            "waktu": f"{format_waktu_teks}, {jam_mulai:02d}:{menit_acak:02d} WIB",
            "deviceId": f"device_{nama_pasaran}_{i}_{random.randint(1000,9999)}",
            "editCount": 1
        }
        
        try:
            response = requests.post(url_firebase, json=data_payload, timeout=5)
            if response.status_code == 200:
                print(f"   [{i}/{jumlah_bot}] Berhasil: {nama_bot} ({jumlah_line} Line)")
            else:
                print(f"   [{i}/{jumlah_bot}] Gagal: {nama_bot}")
        except Exception as e:
            print(f"   [{i}/{jumlah_bot}] Error: {e}")
            
        # Jeda antar bot diperlebar (20 s.d 60 detik) agar aman dari deteksi invalid traffic iklan
        jeda_aman = random.uniform(20.0, 60.0)
        time.sleep(jeda_aman)

print("\n🎉 Selesai! Semua bot terkirim ke masing-masing URL pasaran dengan aman.")
