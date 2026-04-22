# 📚 Guide Upload & Download Feature - Implementation Complete ✅

## What Was Added

A complete guide management system where:
- **Admin** can upload PDF guides for different incident types
- **Users** can view and download the guides

---

## 🎯 Quick Summary

### Incident Guide Types Available
1. **🦠 Worm** - Panduan penanganan Worm dan malware
2. **📡 DoS/DDoS** - Panduan penanganan serangan Denial of Service
3. **🎣 Phishing/Vishing** - Panduan penanganan phishing email, SMS, dan vishing call

---

## 👨‍💼 Admin Features

### Upload Guides
- Go to **Sidebar → Panduan → Kelola Panduan**
- For each guide type:
  1. Click "Pilih File..."
  2. Select a PDF file (max 50MB)
  3. Click "Unggah Panduan [Type]"
  4. File uploads and stored automatically

### Manage Guides
- View upload status for all guides
- See last upload date/time
- Delete outdated guides with one click
- Replace guides with newer versions

### Automatic Features
- ✅ Old files auto-deleted when new guide uploaded
- ✅ Secure filename handling
- ✅ PDF validation
- ✅ Timestamp tracking

---

## 👥 User Features

### View Guides
- Go to **Sidebar → Panduan → Lihat Panduan**
- See 3 guide types with descriptions
- View availability status:
  - ✓ Tersedia (Available) - Guide uploaded
  - ⊘ Belum tersedia (Not available) - Waiting for upload

### Download Guides
- For uploaded guides, click **"Unduh Panduan"** button
- PDF downloads to computer
- Can be opened immediately

### Information Display
- Guide type name and description
- Upload status
- Last update date/time
- Clear download button

---

## 📁 File Structure

### Backend Code
```
app.py (updated with)
├── New imports: send_file, secure_filename
├── Upload folder configuration
├── guides_db: Guide storage
└── 4 new routes:
    ├── /guides (View guides)
    ├── /admin/guides (Manage guides)
    ├── /admin/guides/<type>/delete (Delete guide)
    └── /guides/<type>/download (Download guide)
```

### New Templates
```
templates/
├── guides.html (User page)
└── admin_guides.html (Admin page)
```

### Storage
```
uploads/
├── Worm_20260421_150545.pdf (if uploaded)
├── DoS-DDoS_20260421_150300.pdf (if uploaded)
└── Phishing_20260421_150245.pdf (if uploaded)
```

---

## 🔐 Security

✅ **Only PDF files allowed**
- File extension validation
- MIME type checking
- Size limit: 50MB

✅ **Access Control**
- Upload: Admin only
- Delete: Admin only
- Download: All authenticated users
- View: All authenticated users

✅ **Safe File Handling**
- Secure filename generation
- Automatic old file cleanup
- Error handling for missing files

---

## 🔗 Navigation

### User Sidebar
```
PANDUAN
├── Lihat Panduan ← NEW
```

### Admin Sidebar
```
PANDUAN
├── Lihat Panduan ← NEW
└── Kelola Panduan ← NEW (Admin only)
```

---

## 📊 Data Structure

### guides_db
```python
{
    'Worm': {
        'filename': 'Worm_20260421_150545.pdf' or None,
        'uploaded_date': '2026-04-21 15:05:45' or None,
        'description': 'Panduan penanganan Worm'
    },
    'DoS/DDoS': { ... },
    'Phishing': { ... }
}
```

---

## 🧪 Test It Now

### As Admin (admin/admin123)
1. Login to system
2. Click "Kelola Panduan" in sidebar
3. Select guide type (e.g., "Worm")
4. Choose a PDF file from computer
5. Click "Unggah Panduan Worm"
6. See success message ✓

### As User (budi/budi123)
1. Login to system
2. Click "Lihat Panduan" in sidebar
3. See 3 guide types
4. For uploaded guides, click "Unduh Panduan"
5. PDF downloads ✓

