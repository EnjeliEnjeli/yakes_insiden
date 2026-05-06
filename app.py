"""
Sistem Pelaporan Insiden Keamanan Siber — Yakes Telkom
Flask Application

Flow: Karyawan → Login → Isi Form → Generate PDF → Kirim WA Helpdesk → Terkirim
"""

import os
import json
from datetime import datetime
from io import BytesIO
from functools import wraps
from urllib.parse import quote

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, send_file
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# ReportLab for PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# ═══════════════════════════════════════════════════════════════
# APP CONFIGURATION
# ═══════════════════════════════════════════════════════════════
app = Flask(__name__)
app.secret_key = 'yakes-telkom-insiden-secret-key-2024'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'insiden.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PDF_FOLDER'] = os.path.join(basedir, 'uploads', 'pdf')
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads', 'guides')

os.makedirs(app.config['PDF_FOLDER'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

db = SQLAlchemy(app)

# WhatsApp Helpdesk Number (international format tanpa +)
WA_HELPDESK_NUMBER = '6285397175128'

# ═══════════════════════════════════════════════════════════════
# DATABASE MODELS
# ═══════════════════════════════════════════════════════════════
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    laporan = db.relationship('LaporanInsiden', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class LaporanInsiden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomor_insiden = db.Column(db.String(20), unique=True, nullable=False)
    # Step 1
    jenis_insiden = db.Column(db.String(50), nullable=False)
    # Step 2
    tanggal = db.Column(db.String(20), nullable=False)
    jam = db.Column(db.String(10), nullable=False)
    lokasi = db.Column(db.String(100), nullable=False)
    tim_csirt = db.Column(db.String(100))
    sistem_terdampak = db.Column(db.String(200))
    tingkat_keparahan = db.Column(db.String(20), nullable=False)
    deskripsi_kejadian = db.Column(db.Text, nullable=False)
    ringkasan_insiden = db.Column(db.Text)
    kronologi = db.Column(db.Text)
    # Step 3
    dampak = db.Column(db.Text)
    tindakan_awal = db.Column(db.Text)
    akar_masalah = db.Column(db.Text)
    ioc_hash = db.Column(db.String(200))
    ioc_ip_domain = db.Column(db.String(200))
    ioc_port_media = db.Column(db.String(200))
    analisis_teknis = db.Column(db.Text)
    aksi_soc = db.Column(db.Text)
    aksi_ir = db.Column(db.Text)
    pemulihan = db.Column(db.Text)
    rekomendasi = db.Column(db.Text)
    # Meta
    status = db.Column(db.String(20), default='Draft')
    pdf_filename = db.Column(db.String(200))
    pelapor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Guides (static data)
guides_db = {
    'Worm': {'filename': None, 'uploaded_date': None, 'description': 'Panduan penanganan Worm'},
    'DoS/DDoS': {'filename': None, 'uploaded_date': None, 'description': 'Panduan penanganan DoS/DDoS'},
    'Phishing': {'filename': None, 'uploaded_date': None, 'description': 'Panduan penanganan Phishing/Vishing'},
}

# ═══════════════════════════════════════════════════════════════
# DECORATORS
# ═══════════════════════════════════════════════════════════════
def login_required(f):
    """Decorator: require user to be logged in"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════
def generate_nomor_insiden():
    """Generate auto-increment incident number like INC-0001"""
    last = LaporanInsiden.query.order_by(LaporanInsiden.id.desc()).first()
    next_num = (last.id + 1) if last else 1
    return f"INC-{next_num:04d}"


def generate_wa_link(laporan):
    """Generate wa.me link with pre-filled message"""
    user = db.session.get(User, laporan.pelapor_id)
    nama = user.nama if user else '-'

    message = (
        f"📋 *LAPORAN INSIDEN KEAMANAN SIBER*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 No: {laporan.nomor_insiden}\n"
        f"⚠️ Jenis: {laporan.jenis_insiden}\n"
        f"🔴 Keparahan: {laporan.tingkat_keparahan}\n"
        f"👤 Pelapor: {nama}\n"
        f"📅 Tanggal: {laporan.tanggal}, {laporan.jam} WIB\n"
        f"📍 Lokasi: {laporan.lokasi}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 Deskripsi:\n{laporan.deskripsi_kejadian}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Mohon segera ditindaklanjuti. File PDF laporan akan dikirim menyusul._"
    )
    return f"https://wa.me/{WA_HELPDESK_NUMBER}?text={quote(message)}"


def generate_pdf(laporan):
    """Generate PDF report and save to uploads/pdf/"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
        leftMargin=2*cm, rightMargin=2*cm
    )

    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Heading1'],
        fontSize=16, textColor=colors.HexColor('#1d4ed8'),
        spaceAfter=6, alignment=1
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=9, textColor=colors.HexColor('#64748b'),
        alignment=1, spaceAfter=20
    )
    section_style = ParagraphStyle(
        'SectionTitle', parent=styles['Heading2'],
        fontSize=12, textColor=colors.HexColor('#1e293b'),
        spaceAfter=8, spaceBefore=16
    )
    normal_style = ParagraphStyle(
        'CustomNormal', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#334155'),
        leading=14, spaceAfter=6
    )
    footer_style = ParagraphStyle(
        'Footer', parent=styles['Normal'],
        fontSize=8, textColor=colors.HexColor('#94a3b8')
    )

    # Title
    elements.append(Paragraph("LAPORAN INSIDEN KEAMANAN SIBER", title_style))
    elements.append(Paragraph("Yakes Telkom · Digital Healthcare IT Operation", subtitle_style))
    elements.append(Spacer(1, 0.3*cm))

    # Info table
    user = db.session.get(User, laporan.pelapor_id)
    nama = user.nama if user else '-'

    meta_data = [
        ['Nomor Insiden', laporan.nomor_insiden],
        ['Jenis Insiden', laporan.jenis_insiden],
        ['Tingkat Keparahan', laporan.tingkat_keparahan],
        ['Pelapor', nama],
        ['Tanggal Kejadian', f"{laporan.tanggal}, pukul {laporan.jam} WIB"],
        ['Lokasi', laporan.lokasi],
    ]
    if laporan.tim_csirt:
        meta_data.append(['Tim CSIRT', laporan.tim_csirt])
    if laporan.sistem_terdampak:
        meta_data.append(['Sistem Terdampak', laporan.sistem_terdampak])

    meta_table = Table(meta_data, colWidths=[5*cm, 11*cm])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 0.5*cm))

    # Content sections
    sections = [
        ('Deskripsi Kejadian', laporan.deskripsi_kejadian),
        ('Ringkasan Insiden', laporan.ringkasan_insiden),
        ('Kronologi', laporan.kronologi),
        ('Dampak', laporan.dampak),
        ('Tindakan Awal', laporan.tindakan_awal),
        ('Akar Masalah (Root Cause)', laporan.akar_masalah),
        ('Analisis Teknis', laporan.analisis_teknis),
        ('Aksi SOC (Detection)', laporan.aksi_soc),
        ('Aksi IR (Response)', laporan.aksi_ir),
        ('Pemulihan', laporan.pemulihan),
        ('Rekomendasi', laporan.rekomendasi),
    ]
    for title, content in sections:
        if content:
            elements.append(Paragraph(title, section_style))
            elements.append(Paragraph(str(content), normal_style))

    # IOC
    if laporan.ioc_hash or laporan.ioc_ip_domain or laporan.ioc_port_media:
        elements.append(Paragraph("Indikator (IOC / IOA)", section_style))
        ioc = ""
        if laporan.ioc_hash:
            ioc += f"<b>Hash:</b> {laporan.ioc_hash}<br/>"
        if laporan.ioc_ip_domain:
            ioc += f"<b>IP/Domain:</b> {laporan.ioc_ip_domain}<br/>"
        if laporan.ioc_port_media:
            ioc += f"<b>Port/Media:</b> {laporan.ioc_port_media}"
        elements.append(Paragraph(ioc, normal_style))

    # Footer
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(
        f"Dicetak: {datetime.now().strftime('%d %B %Y, %H:%M')} WIB", footer_style
    ))
    elements.append(Paragraph(
        "Dokumen ini dibuat secara otomatis oleh Sistem Pelaporan Insiden Yakes Telkom.",
        footer_style
    ))

    doc.build(elements)

    # Save file
    pdf_filename = f"laporan_{laporan.nomor_insiden.replace('-','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_path = os.path.join(app.config['PDF_FOLDER'], pdf_filename)
    with open(pdf_path, 'wb') as f:
        f.write(buffer.getvalue())

    return pdf_filename


