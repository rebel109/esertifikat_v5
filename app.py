from flask import (Flask, render_template, request, jsonify,
                   redirect, url_for, session, send_file, abort)
import os
import json
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import pymysql
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'uinrf-palembang-secret-2024'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# ================================================================
DB_CONFIG = {
    'host':        'localhost',
    'port':        3306,
    'user':        'root',
    'password':    '',
    'database':    'esertifikat',
    'charset':     'utf8mb4',
    'autocommit':  False,
    'cursorclass': pymysql.cursors.DictCursor,
}
# ================================================================

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER  = os.path.join(BASE_DIR, 'static', 'uploads')
SETTING_FOLDER = os.path.join(BASE_DIR, 'static', 'settings')
ALLOWED_CERT   = {'pdf', 'jpg', 'jpeg', 'png'}
ALLOWED_IMG    = {'jpg', 'jpeg', 'png', 'webp'}
TIMEOUT_MENIT  = 3

os.makedirs(UPLOAD_FOLDER,  exist_ok=True)
os.makedirs(SETTING_FOLDER, exist_ok=True)

ADMIN_FILE = os.path.join(SETTING_FOLDER, 'admins.json')

# ── admin account helpers ─────────────────────────────────────────

def _hash(password):
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def load_admins():
    """Baca daftar admin dari file JSON. Buat default jika belum ada."""
    if os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    # Default pertama kali
    default = [{'username': 'admin', 'password': _hash('uinrf2024'),
                'nama': 'Administrator', 'role': 'superadmin'}]
    save_admins(default)
    return default

