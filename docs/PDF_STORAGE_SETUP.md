# 📄 PDF Storage Configuration

Sistem otomatis untuk menyimpan file PDF laporan ke folder lokal yang tidak ikut terupload ke GitHub.

## 🎯 Fitur

✅ **Automatic Git Setup**
- File PDF tersimpan di folder `/uploads/pdf`
- Folder otomatis masuk ke `.gitignore`
- Jika folder sudah terlanjur di-track git, otomatis di-untrack
- File fisik pengguna tetap aman (tidak dihapus)

✅ **Best Practices**
- Menggunakan `git rm --cached` (hanya untrack, tidak hapus file)
- Preserve empty folder dengan `.gitkeep`
- Backup-safe: semua data tetap di lokal
- Production-ready: no data loss

## 📁 Struktur

```
yakes_insiden/
├── app.py                          # Main Flask app
├── .gitignore                      # Git ignore rules (updated otomatis)
├── uploads/
│   ├── pdf/                        # 📌 PDF laporan disimpan di sini
│   │   ├── laporan_INC-0001_*.pdf
│   │   ├── laporan_INC-0002_*.pdf
│   │   └── .gitkeep               # Preserve folder di git
│   └── guides/                     # Panduan files
└── utils/
    ├── git_setup.py               # Git configuration utility
    ├── app_init.py                # App initialization
    └── __init__.py
```

## 🚀 Cara Kerja

### 1. **Startup Otomatis**
Saat aplikasi dimulai (`python app.py`):

```python
# app.py menjalankan:
from utils import initialize_app
initialize_app(app)
```

Output:
```
======================================================================
🚀 Initializing PDF Storage Configuration
======================================================================
🔍 Checking Git status...
✅ Updated .gitignore to exclude 'uploads/pdf/'
✅ Folder 'uploads/pdf' is already not tracked
======================================================================
```

### 2. **PDF Generation**
Ketika laporan dibuat, file PDF otomatis disimpan:

```python
# Existing code in app.py (tidak perlu diubah)
pdf_filename = generate_pdf(laporan)
# → Tersimpan di: /uploads/pdf/laporan_INC-0001_20260519_143022.pdf
```

### 3. **Git Ignore**
File `.gitignore` berisi:
```
# PDF Uploads - CRITICAL: Never commit user-uploaded PDFs to GitHub
uploads/pdf/
!uploads/pdf/.gitkeep
```

Ini memastikan:
- ✅ Semua file PDF dalam `uploads/pdf/` diabaikan git
- ✅ `.gitkeep` tetap tracked (untuk preserve folder)
- ✅ Ketika commit, file PDF tidak akan masuk repository

## 🛠️ Manual Setup (Jika diperlukan)

Jika folder sudah terlanjur di-track git, jalankan manual setup:

```bash
# Opsi 1: Jalankan setup script
python utils/git_setup.py

# Output:
# ============================================================
# 🔍 Checking Git status...
# ⏳ Untracking 'uploads/pdf' from git...
# ✅ Successfully untracked 'uploads/pdf' from git
#    (Files remain in your local computer)
# ✅ .gitignore already configured for 'uploads/pdf/'
# ============================================================
# ✅ Setup completed successfully!
```

Atau manual dengan git commands:
```bash
# Untrack folder dari git (tanpa delete file)
git rm --cached -r uploads/pdf/

# Staging the removal
git add uploads/pdf/

# Commit
git commit -m "Stop tracking PDF uploads"
```

## 📊 Verifikasi

Pastikan setup berhasil dengan command:

```bash
# 1. Check .gitignore config
cat .gitignore | grep -A2 "uploads/pdf"
# Output harus ada: uploads/pdf/

# 2. Check git status (tidak boleh ada uploads/pdf)
git status

# 3. Check local files (harus ada)
ls -la uploads/pdf/
# Harusnya muncul file PDF
```

## 🔒 Security & Best Practices

| Aspek | ✅ Implementasi |
|-------|-----------------|
| **File Safety** | Tidak ada file yang dihapus |
| **Git Tracking** | Folder tidak di-track, tidak di-commit |
| **Backups** | Tetap ada di local computer |
| **Production** | Safe untuk production use |
| **Automation** | Setup otomatis saat app start |
| **Documentation** | Clear dan well-documented |

## 📝 Code Reference

### app.py - Initialization
```python
from utils import initialize_app

app = Flask(__name__)
# ... config ...

# Auto setup PDF folder gitignore
initialize_app(app)

db = SQLAlchemy(app)
```

### Generate PDF (tidak perlu diubah)
```python
def generate_pdf(laporan):
    # ... build PDF elements ...
    pdf_filename = f"laporan_{laporan.nomor_insiden}_{datetime.now()}.pdf"
    pdf_path = os.path.join(app.config['PDF_FOLDER'], pdf_filename)
    with open(pdf_path, 'wb') as f:
        f.write(buffer.getvalue())
    return pdf_filename
```

### utils/git_setup.py - Core Logic
```python
def setup_pdf_folder_gitignore(project_root):
    """Setup gitignore dan untrack jika diperlukan"""
    # 1. Check jika git repo
    # 2. Untrack uploads/pdf jika sudah tracked
    # 3. Update .gitignore
    # 4. Preserve files (no deletion)
```

## ⚠️ Troubleshooting

### Q: File PDF tidak tersimpan?
**A:** Check folder permissions:
```bash
ls -la uploads/
chmod 755 uploads/pdf/
```

### Q: Git masih track uploads/pdf?
**A:** Run manual untrack:
```bash
python utils/git_setup.py
# atau
git rm --cached -r uploads/pdf/
git add uploads/pdf/
git commit -m "Untrack PDF uploads"
```

### Q: Ingin kembali track uploads/pdf?
**A:** Edit `.gitignore` dan hapus line:
```
# Hapus atau comment line ini:
# uploads/pdf/
```

## 🎓 Referensi

- **Best Practice**: [GitHub - Handling Large Files](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
- **Git Documentation**: [.gitignore](https://git-scm.com/docs/gitignore)
- **Flask Guide**: [Flask File Uploads](https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/)

## 📞 Support

Jika ada masalah, check:
1. ✅ Python version (3.7+)
2. ✅ Git installed dan configured
3. ✅ Folder permissions
4. ✅ `.gitignore` exists di project root

---

**Last Updated**: May 19, 2026
**Version**: 1.0.0
