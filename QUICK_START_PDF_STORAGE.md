# 🚀 Quick Start - PDF Storage Setup

## ✨ Apa yang Sudah Disetup?

Sistem otomatis sudah dikonfigurasi untuk:

✅ Menyimpan file PDF laporan ke folder `/uploads/pdf`  
✅ Otomatis exclude folder dari GitHub (.gitignore)  
✅ Jika sudah terlanjur di-track, otomatis di-untrack  
✅ Preserve semua file (tidak ada yang dihapus)  
✅ Jalankan otomatis saat aplikasi startup  

## 🎯 Mulai Menggunakan

### 1. Jalankan Aplikasi Seperti Biasa

```bash
python app.py
```

Output saat startup akan menunjukkan:
```
======================================================================
🚀 Initializing PDF Storage Configuration
======================================================================
🔍 Checking Git status...
✅ .gitignore already configured for 'uploads/pdf/'
✅ Folder 'uploads/pdf' is already not tracked
======================================================================
```

### 2. Mulai Buat Laporan

- Aplikasi siap menerima laporan baru
- File PDF otomatis tersimpan di `uploads/pdf/`
- File tidak akan di-commit ke GitHub

### 3. Verifikasi Setup

Jalankan test script:
```bash
python test_pdf_storage_setup.py
```

Hasilnya:
```
✅ Check 1: app.py exists
✅ Check 2: .gitignore configured
✅ Check 3: Git repo status
✅ Check 4: uploads/pdf not tracked
... (lebih banyak checks)

All checks passed! PDF Storage setup is configured correctly.
```

## 📁 Struktur File

```
yakes_insiden/
├── app.py                          # Main app (sudah updated)
├── .gitignore                      # Created (exclude uploads/pdf/)
├── test_pdf_storage_setup.py      # Test script
├── utils/
│   ├── __init__.py                # Package init
│   ├── git_setup.py               # Git configuration
│   └── app_init.py                # App initialization
├── docs/
│   └── PDF_STORAGE_SETUP.md       # Full documentation
└── uploads/
    └── pdf/                        # 📌 PDF laporan tersimpan di sini
        ├── laporan_INC-0001_*.pdf
        ├── laporan_INC-0002_*.pdf
        └── .gitkeep
```

## ✅ Checklist Verifikasi

- [ ] Aplikasi berjalan tanpa error
- [ ] Output saat startup menunjukkan setup berhasil
- [ ] File PDF terbuat di `uploads/pdf/`
- [ ] `git status` tidak menampilkan file PDF
- [ ] `python test_pdf_storage_setup.py` all passed

## 🔧 Jika Ada Masalah

### Masalah 1: "uploads/pdf folder not found"
```bash
mkdir -p uploads/pdf
python app.py
```

### Masalah 2: "git still tracking uploads/pdf"
```bash
python utils/git_setup.py
```

### Masalah 3: Ingin tahu detail setup
```bash
cat .gitignore | grep -A2 "uploads/pdf"
git status  # Pastikan tidak ada uploads/pdf
```

## 📚 Dokumentasi Lengkap

Untuk detail lebih lanjut, baca:
- [PDF_STORAGE_SETUP.md](./docs/PDF_STORAGE_SETUP.md) - Dokumentasi lengkap
- [app.py](./app.py) - Lihat imports dan initialize_app call
- [utils/git_setup.py](./utils/git_setup.py) - Core logic

## 🎓 Ringkasan Teknis

| Komponen | Fungsi |
|----------|--------|
| `.gitignore` | Exclude `uploads/pdf/` dari git |
| `utils/git_setup.py` | Untrack jika sudah di-track, update `.gitignore` |
| `utils/app_init.py` | Orchestrate initialization |
| `app.py` | Call `initialize_app()` saat startup |
| `generate_pdf()` | Save PDF ke `app.config['PDF_FOLDER']` |

## ⚡ Key Points

1. **Otomatis**: Setup jalan saat app start, tidak perlu manual
2. **Safe**: File tetap di lokal, tidak dihapus
3. **Git-friendly**: PDF tidak masuk repo GitHub
4. **Production-ready**: Tested dan best-practice compliant
5. **Well-documented**: Full docs & test script included

---

**Next Steps:**
1. ✅ Jalankan: `python app.py`
2. ✅ Test: `python test_pdf_storage_setup.py`
3. ✅ Commit code (tanpa PDF files)
4. ✅ Deploy dengan percaya diri!

**Support:**
- Baca [PDF_STORAGE_SETUP.md](./docs/PDF_STORAGE_SETUP.md)
- Run test script untuk verifikasi
- Check git status: `git status`
