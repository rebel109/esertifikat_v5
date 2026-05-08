# E-Sertifikat Akreditasi — UIN Raden Fatah Palembang

## Cara Menjalankan

### 1. Install dependensi
```bash
pip install flask
```

### 2. Jalankan aplikasi
```bash
python app.py
```

### 3. Buka di browser
- **Halaman Publik:** http://localhost:5000
- **Admin Login:** http://localhost:5000/admin/login

## Akun Admin (Demo)
- **Username:** admin
- **Password:** uinrf2024

## Fitur
- ✅ Halaman publik: tabel program studi & akreditasi dengan pencarian & filter
- ✅ Modal riwayat sertifikat per program studi (multi-periode)
- ✅ Download/pratinjau sertifikat dalam format HTML yang elegan
- ✅ Admin CRUD: Program Studi (tambah, edit, hapus)
- ✅ Admin CRUD: Sertifikat (tambah, edit, hapus)
- ✅ Dropdown untuk Fakultas, Jenjang, dan Akreditasi
- ✅ Date picker untuk tanggal terbit & berakhir
- ✅ Indikator status aktif/kadaluarsa otomatis
- ✅ Data contoh 12 program studi & 24 sertifikat

## Struktur File
```
esertifikat/
├── app.py                    # Flask backend + SQLite
├── templates/
│   ├── base.html             # Template dasar (navbar, CSS, JS)
│   ├── index.html            # Halaman publik
│   ├── admin_login.html      # Halaman login admin
│   ├── admin_dashboard.html  # Dashboard admin
│   ├── admin_prodi.html      # CRUD Program Studi
│   └── admin_sertifikat.html # CRUD Sertifikat
└── esertifikat.db            # Database SQLite (auto-dibuat)
```
