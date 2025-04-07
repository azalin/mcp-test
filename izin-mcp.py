from mcp.server.fastmcp import FastMCP
import uvicorn
import sqlite3
from datetime import datetime
import os

# Yerel ortam için port ve host ayarları
PORT = 3010
HOST = "127.0.0.1"  # Yerel ortam için localhost

# MCP sunucusu oluştur
mcp = FastMCP("Personelİzin")

def get_db_connection():
    """Veritabanı bağlantısı oluştur"""
    return sqlite3.connect('personel.db')

#@mcp.tool()
#def add(a: int, b: int) -> int:"""
    #"""Add two numbers"""
    #return a * b

@mcp.tool()
def personel_list(personel_id: int) -> dict:
    """Belirli bir personelin izin geçmişini döndürür"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Önce personel bilgilerini al
    cursor.execute('SELECT isim FROM personel WHERE personel_id = ?', (personel_id,))
    personel = cursor.fetchone()
    
    if not personel:
        conn.close()
        return {"hata": "Personel bulunamadı"}
    
    # Personelin izin geçmişini al
    cursor.execute('''
        SELECT izin_baslangic_tarihi, izin_bitis_tarihi, izin_gun_sayisi
        FROM izin_durumu
        WHERE personel_id = ?
        ORDER BY izin_baslangic_tarihi DESC
    ''', (personel_id,))
    
    izinler = cursor.fetchall()
    conn.close()
    
    # Sonuçları formatla
    izin_listesi = []
    for i, izin in enumerate(izinler, 1):
        izin_listesi.append({
            "izin_no": i,
            "baslangic_tarihi": izin[0],
            "bitis_tarihi": izin[1],
            "izin_gun_sayisi": izin[2]
        })
    
    return {
        "personel_id": personel_id,
        "isim": personel[0],
        "toplam_izin_sayisi": len(izinler),
        "izinler": izin_listesi
    }

@mcp.tool()
def izin_talep(personel_id: int, baslangic_tarihi: str, bitis_tarihi: str) -> dict:
    """Personel için izin talebi oluşturur"""
    try:
        # Tarihleri kontrol et
        baslangic = datetime.strptime(baslangic_tarihi, '%d/%m/%Y')
        bitis = datetime.strptime(bitis_tarihi, '%d/%m/%Y')
        
        if bitis < baslangic:
            return {"hata": "Bitiş tarihi başlangıç tarihinden önce olamaz"}
        
        # İzin gün sayısını hesapla
        izin_gun = (bitis - baslangic).days + 1
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Personelin kalan izin gününü kontrol et
        cursor.execute('SELECT izin_gun_sayisi FROM personel WHERE personel_id = ?', (personel_id,))
        personel = cursor.fetchone()
        
        if not personel:
            conn.close()
            return {"hata": "Personel bulunamadı"}
        
        # Kullanılan izin günlerini hesapla
        cursor.execute('''
            SELECT COALESCE(SUM(izin_gun_sayisi), 0) 
            FROM izin_durumu 
            WHERE personel_id = ?
        ''', (personel_id,))
        kullanilan_izin = cursor.fetchone()[0]
        
        kalan_izin = personel[0] - kullanilan_izin
        
        if izin_gun > kalan_izin:
            conn.close()
            return {"hata": f"Yetersiz izin günü. Kalan izin: {kalan_izin} gün"}
        
        # Tarih çakışması kontrolü
        cursor.execute('''
            SELECT COUNT(*) FROM izin_durumu
            WHERE personel_id = ? AND 
            (
                (izin_baslangic_tarihi <= ? AND izin_bitis_tarihi >= ?) OR
                (izin_baslangic_tarihi <= ? AND izin_bitis_tarihi >= ?) OR
                (izin_baslangic_tarihi >= ? AND izin_bitis_tarihi <= ?)
            )
        ''', (
            personel_id, 
            baslangic.strftime('%Y-%m-%d'), baslangic.strftime('%Y-%m-%d'),
            bitis.strftime('%Y-%m-%d'), bitis.strftime('%Y-%m-%d'),
            baslangic.strftime('%Y-%m-%d'), bitis.strftime('%Y-%m-%d')
        ))
        cakisma_sayisi = cursor.fetchone()[0]
        
        if cakisma_sayisi > 0:
            conn.close()
            return {"hata": "Bu tarih aralığında zaten izin kaydı bulunmaktadır"}
        
        # İzin kaydını ekle
        cursor.execute('''
            INSERT INTO izin_durumu 
            (personel_id, izin_baslangic_tarihi, izin_bitis_tarihi, izin_gun_sayisi)
            VALUES (?, ?, ?, ?)
        ''', (personel_id, baslangic.strftime('%Y-%m-%d'), bitis.strftime('%Y-%m-%d'), izin_gun))
        
        conn.commit()
        conn.close()
        
        return {
            "mesaj": "İzin talebi başarıyla oluşturuldu",
            "personel_id": personel_id,
            "baslangic_tarihi": baslangic_tarihi,
            "bitis_tarihi": bitis_tarihi,
            "izin_gun": izin_gun,
            "kalan_izin": kalan_izin - izin_gun
        }
        
    except ValueError:
        return {"hata": "Geçersiz tarih formatı. Lütfen DD/MM/YYYY formatında girin"}
    except Exception as e:
        return {"hata": str(e)}

@mcp.tool()
def izin_gun_sayisi(personel_id: int) -> dict:
    """Personelin izin gün sayısı bilgisini döndürür"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Personel bilgilerini al
    cursor.execute('SELECT isim, izin_gun_sayisi FROM personel WHERE personel_id = ?', (personel_id,))
    personel = cursor.fetchone()
    
    if not personel:
        conn.close()
        return {"hata": "Personel bulunamadı"}
    
    # Kullanılan izin günlerini hesapla
    cursor.execute('''
        SELECT COALESCE(SUM(izin_gun_sayisi), 0) 
        FROM izin_durumu 
        WHERE personel_id = ?
    ''', (personel_id,))
    kullanilan_izin = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "personel_id": personel_id,
        "isim": personel[0],
        "toplam_izin": personel[1],
        "kullanilan_izin": kullanilan_izin,
        "kalan_izin": personel[1] - kullanilan_izin
    }

if __name__ == "__main__":
    print("MCP sunucusu başlatılıyor...")
    print(f"Sunucu adresi: http://{HOST}:{PORT}/sse")
    
    # Uvicorn ile başlat
    uvicorn.run(
        mcp.sse_app(),
        host=HOST,
        port=PORT,
        log_level="info"
    ) 