def save_admins(data):
    with open(ADMIN_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def find_admin(username):
    for a in load_admins():
        if a['username'] == username:
            return a
    return None

def verify_admin(username, password):
    a = find_admin(username)
    return a and a['password'] == _hash(password)


@app.context_processor
def inject_settings():
    return dict(get_setting=get_setting)


# ── helpers ───────────────────────────────────────────────────────

def get_db():
    try:
        return pymysql.connect(**DB_CONFIG)
    except pymysql.err.OperationalError as e:
        raise RuntimeError(f"Tidak bisa koneksi MySQL: {e}")

def query(sql, params=(), one=False, commit=False):
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(sql, params)
            if commit:
                conn.commit()
                return c.lastrowid
            return c.fetchone() if one else c.fetchall()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_setting(key, default=''):
    p = os.path.join(SETTING_FOLDER, f"{key}.txt")
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return default

def set_setting(key, value):
    with open(os.path.join(SETTING_FOLDER, f"{key}.txt"), 'w', encoding='utf-8') as f:
        f.write(value)

def remove_file(folder, fname):
    if fname:
        p = os.path.join(folder, fname)
        if os.path.exists(p):
            os.remove(p)

def save_cert_file(file_obj, prefix='sert'):
    if file_obj and getattr(file_obj, 'filename', None):
        ext = file_obj.filename.rsplit('.', 1)[-1].lower()
        if ext in ALLOWED_CERT:
            fname = secure_filename(f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}")
            file_obj.save(os.path.join(UPLOAD_FOLDER, fname))
            return fname
    return None

def save_img_file(file_obj, save_name):
    if file_obj and getattr(file_obj, 'filename', None):
        ext = file_obj.filename.rsplit('.', 1)[-1].lower()
        if ext in ALLOWED_IMG:
            # Hapus semua file lama dengan nama dasar yang sama
            for f in os.listdir(SETTING_FOLDER):
                if f.startswith(f"{save_name}."):
                    os.remove(os.path.join(SETTING_FOLDER, f))
            fname = f"{save_name}.{ext}"
            file_obj.save(os.path.join(SETTING_FOLDER, fname))
            return fname
    return None

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        # Cek idle timeout
        last = session.get('last_activity')
        if last:
            idle = datetime.now() - datetime.fromisoformat(last)
            if idle > timedelta(minutes=TIMEOUT_MENIT):
                session.clear()
                return redirect(url_for('admin_login', timeout=1))
        session['last_activity'] = datetime.now().isoformat()
        return f(*args, **kwargs)
    return decorated


# ── TEST DB ───────────────────────────────────────────────────────

@app.route('/test-db')
def test_db():
    hasil = []
    try:
        conn = get_db()
        hasil.append("✅ Koneksi MySQL berhasil!")
        with conn.cursor() as c:
            c.execute("SELECT COUNT(*) AS n FROM program_studi")
            hasil.append(f"✅ Tabel program_studi: {c.fetchone()['n']} baris")
            c.execute("SELECT COUNT(*) AS n FROM sertifikat")
            hasil.append(f"✅ Tabel sertifikat: {c.fetchone()['n']} baris")
        conn.close()
        hasil.append("✅ Semua OK!")
    except Exception as e:
        hasil.append(f"❌ ERROR: {e}")
    return "<br>".join(hasil) + "<br><br><a href='/'>← Kembali</a>"


# ── PUBLIC ────────────────────────────────────────────────────────

@app.route('/')
def index():
    data = query('''
        SELECT ps.id, ps.nama, ps.fakultas, ps.jenjang,
               s.akreditasi,
               DATE_FORMAT(s.tgl_terbit,   '%%Y-%%m-%%d') AS tgl_terbit,
               DATE_FORMAT(s.tgl_berakhir, '%%Y-%%m-%%d') AS tgl_berakhir,
               s.nomor_sk,
               (SELECT COUNT(*) FROM sertifikat WHERE prodi_id = ps.id) AS jumlah_sertifikat
        FROM program_studi ps
        LEFT JOIN sertifikat s ON s.id = (
            SELECT id FROM sertifikat WHERE prodi_id = ps.id
            ORDER BY tgl_berakhir DESC LIMIT 1
        )
        ORDER BY ps.fakultas, ps.nama
    ''')
    return render_template('index.html', data=data)

@app.route('/download/<int:sid>')
def download_sertifikat(sid):
    s = query('''
        SELECT s.id, s.akreditasi, s.file_name, s.nomor_sk,
               DATE_FORMAT(s.tgl_terbit,   '%%Y-%%m-%%d') AS tgl_terbit,
               DATE_FORMAT(s.tgl_berakhir, '%%Y-%%m-%%d') AS tgl_berakhir,
               ps.nama, ps.fakultas, ps.jenjang
        FROM sertifikat s JOIN program_studi ps ON s.prodi_id=ps.id
        WHERE s.id=%s
    ''', (sid,), one=True)
    if not s:
        return "Tidak ditemukan", 404
    if s['file_name']:
        fp = os.path.join(UPLOAD_FOLDER, s['file_name'])
        if os.path.exists(fp):
            return send_file(fp, as_attachment=False)
    return generate_cert_html(s), 200, {'Content-Type': 'text/html; charset=utf-8'}

@app.route('/file/<int:sid>')
def view_file(sid):
    row = query("SELECT file_name FROM sertifikat WHERE id=%s", (sid,), one=True)
    if not row or not row['file_name']:
        abort(404)
    fp = os.path.join(UPLOAD_FOLDER, row['file_name'])
    if not os.path.exists(fp):
        abort(404)
    return send_file(fp, as_attachment=False)

@app.route('/api/sertifikat/<int:prodi_id>')
def api_sertifikat(prodi_id):
    rows = query('''
        SELECT id, prodi_id, akreditasi,
               DATE_FORMAT(tgl_terbit,   '%%Y-%%m-%%d') AS tgl_terbit,
               DATE_FORMAT(tgl_berakhir, '%%Y-%%m-%%d') AS tgl_berakhir,
               nomor_sk, file_name
        FROM sertifikat WHERE prodi_id=%s ORDER BY tgl_terbit
    ''', (prodi_id,))
    for r in rows:
        r['has_file'] = bool(r['file_name'] and
                             os.path.exists(os.path.join(UPLOAD_FOLDER, r['file_name'])))
    return jsonify(rows)

@app.route('/static/settings/<path:filename>')
def settings_file(filename):
    fp = os.path.join(SETTING_FOLDER, filename)
    if not os.path.exists(fp):
        abort(404)
    return send_file(fp)


# ── ADMIN AUTH ────────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    timeout    = request.args.get('timeout')
    pw_changed = request.args.get('pw_changed')
    error      = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if verify_admin(username, password):
            session.clear()
            session['admin']         = True
            session['username']      = username
            session['last_activity'] = datetime.now().isoformat()
            return redirect(url_for('admin_dashboard'))
        error = 'Username atau password salah!'
    return render_template('admin_login.html', error=error,
                           timeout=timeout, pw_changed=pw_changed,
                           timeout_menit=TIMEOUT_MENIT)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))


