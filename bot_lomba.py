import random
import time
import requests

# Daftar 10 Pasaran Lengkap beserta URL Firebase-nya masing-masing
pasaran_list = {
    "Macau": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-macau.json",
    "Cambodia": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-cambodia.json",
    "Sydney Pools": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-sydneypools.json",
    "Sydney Lotto": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-sdylotto.json",
    "China": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-china.json",
    "Japan": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-japan.json",
    "SGP": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-sgp.json",
    "Taiwan": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-taiwan.json",
    "Hongkong Pools": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-hkpools.json",
    "Hongkong Lotto": "https://komentar-web-f9e2e-default-rtdb.asia-southeast1.firebasedatabase.app/komentar/lomba-hklotto.json"
}

# Daftar 50 Nama Cowok Indonesia untuk Bot
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

print("🤖 Memulai bot otomatis multi-pasaran dengan variasi waktu acak...")

# Beri jeda awal acak secara keseluruhan agar tidak langsung jalan bersamaan pas program nyala
waktu_tunggu_awal = random.randint(5, 30)
time.sleep(waktu_tunggu_awal)

for nama_pasaran, url_firebase in pasaran_list.items():
    print(f"\n🚀 Mengirim bot untuk pasaran: {nama_pasaran}")
    
    # Acak jumlah bot yang ikut tiap hari (misal antara 25 sampai 35 orang saja)
    jumlah_bot_hari_ini = random.randint(25, 35)
    
    for i in range(1, jumlah_bot_hari_ini + 1):
        # Ambil nama secara acak
        nama_bot = random.choice(daftar_nama)
        
        # Line tebakan diacak dari 2 sampai 15 line
        jumlah_line = random.randint(2, 15)
        tebakan_list = [f"{random.randint(0, 99):02d}" for _ in range(jumlah_line)]
        isi_tebakan = " ".join(tebakan_list)
        
        # Timestamp saat ini + sedikit variasi detik acak agar tidak kembar
        current_time_ms = int(time.time() * 1000) + random.randint(100, 90000)
        
        data_payload = {
            "nama": nama_bot,
            "email": f"bot_{nama_pasaran.lower().replace(' ', '_')}_{i}@gmail.com",
            "isi": isi_tebakan,
            "rawDate": "2026-06-06",
            "tglFormat": "06/06/2026",
            "timestamp": current_time_ms,
            "waktu": f"6 Jun 2026, 12:{random.randint(10, 45):02d} WIB", # Jam menit dibuat variatif
            "deviceId": f"device_{nama_pasaran}_{i}_{random.randint(1000,9999)}",
            "editCount": 1
        }
        
        try:
            response = requests.post(url_firebase, json=data_payload, timeout=5)
            if response.status_code == 200:
                print(f"   [{i}/{jumlah_bot_hari_ini}] Berhasil: {nama_bot} ({jumlah_line} Line)")
            else:
                print(f"   [{i}/{jumlah_bot_hari_ini}] Gagal: {nama_bot}")
        except Exception as e:
            print(f"   [{i}/{jumlah_bot_hari_ini}] Error koneksi: {e}")
            
        # Jeda waktu antar bot dibuat acak (antara 2 detik sampai 8 detik) 
        # supaya terlihat seperti orang ngirim satu-satu secara bergantian
        jeda_acak = random.uniform(2.0, 8.0)
        time.sleep(jeda_acak)

print("\n🎉 Selesai! Semua bot terkirim dengan pola acak yang natural.")
