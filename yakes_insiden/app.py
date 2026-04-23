from flask import Flask, render_template, redirect, url_for, request, session, make_response, flash, send_file
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from werkzeug.utils import secure_filename
import json, os
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'yakes-telkom-secret-2025'

# ─── Uploads directory ────────────────────────────────────────────────────────
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ─── In-memory database (ganti dengan SQLite/PostgreSQL untuk produksi) ───────
users = {
    'admin': {'password': 'admin123', 'role': 'admin', 'nama': 'Admin IT'},
    'budi':  {'password': 'budi123',  'role': 'user',  'nama': 'Budi Santoso'},
    'siti':  {'password': 'siti123',  'role': 'user',  'nama': 'Siti Rahayu'},
}

insiden_db = [
    {
        'id': 'INC-001', 'jenis': 'Phishing SMS', 'pelapor': 'Budi Santoso',
        'username_pelapor': 'budi', 'tanggal': '2025-07-16',
        'jam': '09:15', 'lokasi': 'Kantor Pusat Bandung',
        'deskripsi': 'Menerima SMS mencurigakan yang meminta klik link dan memasukkan data login akun kesehatan.',
        'dampak': 'Akun email terancam, potensi kebocoran data pasien.',
        'tindakan_awal': 'Tidak mengklik link dan segera melaporkan ke tim IT.',
        'status': 'Selesai', 'severity': 'Tinggi',
        'catatan_admin': 'Akun diamankan, password direset, user diedukasi.',
        'petugas': 'Admin IT', 'tanggal_update': '2025-07-17'
    },
    {
        'id': 'INC-002', 'jenis': 'Worm', 'pelapor': 'Siti Rahayu',
        'username_pelapor': 'siti', 'tanggal': '2025-07-17',
        'jam': '14:30', 'lokasi': 'Ruang Server Lt.3',
        'deskripsi': 'Komputer server menunjukkan aktivitas jaringan tidak normal, CPU 100% tanpa sebab jelas.',
        'dampak': 'Kinerja server menurun drastis, layanan SIMRS terganggu 2 jam.',
        'tindakan_awal': 'Server diisolasi dari jaringan utama sementara waktu.',
        'status': 'Diproses', 'severity': 'Tinggi',
        'catatan_admin': 'Sedang dilakukan analisis forensik.',
        'petugas': 'Admin IT', 'tanggal_update': '2025-07-18'
    },
    {
        'id': 'INC-003', 'jenis': 'DoS/DDoS', 'pelapor': 'Budi Santoso',
        'username_pelapor': 'budi', 'tanggal': '2025-07-18',
        'jam': '11:00', 'lokasi': 'Infrastruktur Cloud',
        'deskripsi': 'Website portal pasien tidak dapat diakses selama 30 menit akibat lonjakan traffic mencurigakan.',
        'dampak': 'Layanan portal pasien down, sekitar 200 pengguna terdampak.',
        'tindakan_awal': 'Kontak provider hosting untuk mitigasi.',
        'status': 'Diproses', 'severity': 'Sedang',
        'catatan_admin': 'Koordinasi dengan tim jaringan.',
        'petugas': 'Admin IT', 'tanggal_update': '2025-07-18'
    },
    {
        'id': 'INC-004', 'jenis': 'Vishing', 'pelapor': 'Siti Rahayu',
        'username_pelapor': 'siti', 'tanggal': '2025-07-19',
        'jam': '16:45', 'lokasi': 'Kantor Pusat Bandung',
        'deskripsi': 'Mendapat telepon dari orang mengaku teknisi Telkom yang meminta akses remote ke komputer.',
        'dampak': 'Tidak ada dampak, permintaan ditolak.',
        'tindakan_awal': 'Menolak permintaan dan menutup telepon.',
        'status': 'Selesai', 'severity': 'Rendah',
        'catatan_admin': 'Laporan dicatat, tidak ada tindak lanjut teknis diperlukan.',
        'petugas': 'Admin IT', 'tanggal_update': '2025-07-19'
    },
    {
        'id': 'INC-005', 'jenis': 'Phishing SMS', 'pelapor': 'Budi Santoso',
        'username_pelapor': 'budi', 'tanggal': '2025-07-20',
        'jam': '08:30', 'lokasi': 'Kantor Pusat Bandung',
        'deskripsi': 'SMS massal ke nomor karyawan berisi tautan palsu berkedok promo kesehatan Telkom.',
        'dampak': 'Belum ada korban teridentifikasi, potensi phishing skala besar.',
        'tindakan_awal': 'Melaporkan nomor pengirim ke tim IT.',
        'status': 'Menunggu', 'severity': 'Tinggi',
        'catatan_admin': '',
        'petugas': '-', 'tanggal_update': '2025-07-20'
    },
]