# ── ADMIN DASHBOARD ───────────────────────────────────────────────

@app.route('/admin')
@admin_required
def admin_dashboard():
    total_prodi      = query("SELECT COUNT(*) AS n FROM program_studi", one=True)['n']
    total_sertifikat = query("SELECT COUNT(*) AS n FROM sertifikat",    one=True)['n']
    aktif            = query("SELECT COUNT(*) AS n FROM sertifikat WHERE tgl_berakhir >= CURDATE()", one=True)['n']

    # Data sertifikat terbaru per program studi
    latest_certificates = query('''
        SELECT ps.nama, ps.fakultas, ps.jenjang, s.akreditasi,
               DATE_FORMAT(s.tgl_terbit,   '%%Y-%%m-%%d') AS tgl_terbit,
               DATE_FORMAT(s.tgl_berakhir, '%%Y-%%m-%%d') AS tgl_berakhir,
               s.id AS sid, s.nomor_sk
        FROM sertifikat s
        JOIN program_studi ps ON s.prodi_id = ps.id
        INNER JOIN (
            SELECT prodi_id, MAX(created_at) as max_created, MAX(id) as max_id
            FROM sertifikat
            GROUP BY prodi_id
        ) latest ON s.prodi_id = latest.prodi_id
                      AND s.created_at = latest.max_created
                      AND s.id = latest.max_id
        ORDER BY s.akreditasi, s.tgl_berakhir DESC
    ''')

    # Kelompokkan berdasarkan akreditasi
    unggul = [cert for cert in latest_certificates if cert['akreditasi'] == 'Unggul']
    baik_sekali = [cert for cert in latest_certificates if cert['akreditasi'] == 'Baik Sekali']
    baik = [cert for cert in latest_certificates if cert['akreditasi'] == 'Baik']
    akreditasi_a = [cert for cert in latest_certificates if cert['akreditasi'] == 'A']
    akreditasi_b = [cert for cert in latest_certificates if cert['akreditasi'] == 'B']
    akreditasi_c = [cert for cert in latest_certificates if cert['akreditasi'] == 'C']

    return render_template('admin_dashboard.html',
                           total_prodi=total_prodi, total_sertifikat=total_sertifikat,
                           aktif=aktif, timeout_menit=TIMEOUT_MENIT,
                           unggul=unggul, baik_sekali=baik_sekali, baik=baik,
                           akreditasi_a=akreditasi_a, akreditasi_b=akreditasi_b, akreditasi_c=akreditasi_c)


@app.route('/admin/warnings')
@admin_required
def admin_warnings():
    warnings = query('''
        SELECT ps.nama, ps.fakultas, ps.jenjang, s.akreditasi,
               DATE_FORMAT(s.tgl_terbit,   '%%Y-%%m-%%d') AS tgl_terbit,
               DATE_FORMAT(s.tgl_berakhir, '%%Y-%%m-%%d') AS tgl_berakhir,
               s.id AS sid, s.nomor_sk,
               DATEDIFF(s.tgl_berakhir, CURDATE()) AS hari_tersisa
        FROM sertifikat s JOIN program_studi ps ON s.prodi_id=ps.id
        WHERE s.tgl_berakhir < DATE_ADD(CURDATE(), INTERVAL 1 YEAR)
          AND s.tgl_berakhir >= CURDATE()
        ORDER BY s.tgl_berakhir ASC
    ''')
    return render_template('admin_warnings.html', warnings=warnings, timeout_menit=TIMEOUT_MENIT)


