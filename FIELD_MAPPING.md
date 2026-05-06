# Form Fields Mapping - Gambar Laporan ke Aplikasi

## Gambar Form: "FORM LAPORAN INSIDEN KOMPUTER WORM"

### Mapping ke Aplikasi YAKES

| Gambar | Field Name | Input Type | Step | Status |
|--------|-----------|-----------|------|--------|
| **Judul insiden** | (Auto-generated as ID) | Auto | N/A | - |
| **Tempat & Waktu** | `tanggal`, `jam` | Date + Time | 2 | ✅ |
| **Tim CSIRT** | `tim_csirt` | Text | 2 | ✅ NEW |
| **Sistem Terdampak** | `sistem_terdampak` | Text | 2 | ✅ NEW |
| | | | | |
| **Ringkasan Insiden** | `ringkasan_insiden` | Textarea | 2 | ✅ NEW |
| | | | | |
| **Kronologi** | `kronologi` | Textarea | 2 | ✅ NEW |
| | | | | |
| **Akar Masalah (Root Cause)** | `akar_masalah` | Textarea | 3 | ✅ NEW |
| | | | | |
| **Indikator (IOC / IOA):** | | | | |
| - Hash | `ioc_hash` | Text | 3 | ✅ NEW |
| - Ip/Domain | `ioc_ip_domain` | Text | 3 | ✅ NEW |
| - Port / Media | `ioc_port_media` | Text | 3 | ✅ NEW |
| | | | | |
| **Analisis Teknis** | `analisis_teknis` | Textarea | 3 | ✅ NEW |
| | | | | |
| **Aksi SOC (Detection)** | `aksi_soc` | Textarea | 3 | ✅ NEW |
| | | | | |
| **Aksi IR (Response)** | `aksi_ir` | Textarea | 3 | ✅ NEW |
| | | | | |
| **Pemulihan** | `pemulihan` | Textarea | 3 | ✅ NEW |
| | | | | |
| **Rekomendasi** | `rekomendasi` | Textarea | 3 | ✅ NEW |

---

## Form Flow di Aplikasi

```
STEP 1: Pilih Jenis Insiden
├─ Phishing SMS
├─ Vishing
├─ Worm
└─ DoS/DDoS

↓

STEP 2: Detail Kejadian
├─ Tanggal Kejadian *
├─ Jam Kejadian *
├─ Lokasi Kejadian *
├─ Tim CSIRT
├─ Sistem Terdampak
├─ Tingkat Keparahan *
├─ Deskripsi Kejadian *
├─ Ringkasan Insiden
└─ Kronologi

↓

STEP 3: Analisis & Tindakan
├─ Dampak yang Ditimbulkan *
├─ Tindakan Awal yang Sudah Dilakukan *
├─ Akar Masalah (Root Cause)
├─ Indikator (IOC/IOA):
│  ├─ Hash
│  ├─ IP/Domain
│  └─ Port/Media
├─ Analisis Teknis
├─ Aksi SOC (Detection)
├─ Aksi IR (Response)
├─ Pemulihan
└─ Rekomendasi

↓ SUBMIT

Admin dapat Download PDF dengan semua data ✅
```

---

## PDF Output Example

Ketika admin export ke PDF, dokumen akan berisi:

```
┌─────────────────────────────────┐
│   LAPORAN INSIDEN KEAMANAN      │
└─────────────────────────────────┘

METADATA:
┌────────────────────────┐
│ ID Insiden    │ INC-006 │
│ Jenis         │ Worm    │
│ Status        │ Diproses│
│ Severity      │ Tinggi  │
│ Pelapor       │ Budi... │
│ Tanggal       │ 20/7/25 │
│ Jam           │ 14:30   │
│ Lokasi        │ Lt. 3   │
│ Updated       │ 21/7/25 │
└────────────────────────┘

DESKRIPSI INSIDEN
Menerima email mencurigakan dengan attachment...

DAMPAK
Komputer terinfeksi, data tersebar ke 5 komputer lain...

TINDAKAN AWAL
Server diisolasi segera dari jaringan...

TIM CSIRT
SOC Alpha Team melakukan investigasi...

SISTEM TERDAMPAK
Server Web #3, Database Server, Workstation 5 unit...

RINGKASAN INSIDEN
Worm menyebar melalui SMB...

KRONOLOGI
14:30 - Alert terdeteksi
14:35 - Server diisolasi
14:50 - Analisis dimulai
...

AKAR MASALAH
Patch Windows belum diupdate, exploit EternalBlue...

INDIKATOR (IOC/IOA)
Hash: a1b2c3d4e5f6...
IP/Domain: 192.168.1.100, malware.com
Port/Media: 445/TCP, SMB

ANALISIS TEKNIS
Worm menggunakan pendekatan lateral movement...

AKSI SOC (DETECTION)
Firewall rules ditambahkan untuk block traffic...

AKSI IR (RESPONSE)
Semua host di-clean dengan antivirus terbaru...

PEMULIHAN
Sistem direstart, backup dipulihkan, traffic normal...

REKOMENDASI
- Implementasi Windows Update policy ketat
- Segmentasi jaringan untuk sistem kritis
- Monitoring traffic anomali 24/7
```

---

## Keuntungan Implementasi Baru

✅ **Untuk User:**
- Form yang lebih lengkap sesuai template resmi
- Dapat mengisi semua informasi teknis yang diperlukan
- Proses pelaporan lebih terstruktur (3 step)

---

## Testing Scenario

### User: Melaporkan Insiden Worm

1. **User Login** sebagai `budi` / `budi123`
2. **Klik "Laporkan Insiden"**
3. **STEP 1:** Pilih "Worm" → Klik "Lanjutkan"
4. **STEP 2:** Isi:
   - Tanggal: 2025-07-20
   - Jam: 14:30
   - Lokasi: Kantor Pusat Bandung, Lt. 3
   - Tim CSIRT: SOC Team Alpha
   - Sistem: Server Web 3, Database
   - Severity: Tinggi
   - Deskripsi: Worm terdeteksi di server...
   - Ringkasan: Malware worm menyebar...
   - Kronologi: 14:30 Alert diterima, 14:35 Server diisolasi...
   - Klik "Lanjutkan"
5. **STEP 3:** Isi:
   - Dampak: Kinerja server down, 100 user terdampak...
   - Tindakan: Server segera diisolasi dari jaringan...
   - Root Cause: Patch Windows belum diupdate...
   - IOC Hash: a1b2c3d4e5f6...
   - IOC IP: 192.168.1.100
   - IOC Port: 445/TCP
   - Analisis: Worm menggunakan exploit EternalBlue...
   - Aksi SOC: Firewall block diterapkan...
   - Aksi IR: Antivirus cleaning dilakukan...
   - Pemulihan: Restart sistem, restore backup...
   - Rekomendasi: Update policy Windows...
   - Klik "Kirim Laporan"


6. **Klik "Export PDF"** → Dokumen lengkap terdownload ✅

7. Kirim Lansung dan terintegrasi dengan WA helpdesk
---

**Status: ✅ SEMUA FIELD SIAP DIGUNAKAN**
