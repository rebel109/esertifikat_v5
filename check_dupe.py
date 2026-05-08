import pymysql
conn = pymysql.connect(host='localhost', user='root', password='', database='esertifikat', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
cursor.execute("SELECT ps.nama, COUNT(*) as jumlah FROM sertifikat s JOIN program_studi ps ON s.prodi_id = ps.id GROUP BY ps.nama HAVING COUNT(*) > 1 ORDER BY jumlah DESC LIMIT 10")
results = cursor.fetchall()
for r in results:
    print(f'{r["nama"]}: {r["jumlah"]} sertifikat')
cursor.close()
conn.close()