# ── ADMIN PRODI ───────────────────────────────────────────────────

@app.route('/admin/prodi')
@admin_required
def admin_prodi():
    data = query('''
        SELECT ps.id, ps.nama, ps.fakultas, ps.jenjang, ps.created_at,
               COUNT(s.id) AS jml_sertifikat
        FROM program_studi ps
        LEFT JOIN sertifikat s ON s.prodi_id=ps.id
        GROUP BY ps.id, ps.nama, ps.fakultas, ps.jenjang, ps.created_at
        ORDER BY ps.fakultas, ps.nama
    ''')
    return render_template('admin_prodi.html', data=data, timeout_menit=TIMEOUT_MENIT)

@app.route('/admin/prodi/add', methods=['POST'])
@admin_required
def admin_prodi_add():
    nama     = request.form.get('nama',     '').strip()
    fakultas = request.form.get('fakultas', '').strip()
    jenjang  = request.form.get('jenjang',  '').strip()
    if nama and fakultas and jenjang:
        query("INSERT INTO program_studi (nama,fakultas,jenjang) VALUES (%s,%s,%s)",
              (nama, fakultas, jenjang), commit=True)
    return redirect(url_for('admin_prodi'))

@app.route('/admin/prodi/edit/<int:id>', methods=['POST'])
@admin_required
def admin_prodi_edit(id):
    query("UPDATE program_studi SET nama=%s,fakultas=%s,jenjang=%s WHERE id=%s",
          (request.form.get('nama','').strip(),
           request.form.get('fakultas','').strip(),
           request.form.get('jenjang','').strip(), id), commit=True)
    return redirect(url_for('admin_prodi'))

@app.route('/admin/prodi/delete/<int:id>', methods=['POST'])
@admin_required
def admin_prodi_delete(id):
    rows = query("SELECT file_name FROM sertifikat WHERE prodi_id=%s", (id,))
    for r in rows:
        remove_file(UPLOAD_FOLDER, r['file_name'])
    query("DELETE FROM sertifikat    WHERE prodi_id=%s", (id,), commit=True)
    query("DELETE FROM program_studi WHERE id=%s",       (id,), commit=True)
    return redirect(url_for('admin_prodi'))


# ── ADMIN SERTIFIKAT ──────────────────────────────────────────────

@app.route('/admin/sertifikat')
@admin_required
def admin_sertifikat():
    data = query('''
        SELECT s.id, s.prodi_id, s.akreditasi, s.file_name,
               DATE_FORMAT(s.tgl_terbit,   '%%Y-%%m-%%d') AS tgl_terbit,
               DATE_FORMAT(s.tgl_berakhir, '%%Y-%%m-%%d') AS tgl_berakhir,
               ps.nama, ps.fakultas, ps.jenjang
        FROM sertifikat s JOIN program_studi ps ON s.prodi_id=ps.id
        ORDER BY ps.nama, s.tgl_terbit
    ''')
    prodi_list = query("SELECT id,nama,jenjang,fakultas FROM program_studi ORDER BY nama")
    return render_template('admin_sertifikat.html', data=data, prodi_list=prodi_list,
                           timeout_menit=TIMEOUT_MENIT)

