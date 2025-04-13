import sqlite3
import os

# Veritabanı dosyasını kontrol et
if os.path.exists('personel.db'):
    print("Veritabanı zaten var. Yeniden oluşturmak için önce personel.db dosyasını silin.")
    exit()

# Veritabanı bağlantısı oluştur
conn = sqlite3.connect('personel.db')
cursor = conn.cursor()

# Personel tablosunu oluştur
cursor.execute('''
CREATE TABLE personel (
    personel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    isim TEXT NOT NULL,
    izin_gun_sayisi INTEGER DEFAULT 20
)
''')

# İzin durumu tablosunu oluştur
cursor.execute('''
CREATE TABLE izin_durumu (
    izin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    personel_id INTEGER NOT NULL,
    izin_baslangic_tarihi TEXT NOT NULL,
    izin_bitis_tarihi TEXT NOT NULL,
    izin_gun_sayisi INTEGER NOT NULL,
    FOREIGN KEY (personel_id) REFERENCES personel (personel_id)
)
''')

# Örnek personeller ekle
personeller = [
    ("Ahmet Yılmaz", 20),
    ("Ayşe Kara", 20),
    ("Mehmet Demir", 20),
    ("Fatma Şahin", 20),
    ("Ali Can", 20),
    ("Zeynep Öztürk", 20),
    ("Mustafa Arslan", 20),
    ("Elif Yıldız", 20),
    ("Hasan Aydın", 20),
    ("Selin Kaya", 20)
]

cursor.executemany('INSERT INTO personel (isim, izin_gun_sayisi) VALUES (?, ?)', personeller)

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()

print("Veritabanı başarıyla oluşturuldu.")
print("Örnek personeller eklendi.")
print("Toplam {} personel kaydı oluşturuldu.".format(len(personeller))) 