# ═══════════════════════════════════════════════════════════════
# ROUTES — AUTH
# ═══════════════════════════════════════════════════════════════
@app.route('/', methods=['GET', 'POST'])
def login():
    """Login route"""
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['nama'] = user.nama
            return redirect(url_for('user_dashboard'))
        error = 'Username atau password salah.'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """Logout: clear session"""
    session.clear()
    return redirect(url_for('login'))


# ═══════════════════════════════════════════════════════════════
# ROUTES — DASHBOARD
# ═══════════════════════════════════════════════════════════════
@app.route('/dashboard')
@login_required
def user_dashboard():
    """Dashboard - display user's reported incidents"""
    laporan_list = LaporanInsiden.query.filter_by(
        pelapor_id=session['user_id']
    ).order_by(LaporanInsiden.created_at.desc()).all()
    return render_template('user_dashboard.html', laporan_list=laporan_list)


# ═══════════════════════════════════════════════════════════════
# ROUTES — FORM PELAPORAN (3 STEPS)
# ═══════════════════════════════════════════════════════════════
@app.route('/laporkan', methods=['GET', 'POST'])
@login_required
def laporkan_step1():
    """Step 1: Pilih Jenis Insiden"""
    if request.method == 'POST':
        jenis = request.form.get('jenis_insiden')
        if not jenis:
            flash('Pilih jenis insiden!', 'warning')
            return render_template('laporkan.html', step=1)
        session['lapor'] = {'jenis_insiden': jenis}
        return redirect(url_for('laporkan_step2'))
    return render_template('laporkan.html', step=1)