@app.route('/admin/sertifikat/add', methods=['POST'])
@admin_required
def admin_sertifikat_add():
    prodi_id     = request.form.get('prodi_id',     '').strip()
    akreditasi   = request.form.get('akreditasi',   '').strip()
    tgl_terbit   = request.form.get('tgl_terbit',   '').strip()
    tgl_berakhir = request.form.get('tgl_berakhir', '').strip()
    file_name    = save_cert_file(request.files.get('file_sertifikat'), f"sert_{prodi_id}")

    # Validasi backend: file wajib ada
    if not file_name:
        prodi_list = query("SELECT id,nama,jenjang,fakultas FROM program_studi ORDER BY nama")
        data = query('''
            SELECT s.id, s.prodi_id, s.akreditasi, s.file_name,
                   DATE_FORMAT(s.tgl_terbit,   '%%Y-%%m-%%d') AS tgl_terbit,
                   DATE_FORMAT(s.tgl_berakhir, '%%Y-%%m-%%d') AS tgl_berakhir,
                   ps.nama, ps.fakultas, ps.jenjang
            FROM sertifikat s JOIN program_studi ps ON s.prodi_id=ps.id
            ORDER BY ps.nama, s.tgl_terbit
        ''')
        return render_template('admin_sertifikat.html', data=data, prodi_list=prodi_list,
                               timeout_menit=TIMEOUT_MENIT,
                               tambah_error='File sertifikat wajib diupload!',
                               open_tambah=True)

    query('''INSERT INTO sertifikat (prodi_id,akreditasi,tgl_terbit,tgl_berakhir,file_name)
             VALUES (%s,%s,%s,%s,%s)''',
          (prodi_id, akreditasi, tgl_terbit, tgl_berakhir, file_name), commit=True)
    return redirect(url_for('admin_sertifikat'))

@app.route('/admin/sertifikat/edit/<int:id>', methods=['POST'])
@admin_required
def admin_sertifikat_edit(id):
    prodi_id     = request.form.get('prodi_id',     '').strip()
    akreditasi   = request.form.get('akreditasi',   '').strip()
    tgl_terbit   = request.form.get('tgl_terbit',   '').strip()
    tgl_berakhir = request.form.get('tgl_berakhir', '').strip()
    new_file     = save_cert_file(request.files.get('file_sertifikat'), f"sert_{prodi_id}")
    if new_file:
        old = query("SELECT file_name FROM sertifikat WHERE id=%s", (id,), one=True)
        remove_file(UPLOAD_FOLDER, old['file_name'] if old else None)
        query('''UPDATE sertifikat SET prodi_id=%s,akreditasi=%s,tgl_terbit=%s,
                 tgl_berakhir=%s,file_name=%s WHERE id=%s''',
              (prodi_id,akreditasi,tgl_terbit,tgl_berakhir,new_file,id), commit=True)
    else:
        query('''UPDATE sertifikat SET prodi_id=%s,akreditasi=%s,tgl_terbit=%s,
                 tgl_berakhir=%s WHERE id=%s''',
              (prodi_id,akreditasi,tgl_terbit,tgl_berakhir,id), commit=True)
    return redirect(url_for('admin_sertifikat'))

@app.route('/admin/sertifikat/delete/<int:id>', methods=['POST'])
@admin_required
def admin_sertifikat_delete(id):
    row = query("SELECT file_name FROM sertifikat WHERE id=%s", (id,), one=True)
    remove_file(UPLOAD_FOLDER, row['file_name'] if row else None)
    query("DELETE FROM sertifikat WHERE id=%s", (id,), commit=True)
    return redirect(url_for('admin_sertifikat'))


# ── ADMIN PENGATURAN ──────────────────────────────────────────────

@app.route('/admin/pengaturan')
@admin_required
def admin_pengaturan():
    admins = load_admins()
    current = session.get('username', 'admin')
    return render_template('admin_pengaturan.html',
                           timeout_menit=TIMEOUT_MENIT,
                           admins=admins,
                           current_user=current)

# ── CRUD AKUN ADMIN ───────────────────────────────────────────────

@app.route('/admin/akun/add', methods=['POST'])
@admin_required
def admin_akun_add():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    nama     = request.form.get('nama',     '').strip()
    role     = request.form.get('role',     'admin').strip()
    error    = None

    if not username or not password or not nama:
        error = 'Semua field wajib diisi!'
    elif find_admin(username):
        error = f'Username "{username}" sudah digunakan!'
    elif len(password) < 6:
        error = 'Password minimal 6 karakter!'

    if error:
        admins  = load_admins()
        current = session.get('username', 'admin')
        return render_template('admin_pengaturan.html',
                               timeout_menit=TIMEOUT_MENIT,
                               admins=admins, current_user=current,
                               akun_error=error, tab='akun')

    data = load_admins()
    data.append({'username': username, 'password': _hash(password),
                 'nama': nama, 'role': role})
    save_admins(data)
    return redirect(url_for('admin_pengaturan') + '#tab-akun')


