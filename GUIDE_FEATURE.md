# Guide Upload & Download Feature

## Overview
Implemented a comprehensive guide management system that allows admins to upload PDF guides for different incident types, and users to view and download them.

---

## 🎯 Features

### For Admin
✅ **Upload Guides**
- Upload PDF guides for each incident type (Worm, DoS/DDoS, Phishing)
- Replace existing guides with newer versions
- File security: only PDF files allowed, max 50MB
- Automatic filename sanitization

✅ **Manage Guides**
- View all guides and their upload status
- Delete outdated guides
- See last upload timestamp for each guide
- Confirmation dialog before deletion

✅ **Admin Panel**
- Dedicated admin guides management page
- Clean, organized interface
- Instructions for proper usage
- Real-time status indicators

### For User
✅ **View Guides**
- Browse available guides for all incident types
- See guide availability status
- Download guides as PDF
- View last update date for each guide

✅ **Easy Access**
- "Lihat Panduan" (View Guides) link in sidebar for all users
- Dedicated guides page with clear layout
- Icons and descriptions for each guide type
- One-click download button

---

## 📁 File Structure

### Backend Files Modified
```
app.py
├── Added imports: send_file, secure_filename, Path
├── Added configuration: UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH
├── Added guides_db: in-memory database for guides storage
├── Added routes:
│   ├── /guides (GET) - View all guides
│   ├── /admin/guides (GET, POST) - Admin upload/manage guides
│   ├── /admin/guides/<type>/delete (POST) - Delete guide
│   └── /guides/<type>/download (GET) - Download guide PDF
```

### New Templates Created
```
templates/
├── guides.html - User-facing guides page
└── admin_guides.html - Admin guide management page
```

### Directory Structure
```
yakes_insiden/
├── app.py
├── templates/
│   ├── base.html (modified - added guide nav links)
│   ├── guides.html (new)
│   └── admin_guides.html (new)
├── uploads/ (auto-created)
│   └── (PDF files stored here with format: GuideType_YYYYMMDDate_HHMMSS.pdf)
```

---

## 🔄 How It Works

### Admin Upload Flow
1. Admin clicks "Kelola Panduan" in sidebar
2. Selects guide type from dropdown
3. Chooses PDF file to upload
4. Clicks "Unggah Panduan [Type]"
5. File is saved to `uploads/` folder with secure name
6. Database updated with filename and timestamp
7. Success message displayed
8. Users can now download the guide

### User Download Flow
1. User clicks "Lihat Panduan" in sidebar
2. Views list of 3 guide types with descriptions
3. For each type, shows:
   - Icon and name
   - Description
   - Availability status
   - Last update date (if uploaded)
4. Clicks "Unduh Panduan" to download
5. PDF opens or downloads to computer

### File Management
- **Upload location**: `yakes_insiden/uploads/`
- **Filename format**: `GuideType_YYYYMMDDate_HHMMSS.pdf`
- **Old files**: Automatically deleted when new guide uploaded
- **Max size**: 50MB per file
- **Allowed types**: PDF only

---

## 📋 Database Schema

### guides_db Structure
```python
guides_db = {
    'Worm': {
        'filename': 'Worm_20260421_150545.pdf',  # or None if not uploaded
        'uploaded_date': '2026-04-21 15:05:45',   # or None
        'description': 'Panduan penanganan Worm'
    },
    'DoS/DDoS': {
        'filename': None,
        'uploaded_date': None,
        'description': 'Panduan penanganan DoS/DDoS'
    },
    'Phishing': {
        'filename': 'Phishing_20260421_150300.pdf',
        'uploaded_date': '2026-04-21 15:03:00',
        'description': 'Panduan penanganan Phishing/Vishing'
    }
}
```

---

## 🔐 Security Features

✅ **File Validation**
- Only PDF files allowed
- Secure filename handling using `secure_filename()`
- File size limit: 50MB

✅ **Access Control**
- Guide upload: Admin only
- Guide deletion: Admin only
- Guide viewing: All authenticated users
- Guide download: All authenticated users

✅ **Error Handling**
- File not found handling
- Invalid file type rejection
- File upload error messages
- Safe file deletion

---

## 🎨 User Interface

### User Guide Page (guides.html)
```
┌─────────────────────────────────┐
│ Panduan Insiden Siber           │
│ Panduan penanganan berbagai...  │
└─────────────────────────────────┘

┌────────────────┬────────────────┬────────────────┐
│ 🦠 Worm        │ 📡 DoS/DDoS    │ 🎣 Phishing    │
├────────────────┼────────────────┼────────────────┤
│ Panduan...     │ Panduan...     │ Panduan...     │
│                │                │                │
│ ✓ Tersedia     │ ⊘ Belum ada   │ ✓ Tersedia     │
│ Diupdate: ...  │                │ Diupdate: ...  │
│ [Unduh]        │ [Panduan...]   │ [Unduh]        │
└────────────────┴────────────────┴────────────────┘

ℹ️ Informasi
Panduan ini berisi prosedur standar...
```

### Admin Guide Management (admin_guides.html)
```
┌─────────────────────────────────┐
│ Kelola Panduan                  │
│ Upload dan kelola panduan...    │
└─────────────────────────────────┘

Guide 1: 🦠 Worm
Status: ✓ Diunggah (2026-04-21 15:05:45)
[Hapus] atau [Pilih File...] [Unggah]

Guide 2: 📡 DoS/DDoS
Status: ⊘ Belum diunggah
[Pilih File...] [Unggah]

Guide 3: 🎣 Phishing/Vishing
Status: ✓ Diunggah (2026-04-21 15:03:00)
[Hapus] atau [Pilih File...] [Unggah]

📋 Petunjuk Penggunaan:
- Panduan harus berupa file PDF...
- Setiap jenis insiden...
- Mengunggah panduan baru...
```

