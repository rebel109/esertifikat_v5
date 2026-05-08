-- ============================================================
-- E-Sertifikat Akreditasi UIN Raden Fatah Palembang
-- File SQL untuk MySQL / phpMyAdmin / XAMPP
-- Cara import: phpMyAdmin → pilih database esertifikat → Import
-- ============================================================

SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Tabel: program_studi
-- ----------------------------
DROP TABLE IF EXISTS `program_studi`;

CREATE TABLE `program_studi` (
  `id`         INT(11)      NOT NULL AUTO_INCREMENT,
  `nama`       VARCHAR(255) NOT NULL,
  `fakultas`   VARCHAR(255) NOT NULL,
  `jenjang`    VARCHAR(10)  NOT NULL,
  `created_at` TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Tabel: sertifikat
-- ----------------------------
DROP TABLE IF EXISTS `sertifikat`;

CREATE TABLE `sertifikat` (
  `id`           INT(11)      NOT NULL AUTO_INCREMENT,
  `prodi_id`     INT(11)      NOT NULL,
  `akreditasi`   VARCHAR(50)  NOT NULL,
  `tgl_terbit`   DATE         NOT NULL,
  `tgl_berakhir` DATE         NOT NULL,
  `nomor_sk`     VARCHAR(100) DEFAULT NULL,
  `file_name`    VARCHAR(255) DEFAULT NULL,
  `created_at`   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_prodi_id` (`prodi_id`),
  CONSTRAINT `fk_prodi_id`
    FOREIGN KEY (`prodi_id`) REFERENCES `program_studi` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Data: program_studi
-- ----------------------------
INSERT INTO `program_studi` (`id`, `nama`, `fakultas`, `jenjang`) VALUES
(1,  'Sistem Informasi',           'Fakultas Sains dan Teknologi',      'S1'),
(2,  'Teknik Informatika',         'Fakultas Sains dan Teknologi',      'S1'),
(3,  'Ilmu Komputer',              'Fakultas Sains dan Teknologi',      'S1'),
(4,  'Pendidikan Agama Islam',     'Fakultas Tarbiyah dan Keguruan',    'S1'),
(5,  'Manajemen Pendidikan Islam', 'Fakultas Tarbiyah dan Keguruan',    'S1'),
(6,  'Hukum Keluarga Islam',       'Fakultas Syariah dan Hukum',        'S1'),
(7,  'Hukum Ekonomi Syariah',      'Fakultas Syariah dan Hukum',        'S1'),
(8,  'Perbankan Syariah',          'Fakultas Ekonomi dan Bisnis Islam', 'S1'),
(9,  'Akuntansi Syariah',          'Fakultas Ekonomi dan Bisnis Islam', 'S1'),
(10, 'Komunikasi Penyiaran Islam', 'Fakultas Dakwah dan Komunikasi',    'S1'),
(11, 'Magister PAI',               'Pascasarjana',                      'S2'),
(12, 'Doktor Ilmu Agama',          'Pascasarjana',                      'S3');

-- ----------------------------
-- Data: sertifikat
-- ----------------------------
INSERT INTO `sertifikat` (`id`, `prodi_id`, `akreditasi`, `tgl_terbit`, `tgl_berakhir`, `nomor_sk`) VALUES
(1,  1,  'B',      '2010-01-15', '2015-01-15', 'SK/BAN-PT/2010/001'),
(2,  1,  'B',      '2015-03-20', '2020-03-20', 'SK/BAN-PT/2015/045'),
(3,  1,  'A',      '2020-05-10', '2025-05-10', 'SK/BAN-PT/2020/112'),
(4,  2,  'C',      '2012-06-01', '2017-06-01', 'SK/BAN-PT/2012/023'),
(5,  2,  'B',      '2017-08-15', '2022-08-15', 'SK/BAN-PT/2017/089'),
(6,  2,  'B',      '2022-09-01', '2027-09-01', 'SK/BAN-PT/2022/201'),
(7,  3,  'B',      '2015-02-10', '2020-02-10', 'SK/BAN-PT/2015/067'),
(8,  3,  'A',      '2020-04-20', '2025-04-20', 'SK/BAN-PT/2020/145'),
(9,  4,  'A',      '2010-03-05', '2015-03-05', 'SK/BAN-PT/2010/008'),
(10, 4,  'A',      '2015-05-12', '2020-05-12', 'SK/BAN-PT/2015/078'),
(11, 4,  'Unggul', '2020-07-18', '2025-07-18', 'SK/BAN-PT/2020/189'),
(12, 5,  'B',      '2013-09-20', '2018-09-20', 'SK/BAN-PT/2013/056'),
(13, 5,  'A',      '2018-11-05', '2023-11-05', 'SK/BAN-PT/2018/134'),
(14, 6,  'B',      '2011-04-15', '2016-04-15', 'SK/BAN-PT/2011/034'),
(15, 6,  'A',      '2016-06-22', '2021-06-22', 'SK/BAN-PT/2016/098'),
(16, 7,  'B',      '2014-08-30', '2019-08-30', 'SK/BAN-PT/2014/071'),
(17, 7,  'A',      '2019-10-14', '2024-10-14', 'SK/BAN-PT/2019/167'),
(18, 8,  'B',      '2012-12-01', '2017-12-01', 'SK/BAN-PT/2012/045'),
(19, 8,  'A',      '2017-01-20', '2022-01-20', 'SK/BAN-PT/2017/012'),
(20, 9,  'B',      '2016-03-08', '2021-03-08', 'SK/BAN-PT/2016/045'),
(21, 10, 'B',      '2013-07-25', '2018-07-25', 'SK/BAN-PT/2013/089'),
(22, 11, 'B',      '2015-11-10', '2020-11-10', 'SK/BAN-PT/2015/123'),
(23, 11, 'A',      '2020-12-05', '2025-12-05', 'SK/BAN-PT/2020/234'),
(24, 12, 'B',      '2018-05-30', '2023-05-30', 'SK/BAN-PT/2018/156');

SET FOREIGN_KEY_CHECKS = 1;