@app.route('/admin/akun/edit/<username>', methods=['POST'])
@admin_required
def admin_akun_edit(username):
    nama         = request.form.get('nama',         '').strip()
    role         = request.form.get('role',         'admin').strip()
    new_password = request.form.get('new_password', '').strip()
    error        = None

    if not nama:
        error = 'Nama tidak boleh kosong!'
    elif new_password and len(new_password) < 6:
        error = 'Password baru minimal 6 karakter!'

    data = load_admins()
    for a in data:
        if a['username'] == username:
            a['nama'] = nama
            a['role'] = role
            if new_password:
                a['password'] = _hash(new_password)
            break

    if not error:
        save_admins(data)
    return redirect(url_for('admin_pengaturan') + '#tab-akun')


@app.route('/admin/akun/delete/<username>', methods=['POST'])
@admin_required
def admin_akun_delete(username):
    current = session.get('username', 'admin')
    # Tidak boleh hapus diri sendiri
    if username == current:
        return redirect(url_for('admin_pengaturan') + '#tab-akun')
    data = [a for a in load_admins() if a['username'] != username]
    # Minimal harus ada 1 akun
    if len(data) > 0:
        save_admins(data)
    return redirect(url_for('admin_pengaturan') + '#tab-akun')


@app.route('/admin/akun/ganti-password', methods=['POST'])
@admin_required
def admin_ganti_password():
    """Admin ganti password dirinya sendiri."""
    current      = session.get('username', 'admin')
    old_pass     = request.form.get('old_password',  '').strip()
    new_pass     = request.form.get('new_password',  '').strip()
    konfirm_pass = request.form.get('konfirm_password', '').strip()
    error = None

    if not verify_admin(current, old_pass):
        error = 'Password lama tidak sesuai!'
    elif len(new_pass) < 6:
        error = 'Password baru minimal 6 karakter!'
    elif new_pass != konfirm_pass:
        error = 'Konfirmasi password tidak cocok!'

    if not error:
        data = load_admins()
        for a in data:
            if a['username'] == current:
                a['password'] = _hash(new_pass)
                break
        save_admins(data)
        # Logout setelah ganti password
        session.clear()
        return redirect(url_for('admin_login') + '?pw_changed=1')

    admins = load_admins()
    return render_template('admin_pengaturan.html',
                           timeout_menit=TIMEOUT_MENIT,
                           admins=admins, current_user=current,
                           pw_error=error, tab='akun')

@app.route('/admin/pengaturan/logo', methods=['POST'])
@admin_required
def admin_upload_logo():
    fname = save_img_file(request.files.get('logo'), 'logo')
    if fname:
        set_setting('logo', fname)
    return redirect(url_for('admin_pengaturan'))

@app.route('/admin/pengaturan/logo/hapus', methods=['POST'])
@admin_required
def admin_hapus_logo():
    remove_file(SETTING_FOLDER, get_setting('logo'))
    set_setting('logo', '')
    return redirect(url_for('admin_pengaturan'))

@app.route('/admin/pengaturan/background', methods=['POST'])
@admin_required
def admin_upload_background():
    fname = save_img_file(request.files.get('background'), 'background')
    if fname:
        set_setting('background', fname)
    return redirect(url_for('admin_pengaturan'))

@app.route('/admin/pengaturan/background/hapus', methods=['POST'])
@admin_required
def admin_hapus_background():
    remove_file(SETTING_FOLDER, get_setting('background'))
    set_setting('background', '')
    return redirect(url_for('admin_pengaturan'))

@app.route('/admin/pengaturan/teks', methods=['POST'])
@admin_required
def admin_simpan_teks():
    set_setting('site_title',    request.form.get('site_title',    '').strip())
    set_setting('site_subtitle', request.form.get('site_subtitle', '').strip())
    return redirect(url_for('admin_pengaturan'))


# ── CERT HTML ─────────────────────────────────────────────────────