@app.route('/laporkan/step2', methods=['GET', 'POST'])
@login_required
def laporkan_step2():
    """Step 2: Detail Kejadian"""
    if 'lapor' not in session:
        return redirect(url_for('laporkan_step1'))
    if request.method == 'POST':
        data = session['lapor']
        data.update({
            'tanggal': request.form.get('tanggal'),
            'jam': request.form.get('jam'),
            'lokasi': request.form.get('lokasi'),
            'tim_csirt': request.form.get('tim_csirt'),
            'sistem_terdampak': request.form.get('sistem_terdampak'),
            'tingkat_keparahan': request.form.get('tingkat_keparahan'),
            'deskripsi_kejadian': request.form.get('deskripsi_kejadian'),
            'ringkasan_insiden': request.form.get('ringkasan_insiden'),
            'kronologi': request.form.get('kronologi'),
        })
        session['lapor'] = data
        return redirect(url_for('laporkan_step3'))
    return render_template('laporkan.html', step=2, data=session.get('lapor', {}))


@app.route('/laporkan/step3', methods=['GET', 'POST'])
@login_required
def laporkan_step3():
    """Step 3: Analisis & Submit → Generate PDF → Konfirmasi"""
    if 'lapor' not in session:
        return redirect(url_for('laporkan_step1'))

    if request.method == 'POST':
        data = session['lapor']
        data.update({
            'dampak': request.form.get('dampak'),
            'tindakan_awal': request.form.get('tindakan_awal'),
            'akar_masalah': request.form.get('akar_masalah'),
            'ioc_hash': request.form.get('ioc_hash'),
            'ioc_ip_domain': request.form.get('ioc_ip_domain'),
            'ioc_port_media': request.form.get('ioc_port_media'),
            'analisis_teknis': request.form.get('analisis_teknis'),
            'aksi_soc': request.form.get('aksi_soc'),
            'aksi_ir': request.form.get('aksi_ir'),
            'pemulihan': request.form.get('pemulihan'),
            'rekomendasi': request.form.get('rekomendasi'),
        })

        # Save to database
        nomor = generate_nomor_insiden()
        laporan = LaporanInsiden(
            nomor_insiden=nomor,
            jenis_insiden=data.get('jenis_insiden'),
            tanggal=data.get('tanggal'),
            jam=data.get('jam'),
            lokasi=data.get('lokasi'),
            tim_csirt=data.get('tim_csirt'),
            sistem_terdampak=data.get('sistem_terdampak'),
            tingkat_keparahan=data.get('tingkat_keparahan'),
            deskripsi_kejadian=data.get('deskripsi_kejadian'),
            ringkasan_insiden=data.get('ringkasan_insiden'),
            kronologi=data.get('kronologi'),
            dampak=data.get('dampak'),
            tindakan_awal=data.get('tindakan_awal'),
            akar_masalah=data.get('akar_masalah'),
            ioc_hash=data.get('ioc_hash'),
            ioc_ip_domain=data.get('ioc_ip_domain'),
            ioc_port_media=data.get('ioc_port_media'),
            analisis_teknis=data.get('analisis_teknis'),
            aksi_soc=data.get('aksi_soc'),
            aksi_ir=data.get('aksi_ir'),
            pemulihan=data.get('pemulihan'),
            rekomendasi=data.get('rekomendasi'),
            pelapor_id=session['user_id'],
            status='Draft'
        )
        db.session.add(laporan)
        db.session.commit()

        # Generate PDF
        try:
            pdf_filename = generate_pdf(laporan)
            laporan.pdf_filename = pdf_filename
            laporan.status = 'PDF Generated'
            db.session.commit()
        except Exception as e:
            flash(f'Laporan tersimpan, tapi gagal generate PDF: {str(e)}', 'warning')

        session.pop('lapor', None)
        return redirect(url_for('konfirmasi', id=laporan.id))

    return render_template('laporkan.html', step=3, data=session.get('lapor', {}))