next_id = [6]

# ─── Guides database (stored with filename, type, upload date) ────────────────
guides_db = {
    'Worm': {'filename': None, 'uploaded_date': None, 'description': 'Panduan penanganan Worm'},
    'DoS/DDoS': {'filename': None, 'uploaded_date': None, 'description': 'Panduan penanganan DoS/DDoS'},
    'Phishing': {'filename': None, 'uploaded_date': None, 'description': 'Panduan penanganan Phishing/Vishing'},
}


def login_required(f):
    """Decorator: require user to be logged in"""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Decorator: require admin role"""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Anda tidak memiliki akses ke halaman ini. Hanya admin yang dapat mengakses.', 'error')
            return redirect(url_for('user_dashboard'))
        return f(*args, **kwargs)
    return decorated


# ─── AUTH ─────────────────────────────────────────────────────────────────────
@app.route('/', methods=['GET', 'POST'])
def login():
    """Login route - direct to appropriate dashboard based on role"""
    if 'username' in session:
        return redirect(url_for('admin_dashboard') if session['role'] == 'admin' else url_for('user_dashboard'))
    error = None
    if request.method == 'POST':
        u = request.form.get('username', '').strip()
        p = request.form.get('password', '').strip()
        if u in users and users[u]['password'] == p:
            session['username'] = u
            session['role'] = users[u]['role']
            session['nama'] = users[u]['nama']
            return redirect(url_for('admin_dashboard') if users[u]['role'] == 'admin' else url_for('user_dashboard'))
        error = 'Username atau password salah.'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """Logout: clear session"""
    session.clear()
    return redirect(url_for('login'))


# ─── ADMIN ────────────────────────────────────────────────────────────────────
@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard - displays incident statistics and list"""
    total   = len(insiden_db)
    menunggu = sum(1 for i in insiden_db if i['status'] == 'Menunggu')
    diproses = sum(1 for i in insiden_db if i['status'] == 'Diproses')
    selesai  = sum(1 for i in insiden_db if i['status'] == 'Selesai')
    per_jenis = {}
    for i in insiden_db:
        per_jenis[i['jenis']] = per_jenis.get(i['jenis'], 0) + 1
    return render_template('admin_dashboard.html',
        insiden_list=sorted(insiden_db, key=lambda x: x['tanggal'], reverse=True),
        total=total, menunggu=menunggu, diproses=diproses, selesai=selesai,
        per_jenis=json.dumps(per_jenis))


@app.route('/admin/insiden/<id>')
@admin_required
def admin_detail(id):
    """Admin detail view - display incident details"""
    insiden = next((i for i in insiden_db if i['id'] == id), None)
    if not insiden:
        flash('Insiden tidak ditemukan.', 'error')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_detail.html', insiden=insiden)


@app.route('/admin/insiden/<id>/update', methods=['POST'])
@admin_required
def admin_update(id):
    """Admin update incident - modify status, severity, notes"""
    insiden = next((i for i in insiden_db if i['id'] == id), None)
    if insiden:
        insiden['status']        = request.form.get('status', insiden['status'])
        insiden['severity']      = request.form.get('severity', insiden['severity'])
        insiden['catatan_admin'] = request.form.get('catatan_admin', '')
        insiden['petugas']       = session['nama']
        insiden['tanggal_update'] = datetime.now().strftime('%Y-%m-%d')
        flash('Insiden berhasil diperbarui.', 'success')
    return redirect(url_for('admin_detail', id=id))