def generate_cert_html(s):
    col = {'Unggul':'#1a5c38','A':'#1a3a5c','B':'#2d4a1e','C':'#5c3a1a',
           'Baik Sekali':'#1a5c38','Baik':'#2d4a1e'}.get(s['akreditasi'], '#1a3a5c')
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Sertifikat — {s['nama']}</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#f5f0e8;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:'Crimson Text',serif}}
.cert{{width:794px;min-height:562px;background:#fff;border:3px solid {col};position:relative;padding:40px;box-shadow:0 0 40px rgba(0,0,0,.2)}}
.cert::before{{content:'';position:absolute;inset:8px;border:1px solid {col};opacity:.4;pointer-events:none}}
.hdr{{text-align:center;border-bottom:2px solid {col};padding-bottom:20px;margin-bottom:20px}}
.lr{{display:flex;align-items:center;justify-content:center;gap:16px;margin-bottom:12px}}
.logo{{width:70px;height:70px;background:{col};border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:24px;font-family:'Cinzel',serif;font-weight:900}}
h1{{font-family:'Cinzel',serif;font-size:13px;color:{col};letter-spacing:3px;text-transform:uppercase}}
h2{{font-family:'Cinzel',serif;font-size:11px;color:#666;letter-spacing:2px;margin-top:4px}}
.ttl{{font-family:'Cinzel',serif;font-size:22px;color:{col};text-align:center;margin:16px 0 8px;letter-spacing:2px}}
.sub{{text-align:center;color:#888;font-size:13px;margin-bottom:20px}}
.bdy{{text-align:center;font-size:15px;color:#333;line-height:2}}
.prodi{{font-family:'Cinzel',serif;font-size:26px;color:{col};font-weight:700;display:block;margin:10px 0 4px}}
.akr{{display:inline-block;background:{col};color:#fff;font-family:'Cinzel',serif;font-size:36px;font-weight:900;padding:12px 40px;margin:16px 0;letter-spacing:4px;border-radius:4px}}
.meta{{display:flex;justify-content:space-around;margin-top:24px;padding-top:20px;border-top:1px solid #ddd}}
.mi{{text-align:center}}.ml{{font-size:11px;color:#999;letter-spacing:2px;text-transform:uppercase}}
.mv{{font-size:14px;color:#333;font-weight:600;margin-top:4px}}
.wm{{position:absolute;font-family:'Cinzel',serif;font-size:80px;color:rgba(0,0,0,.03);top:50%;left:50%;transform:translate(-50%,-50%) rotate(-30deg);white-space:nowrap;pointer-events:none}}
.ftr{{text-align:center;margin-top:16px;font-size:11px;color:#aaa}}
@media print{{body{{background:none}}.cert{{box-shadow:none}}}}
</style></head><body>
<div class="cert"><div class="wm">BAN-PT</div>
<div class="hdr"><div class="lr"><div class="logo">UIN</div>
<div><h1>Universitas Islam Negeri Raden Fatah Palembang</h1>
<h2>Sertifikat Akreditasi Program Studi &mdash; BAN-PT</h2></div></div></div>
<div class="ttl">SERTIFIKAT AKREDITASI</div><div class="sub">Badan Akreditasi Nasional Perguruan Tinggi</div>
<div class="bdy">menyatakan bahwa<br><span class="prodi">{s['nama']}</span>
{s['jenjang']} &mdash; {s['fakultas']}<br>telah mendapatkan peringkat akreditasi<br>
<span class="akr">{s['akreditasi']}</span></div>
<div class="meta">
<div class="mi"><div class="ml">Nomor SK</div><div class="mv">{s['nomor_sk'] or '-'}</div></div>
<div class="mi"><div class="ml">Tanggal Terbit</div><div class="mv">{s['tgl_terbit']}</div></div>
<div class="mi"><div class="ml">Berlaku Hingga</div><div class="mv">{s['tgl_berakhir']}</div></div>
</div>
<div class="ftr">Dokumen ini diterbitkan secara elektronik oleh Sistem E-Sertifikat UIN Raden Fatah Palembang</div>
</div></body></html>"""


import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)