# ═══════════════════════════════════════════════════════════════
# ROUTES — KONFIRMASI & PDF
# ═══════════════════════════════════════════════════════════════
@app.route('/konfirmasi/<int:id>')
@login_required
def konfirmasi(id):
    """Confirmation page after report submission"""
    laporan = LaporanInsiden.query.get_or_404(id)
    if laporan.pelapor_id != session['user_id']:
        flash('Anda tidak memiliki akses.', 'error')
        return redirect(url_for('user_dashboard'))
    wa_link = generate_wa_link(laporan)
    return render_template('konfirmasi.html', laporan=laporan, wa_link=wa_link)


@app.route('/download-pdf/<int:id>')
@login_required
def download_pdf(id):
    """Download generated PDF"""
    from flask import make_response

    laporan = LaporanInsiden.query.get_or_404(id)
    if laporan.pelapor_id != session['user_id']:
        flash('Anda tidak memiliki akses.', 'error')
        return redirect(url_for('user_dashboard'))
    if not laporan.pdf_filename:
        flash('PDF belum tersedia.', 'error')
        return redirect(url_for('user_dashboard'))

    pdf_path = os.path.join(app.config['PDF_FOLDER'], laporan.pdf_filename)
    if not os.path.exists(pdf_path):
        flash('File PDF tidak ditemukan.', 'error')
        return redirect(url_for('user_dashboard'))

    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()

    filename = f"Laporan_{laporan.nomor_insiden}.pdf"
    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.headers['Content-Length'] = len(pdf_data)
    return response


@app.route('/mark-sent/<int:id>', methods=['POST'])
@login_required
def mark_sent(id):
    """Mark report as sent to helpdesk"""
    laporan = LaporanInsiden.query.get_or_404(id)
    if laporan.pelapor_id != session['user_id']:
        flash('Anda tidak memiliki akses.', 'error')
        return redirect(url_for('user_dashboard'))
    laporan.status = 'Terkirim'
    db.session.commit()
    flash('Status laporan diperbarui: Terkirim ke Helpdesk.', 'success')
    return redirect(url_for('user_dashboard'))


# ═══════════════════════════════════════════════════════════════
# ROUTES — DETAIL LAPORAN
# ═══════════════════════════════════════════════════════════════
@app.route('/laporan/<int:id>')
@login_required
def user_detail(id):
    """Detail view of a report"""
    laporan = LaporanInsiden.query.get_or_404(id)
    if laporan.pelapor_id != session['user_id']:
        flash('Anda tidak memiliki akses.', 'error')
        return redirect(url_for('user_dashboard'))
    wa_link = generate_wa_link(laporan)
    return render_template('user_detail.html', laporan=laporan, wa_link=wa_link)


# ═══════════════════════════════════════════════════════════════
# ROUTES — GUIDES
# ═══════════════════════════════════════════════════════════════
@app.route('/guides')
@login_required
def view_guides():
    """View all available guides"""
    return render_template('guides.html', guides=guides_db)


@app.route('/guides/<guide_type>/download')
@login_required
def download_guide(guide_type):
    """Download a guide PDF"""
    if guide_type not in guides_db or not guides_db[guide_type]['filename']:
        flash('Panduan tidak tersedia.', 'error')
        return redirect(url_for('view_guides'))
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], guides_db[guide_type]['filename'])
    if not os.path.exists(filepath):
        flash('File tidak ditemukan.', 'error')
        return redirect(url_for('view_guides'))
    return send_file(
        filepath, as_attachment=True,
        download_name=f"Panduan_{guide_type}.pdf",
        mimetype='application/pdf'
    )


# ═══════════════════════════════════════════════════════════════
# DATABASE INIT & SEED
# ═══════════════════════════════════════════════════════════════
def init_db():
    """Create tables and seed default users"""
    with app.app_context():
        db.create_all()
        # Seed default users if empty
        if User.query.count() == 0:
            default_users = [
                {'username': 'karyawan1', 'password': 'karyawan123', 'nama': 'Ahmad Fauzi'},
                {'username': 'karyawan2', 'password': 'karyawan123', 'nama': 'Siti Nurhaliza'},
                {'username': 'budi', 'password': 'budi123', 'nama': 'Budi Santoso'},
            ]
            for u in default_users:
                user = User(username=u['username'], nama=u['nama'])
                user.set_password(u['password'])
                db.session.add(user)
            db.session.commit()
            print("[OK] Database initialized with default users:")
            for u in default_users:
                print(f"   - {u['username']} / {u['password']}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
