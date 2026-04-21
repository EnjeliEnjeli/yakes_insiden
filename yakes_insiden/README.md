# Sistem Pelaporan Insiden Siber — Yakes Telkom
Aplikasi web berbasis Flask untuk pengajuan dan pengelolaan laporan insiden keamanan siber.

## Instalasi

```bash
# 1. Masuk ke folder project
cd yakes_insiden

# 2. (Opsional) Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Untuk WeasyPrint di Ubuntu/Debian:
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0

# 5. Jalankan aplikasi
python app.py
```

Buka browser: http://localhost:5000

## Akun Demo

| Username | Password   | Role          |
|----------|------------|---------------|
| admin    | admin123   | Administrator |
| budi     | budi123    | Pelapor       |
| siti     | siti123    | Pelapor       |

## Fitur

### User (Pelapor)
- Login dengan akun masing-masing
- Formulir pengajuan insiden 3 langkah (step-by-step)
- Pilihan jenis: Phishing SMS, Vishing, Worm, DoS/DDoS
- Dashboard riwayat laporan pribadi
- Tracking status real-time dengan timeline

### Admin
- Dashboard statistik (total, menunggu, diproses, selesai)
- Grafik distribusi per kategori dan status
- Tabel semua laporan dengan filter & search
- Detail insiden + update status & catatan penanganan
- Export laporan ke PDF (per insiden)

## Struktur Project

```
yakes_insiden/
├── app.py                  ← Aplikasi utama Flask
├── requirements.txt        ← Dependencies
└── templates/
    ├── base.html           ← Layout utama dengan sidebar
    ├── login.html          ← Halaman login
    ├── admin_dashboard.html← Dashboard admin
    ├── admin_detail.html   ← Detail + update insiden (admin)
    ├── user_dashboard.html ← Dashboard pelapor
    ├── laporkan.html       ← Form 3-step pengajuan insiden
    ├── user_detail.html    ← Detail insiden (pelapor)
    └── laporan_pdf.html    ← Template export PDF
```

## Catatan untuk Pengembangan Lanjutan

Untuk produksi, ganti in-memory database dengan SQLite/PostgreSQL menggunakan SQLAlchemy:

```python
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///insiden.db'
db = SQLAlchemy(app)
```