@app.route('/admin/insiden/<id>/pdf')
@admin_required
def export_pdf(id):
    """Export incident report as PDF using ReportLab (Windows-compatible)"""
    insiden = next((i for i in insiden_db if i['id'] == id), None)
    if not insiden:
        flash('Insiden tidak ditemukan.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if session.get('role') != 'admin':
        flash('Anda tidak memiliki akses untuk export PDF.', 'error')
        return redirect(url_for('user_dashboard'))
    
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                topMargin=0.5*inch, bottomMargin=0.5*inch,
                                leftMargin=0.75*inch, rightMargin=0.75*inch)
        
        elements = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a4d8f'),
            spaceAfter=12,
            alignment=1
        )
        elements.append(Paragraph("LAPORAN INSIDEN KEAMANAN", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        meta_data = [
            ['ID Insiden:', insiden['id']],
            ['Jenis:', insiden['jenis']],
            ['Status:', insiden['status']],
            ['Severity:', insiden['severity']],
            ['Pelapor:', insiden['pelapor']],
            ['Tanggal Laporan:', insiden['tanggal']],
            ['Jam:', insiden['jam']],
            ['Lokasi:', insiden['lokasi']],
            ['Tanggal Update:', insiden['tanggal_update']],
        ]
        
        meta_table = Table(meta_data, colWidths=[2*inch, 3.5*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("Deskripsi Insiden", styles['Heading2']))
        elements.append(Paragraph(insiden['deskripsi'], styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))
        
        elements.append(Paragraph("Dampak", styles['Heading2']))
        elements.append(Paragraph(insiden['dampak'], styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))
        
        elements.append(Paragraph("Tindakan Awal", styles['Heading2']))
        elements.append(Paragraph(insiden['tindakan_awal'], styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))
        
        if insiden.get('tim_csirt'):
            elements.append(Paragraph("Tim CSIRT", styles['Heading2']))
            elements.append(Paragraph(insiden['tim_csirt'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        if insiden.get('sistem_terdampak'):
            elements.append(Paragraph("Sistem Terdampak", styles['Heading2']))
            elements.append(Paragraph(insiden['sistem_terdampak'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        if insiden.get('ringkasan_insiden'):
            elements.append(Paragraph("Ringkasan Insiden", styles['Heading2']))
            elements.append(Paragraph(insiden['ringkasan_insiden'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        if insiden.get('kronologi'):
            elements.append(Paragraph("Kronologi", styles['Heading2']))
            elements.append(Paragraph(insiden['kronologi'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        if insiden.get('akar_masalah'):
            elements.append(Paragraph("Akar Masalah (Root Cause)", styles['Heading2']))
            elements.append(Paragraph(insiden['akar_masalah'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        # IOC Section
        if insiden.get('ioc_hash') or insiden.get('ioc_ip_domain') or insiden.get('ioc_port_media'):
            elements.append(Paragraph("Indikator (IOC / IOA)", styles['Heading2']))
            ioc_content = ""
            if insiden.get('ioc_hash'):
                ioc_content += f"<b>Hash:</b> {insiden['ioc_hash']}<br/>"
            if insiden.get('ioc_ip_domain'):
                ioc_content += f"<b>IP/Domain:</b> {insiden['ioc_ip_domain']}<br/>"
            if insiden.get('ioc_port_media'):
                ioc_content += f"<b>Port / Media:</b> {insiden['ioc_port_media']}"
            elements.append(Paragraph(ioc_content, styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        if insiden.get('analisis_teknis'):
            elements.append(Paragraph("Analisis Teknis", styles['Heading2']))
            elements.append(Paragraph(insiden['analisis_teknis'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        if insiden.get('aksi_soc'):
            elements.append(Paragraph("Aksi SOC (Detection)", styles['Heading2']))
            elements.append(Paragraph(insiden['aksi_soc'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        if insiden.get('aksi_ir'):
            elements.append(Paragraph("Aksi IR (Response)", styles['Heading2']))
            elements.append(Paragraph(insiden['aksi_ir'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        if insiden.get('pemulihan'):
            elements.append(Paragraph("Pemulihan", styles['Heading2']))
            elements.append(Paragraph(insiden['pemulihan'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        if insiden.get('rekomendasi'):
            elements.append(Paragraph("Rekomendasi", styles['Heading2']))
            elements.append(Paragraph(insiden['rekomendasi'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        if insiden['catatan_admin']:
            elements.append(Paragraph("Catatan Admin", styles['Heading2']))
            elements.append(Paragraph(insiden['catatan_admin'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        elements.append(Spacer(1, 0.3*inch))
        footer_text = f"Diproses oleh: {insiden['petugas']} | Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}"
        elements.append(Paragraph(footer_text, styles['Normal']))
        
        doc.build(elements)
        buffer.seek(0)
        
        response = make_response(buffer.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=laporan_{id}.pdf'
        return response
    
    except Exception as e:
        flash(f'Gagal generate PDF: {str(e)}', 'error')
        return redirect(url_for('admin_detail', id=id))


# ─── USER ─────────────────────────────────────────────────────────────────────
@app.route('/user')
@login_required
def user_dashboard():
    """User dashboard - display their reported incidents"""
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    my_insiden = [i for i in insiden_db if i['username_pelapor'] == session['username']]
    return render_template('user_dashboard.html',
        insiden_list=sorted(my_insiden, key=lambda x: x['tanggal'], reverse=True))


@app.route('/user/laporkan', methods=['GET', 'POST'])
@login_required
def laporkan():
    """User report incident - create new incident"""
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        new_id = f"INC-{next_id[0]:03d}"
        next_id[0] += 1
        insiden_db.append({
            'id': new_id,
            'jenis':             request.form.get('jenis'),
            'pelapor':           session['nama'],
            'username_pelapor':  session['username'],
            'tanggal':           request.form.get('tanggal'),
            'jam':               request.form.get('jam'),
            'lokasi':            request.form.get('lokasi'),
            'deskripsi':         request.form.get('deskripsi'),
            'dampak':            request.form.get('dampak'),
            'tindakan_awal':     request.form.get('tindakan_awal'),
            'tim_csirt':         request.form.get('tim_csirt', ''),
            'sistem_terdampak':  request.form.get('sistem_terdampak', ''),
            'ringkasan_insiden': request.form.get('ringkasan_insiden', ''),
            'kronologi':         request.form.get('kronologi', ''),
            'akar_masalah':      request.form.get('akar_masalah', ''),
            'ioc_hash':          request.form.get('ioc_hash', ''),
            'ioc_ip_domain':     request.form.get('ioc_ip_domain', ''),
            'ioc_port_media':    request.form.get('ioc_port_media', ''),
            'analisis_teknis':   request.form.get('analisis_teknis', ''),
            'aksi_soc':          request.form.get('aksi_soc', ''),
            'aksi_ir':           request.form.get('aksi_ir', ''),
            'pemulihan':         request.form.get('pemulihan', ''),
            'rekomendasi':       request.form.get('rekomendasi', ''),
            'status':   'Menunggu',
            'severity': request.form.get('severity', 'Sedang'),
            'catatan_admin': '',
            'petugas': '-',
            'tanggal_update': datetime.now().strftime('%Y-%m-%d'),
        })
        flash(f'Laporan {new_id} berhasil dikirim!', 'success')
        return redirect(url_for('user_dashboard'))
    return render_template('laporkan.html', today=datetime.now().strftime('%Y-%m-%d'))


@app.route('/user/insiden/<id>')
@login_required
def user_detail(id):
    """User detail view - display their incident (with ownership check)"""
    insiden = next((i for i in insiden_db if i['id'] == id), None)
    if not insiden or (session['role'] != 'admin' and insiden['username_pelapor'] != session['username']):
        flash('Anda tidak memiliki akses ke insiden ini.', 'error')
        return redirect(url_for('user_dashboard'))
    return render_template('user_detail.html', insiden=insiden)


# ─── GUIDES (Panduan) ─────────────────────────────────────────────────────────
@app.route('/guides', methods=['GET'])
@login_required
def view_guides():
    """View all available guides for users"""
    guides = guides_db
    return render_template('guides.html', guides=guides)




@app.route('/guides/<guide_type>/download')
@login_required
def download_guide(guide_type):
    """Download guide PDF"""
    if guide_type not in guides_db or not guides_db[guide_type]['filename']:
        flash('Panduan tidak tersedia.', 'error')
        return redirect(url_for('view_guides'))
    
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], guides_db[guide_type]['filename'])
        if not os.path.exists(filepath):
            flash('File tidak ditemukan.', 'error')
            return redirect(url_for('view_guides'))
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f"Panduan_{guide_type}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Terjadi kesalahan saat mengunduh file: {str(e)}', 'error')
        return redirect(url_for('view_guides'))


if __name__ == '__main__':
    app.run(debug=True)