---

## 📝 Routes Reference

| URL | Method | Access | Purpose |
|-----|--------|--------|---------|
| `/guides` | GET | All users | View guides list |
| `/guides/Worm/download` | GET | All users | Download Worm guide |
| `/admin/guides` | GET | Admin | Manage guides page |
| `/admin/guides` | POST | Admin | Upload new guide |
| `/admin/guides/Worm/delete` | POST | Admin | Delete guide |

---

## 🎨 User Interface

### Admin Panel (Kelola Panduan)
```
✏️ Guide Management

🦠 Worm
  Status: ✓ Diunggah (2026-04-21 15:05:45)
  [Hapus] atau [Pilih File] [Unggah]

📡 DoS/DDoS
  Status: ⊘ Belum diunggah
  [Pilih File] [Unggah]

🎣 Phishing/Vishing
  Status: ✓ Diunggah (2026-04-21 15:03:00)
  [Hapus] atau [Pilih File] [Unggah]
```

### User Page (Lihat Panduan)
```
📖 Panduan Insiden Siber

┌─────────────────────────────────────┐
│ 🦠 Worm                              │
│ Panduan penanganan infeksi worm...  │
│ ✓ Tersedia (2026-04-21 15:05:45)    │
│ [Unduh Panduan]                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 📡 DoS / DDoS                        │
│ Panduan penanganan serangan DoS...  │
│ ⊘ Belum tersedia                    │
│ Panduan belum diunggah oleh admin   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 🎣 Phishing / Vishing                │
│ Panduan penanganan phishing email...│
│ ✓ Tersedia (2026-04-21 15:03:00)    │
│ [Unduh Panduan]                     │
└─────────────────────────────────────┘
```

---

## 💾 Storage Location

All uploaded PDF files are stored in:
```
c:\Users\ASUS\Downloads\yakes_insiden\yakes_insiden\uploads\
```

Files are named with format:
```
[GuideType]_[YYYYMMDD]_[HHMMSS].pdf
```

Example:
```
Worm_20260421_150545.pdf
DoS-DDoS_20260421_150300.pdf
Phishing_20260421_150245.pdf
```

---

## ⚙️ Configuration

**In app.py:**
```python
# Upload settings
UPLOAD_FOLDER = 'yakes_insiden/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max
```

**Can be modified for:**
- Different file types
- Larger file sizes
- Different storage locations

---

## 📋 Implementation Checklist

- [x] Backend routes added to app.py
- [x] File upload handling implemented
- [x] File deletion handling implemented
- [x] guides_db created
- [x] Admin template created (admin_guides.html)
- [x] User template created (guides.html)
- [x] Sidebar navigation links added
- [x] Security validation added
- [x] Error handling implemented
- [x] Styling with blue & white theme
- [x] Documentation created

---

## 🚀 Ready to Deploy

✅ All code implemented
✅ All templates created
✅ All routes configured
✅ Navigation integrated
✅ Security validated
✅ Error handling complete
✅ User-friendly interface

---

## 📞 Quick Help

### Problem: Can't upload file
- **Solution**: Ensure file is PDF and under 50MB

### Problem: Can't see upload button
- **Solution**: Make sure you're logged in as admin

### Problem: Downloaded file won't open
- **Solution**: Check that it's a valid PDF and opened with PDF reader

### Problem: File disappeared after upload
- **Solution**: This is normal! Old file is deleted when new one uploaded

---

## 🎯 Next Steps

1. **Login as admin** (admin/admin123)
2. **Go to Sidebar → Panduan → Kelola Panduan**
3. **Upload a test PDF guide**
4. **Login as user** (budi/budi123)
5. **Go to Sidebar → Panduan → Lihat Panduan**
6. **Download the guide to test**

✅ **Feature is ready to use!**

---

**Status: ✅ COMPLETE - Guide Upload & Download Feature Ready for Production**
