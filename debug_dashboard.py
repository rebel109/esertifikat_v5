import pymysql
conn = pymysql.connect(host='localhost', user='root', password='', database='esertifikat', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

# Cek prodi dengan nama yang sama
cursor.execute("SELECT nama, COUNT(*) as jumlah FROM program_studi GROUP BY nama HAVING COUNT(*) > 1")
dup_prodi = cursor.fetchall()
print("Prodi dengan nama duplikat:")
for p in dup_prodi:
    print(f"  {p['nama']}: {p['jumlah']} prodi")

# Cek sertifikat terbaru untuk "Pendidikan Agama Islam"
cursor.execute("""
SELECT ps.id, ps.nama, s.akreditasi, s.created_at, s.tgl_terbit, s.tgl_berakhir
FROM sertifikat s
JOIN program_studi ps ON s.prodi_id = ps.id
WHERE ps.nama = 'Pendidikan Agama Islam'
ORDER BY s.created_at DESC
""")
pai_certs = cursor.fetchall()
print(f"\nSertifikat untuk 'Pendidikan Agama Islam' ({len(pai_certs)} total):")
for cert in pai_certs:
    print(f"  ID: {cert['id']}, Akreditasi: {cert['akreditasi']}, Created: {cert['created_at']}, Terbit: {cert['tgl_terbit']}, Berakhir: {cert['tgl_berakhir']}")

cursor.close()
conn.close()