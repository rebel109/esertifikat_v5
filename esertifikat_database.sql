-- ============================================================
-- E-Sertifikat Akreditasi UIN Raden Fatah Palembang
-- Database SQL Dump
-- Generated: 2024
-- ============================================================

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Struktur Tabel: program_studi
-- ----------------------------
DROP TABLE IF EXISTS program_studi;
CREATE TABLE program_studi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    fakultas TEXT NOT NULL,
    jenjang TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------
-- Struktur Tabel: sertifikat
-- ----------------------------
DROP TABLE IF EXISTS sertifikat;
CREATE TABLE sertifikat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prodi_id INTEGER NOT NULL,
    akreditasi TEXT NOT NULL,
    tgl_terbit DATE NOT NULL,
    tgl_berakhir DATE NOT NULL,
    nomor_sk TEXT,
    file_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prodi_id) REFERENCES program_studi(id)
);

-- ----------------------------
-- Data: program_studi
-- ----------------------------
INSERT INTO program_studi (id, nama, fakultas, jenjang, created_at) VALUES (1, 'Sistem Informasi', 'Fakultas Sains dan Teknologi', 'S1', '2026-04-23 09:04:20');
INSERT INTO program_studi (id, nama, fakultas, jenjang, created_at) VALUES (2, 'Teknik Informatika', 'Fakultas Sains dan Teknologi', 'S1', '2026-04-23 09:04:20');
INSERT INTO program_studi (id, nama, fakultas, jenjang, created_at) VALUES (3, 'Ilmu Komputer', 'Fakultas Sains dan Teknologi', 'S1', '2026-04-23 09:04:20');
INSERT INTO program_studi (id, nama, fakultas, jenjang, created_at) VALUES (4, 'Pendidikan Agama Islam', 'Fakultas Tarbiyah dan Keguruan', 'S1', '2026-04-23 09:04:20');
INSERT INTO program_studi (id, nama, fakultas, jenjang, created_at) VALUES (5, 'Manajemen Pendidikan Islam', 'Fakultas Tarbiyah dan Keguruan', 'S1', '2026-04-23 09:04:20');
INSERT INTO program_studi (id, nama, fakultas, jenjang, created_at) VALUES (6, 'Hukum Keluarga Islam', 'Fakultas Syariah dan Hukum', 'S1', '2026-04-23 09:04:20');
INSERT INTO program_studi (id, nama, fakultas, jenjang, created_at) VALUES (7, 'Hukum Ekonomi Syariah', 'Fakultas Syariah dan Hukum', 'S1', '2026-04-23 09:04:20');
INSERT INTO program_studi (id, nama, fakultas, jenjang, created_at) VALUES (8, 'Perbankan Syariah', 'Fakultas Ekonomi dan Bisnis Islam', 'S1', '2026-04-23 09:04:20');
INSERT INTO program_studi (id, nama, fakultas, jenjang, created_at) VALUES (9, 'Akuntansi Syariah', 'Fakultas Ekonomi dan Bisnis Islam', 'S1', '2026-04-23 09:04:20');
INSERT INTO program_studi (id, nama, fakultas, jenjang, created_at) VALUES (10, 'Komunikasi Penyiaran Islam', 'Fakultas Dakwah dan Komunikasi', 'S1', '2026-04-23 09:04:20');
INSERT INTO program_studi (id, nama, fakultas, jenjang, created_at) VALUES (11, 'Magister PAI', 'Pascasarjana', 'S2', '2026-04-23 09:04:20');
INSERT INTO program_studi (id, nama, fakultas, jenjang, created_at) VALUES (12, 'Doktor Ilmu Agama', 'Pascasarjana', 'S3', '2026-04-23 09:04:20');

-- ----------------------------
-- Data: sertifikat
-- ----------------------------
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (1, 1, 'B', '2010-01-15', '2015-01-15', 'SK/BAN-PT/2010/001', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (2, 1, 'B', '2015-03-20', '2020-03-20', 'SK/BAN-PT/2015/045', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (3, 1, 'A', '2020-05-10', '2025-05-10', 'SK/BAN-PT/2020/112', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (4, 2, 'C', '2012-06-01', '2017-06-01', 'SK/BAN-PT/2012/023', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (5, 2, 'B', '2017-08-15', '2022-08-15', 'SK/BAN-PT/2017/089', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (6, 2, 'B', '2022-09-01', '2027-09-01', 'SK/BAN-PT/2022/201', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (7, 3, 'B', '2015-02-10', '2020-02-10', 'SK/BAN-PT/2015/067', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (8, 3, 'A', '2020-04-20', '2025-04-20', 'SK/BAN-PT/2020/145', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (9, 4, 'A', '2010-03-05', '2015-03-05', 'SK/BAN-PT/2010/008', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (10, 4, 'A', '2015-05-12', '2020-05-12', 'SK/BAN-PT/2015/078', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (11, 4, 'Unggul', '2020-07-18', '2025-07-18', 'SK/BAN-PT/2020/189', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (12, 5, 'B', '2013-09-20', '2018-09-20', 'SK/BAN-PT/2013/056', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (13, 5, 'A', '2018-11-05', '2023-11-05', 'SK/BAN-PT/2018/134', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (14, 6, 'B', '2011-04-15', '2016-04-15', 'SK/BAN-PT/2011/034', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (15, 6, 'A', '2016-06-22', '2021-06-22', 'SK/BAN-PT/2016/098', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (16, 7, 'B', '2014-08-30', '2019-08-30', 'SK/BAN-PT/2014/071', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (17, 7, 'A', '2019-10-14', '2024-10-14', 'SK/BAN-PT/2019/167', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (18, 8, 'B', '2012-12-01', '2017-12-01', 'SK/BAN-PT/2012/045', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (19, 8, 'A', '2017-01-20', '2022-01-20', 'SK/BAN-PT/2017/012', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (20, 9, 'B', '2016-03-08', '2021-03-08', 'SK/BAN-PT/2016/045', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (21, 10, 'B', '2013-07-25', '2018-07-25', 'SK/BAN-PT/2013/089', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (22, 11, 'B', '2015-11-10', '2020-11-10', 'SK/BAN-PT/2015/123', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (23, 11, 'A', '2020-12-05', '2025-12-05', 'SK/BAN-PT/2020/234', NULL, '2026-04-23 09:04:20');
INSERT INTO sertifikat (id, prodi_id, akreditasi, tgl_terbit, tgl_berakhir, nomor_sk, file_name, created_at) VALUES (24, 12, 'B', '2018-05-30', '2023-05-30', 'SK/BAN-PT/2018/156', NULL, '2026-04-23 09:04:20');

PRAGMA foreign_keys = ON;

-- End of dump