---

## 🔗 Navigation Links

### User Navigation (Sidebar)
```
MENU
├── Dashboard Saya
├── Laporkan Insiden
PANDUAN
├── Lihat Panduan ← NEW
└── (no admin link)
```

### Admin Navigation (Sidebar)
```
ADMIN
├── Dashboard
├── Semua Laporan
PANDUAN
├── Lihat Panduan
└── Kelola Panduan ← NEW
```

---

## 📊 Routes Reference

| Route | Method | Access | Function |
|-------|--------|--------|----------|
| `/guides` | GET | Authenticated | View all guides |
| `/guides/<type>/download` | GET | Authenticated | Download guide PDF |
| `/admin/guides` | GET, POST | Admin only | Manage guides, upload |
| `/admin/guides/<type>/delete` | POST | Admin only | Delete guide |

---

## 💾 Database Persistence Notes

**Current Implementation**: In-memory storage (guides_db dictionary)
- ✅ Works for demo/development
- ✅ Files persist (stored on disk)
- ⚠️ Guide metadata resets on app restart
- ⚠️ Not suitable for production

**For Production**: Migrate to SQLite/PostgreSQL
```python
# Example: Store guides metadata in database
guides_table = """
CREATE TABLE guides (
    id INTEGER PRIMARY KEY,
    guide_type TEXT UNIQUE,
    filename TEXT,
    uploaded_date TIMESTAMP,
    description TEXT
)
"""
```

---

## 🧪 Testing Scenarios

### Admin Upload Workflow
1. ✅ Login as admin
2. ✅ Click "Kelola Panduan"
3. ✅ Select "Worm" and PDF file
4. ✅ Click "Unggah Panduan Worm"
5. ✅ See success message
6. ✅ File appears in uploads folder

### User Download Workflow
1. ✅ Login as user (budi/siti)
2. ✅ Click "Lihat Panduan"
3. ✅ See available guides
4. ✅ For uploaded guides, see status + date
5. ✅ Click "Unduh Panduan"
6. ✅ PDF downloads successfully

### Admin Delete Workflow
1. ✅ Login as admin
2. ✅ Click "Kelola Panduan"
3. ✅ Find uploaded guide
4. ✅ Click "Hapus"
5. ✅ Confirm deletion
6. ✅ File removed, status shows "Belum diunggah"

---

## 🐛 Error Handling

| Error | Response |
|-------|----------|
| No file selected | "Tidak ada file yang dipilih." |
| Non-PDF file | "File harus berupa PDF." |
| File not found (download) | "File tidak ditemukan." |
| Invalid guide type | Redirects to guides page |
| Download error | "Terjadi kesalahan saat mengunduh file..." |
| Access denied (non-admin) | Redirects to user dashboard |

---

## 📝 Code Snippets

### Adding a new guide type
```python
guides_db['New Type'] = {
    'filename': None,
    'uploaded_date': None,
    'description': 'Deskripsi panduan baru'
}
```

### Checking if guide exists
```python
if guides['Worm']['filename']:
    # Guide is available
    print("Guide tersedia")
else:
    # Guide not uploaded yet
    print("Belum diunggah")
```

---

## 🚀 Future Enhancements

Potential improvements:
1. **Database persistence**: Migrate to SQLite/PostgreSQL
2. **File versioning**: Keep upload history
3. **Preview**: Show PDF preview in browser
4. **Search**: Search guides by keyword
5. **Tags**: Add topic tags to guides
6. **Notifications**: Notify users when guide updated
7. **Analytics**: Track guide downloads
8. **Categories**: Organize guides by category
9. **Multilingual**: Support multiple languages
10. **Mobile**: Optimize for mobile viewing

---

## ✅ Implementation Checklist

- [x] Backend routes implemented
- [x] File upload handling
- [x] File deletion handling
- [x] Admin template created
- [x] User template created
- [x] Navigation links added
- [x] Security validation added
- [x] Error handling implemented
- [x] Styling applied
- [x] Documentation created

---

## 📞 Usage Guide

### For Admin
1. Navigate to "Kelola Panduan" in sidebar
2. For each guide type:
   - Select PDF file from computer
   - Click upload button
   - Wait for success message
3. To delete:
   - Find uploaded guide
   - Click "Hapus" button
   - Confirm deletion

### For Users
1. Navigate to "Lihat Panduan" in sidebar
2. Browse the 3 available guide types
3. For guides with ✓ status:
   - Click "Unduh Panduan" button
   - PDF will download
4. For guides with ⊘ status:
   - Panduan belum diunggah (guide not yet uploaded)

---

## 🎓 Summary

The guide upload and download feature provides:

✅ **For Organization**
- Centralized guide storage
- Easy guide management
- Clear versioning

✅ **For Admin**
- Simple upload interface
- One-file-per-type system
- Easy deletion

✅ **For Users**
- Easy guide discovery
- One-click download
- Clear availability status
- Update timestamps

✅ **Technical**
- Secure file handling
- Proper access control
- Error handling
- Ready for scaling

**Status: ✅ Feature Complete and Ready for Use**
