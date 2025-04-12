import sys
import json
import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

# FastAPI app oluşturma
app = FastAPI()

# DB bağlantı ve işlemler
def get_db_connection():
    db_path = os.environ.get("DB_PATH", "izin.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Pydantic modelleri
class PermissionRequest(BaseModel):
    personel_id: int
    baslangic: str
    bitis: str

class PersonelId(BaseModel):
    personel_id: int

# Permission listesi
@app.get("/permissions/{personel_id}")
def list_permissions(personel_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM izinler WHERE personel_id = ?", (personel_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "personel_id": row[1], "baslangic": row[2], "bitis": row[3]} for row in rows]

# İzin talep etme
@app.post("/request_permission/")
def request_permission(request: PermissionRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO izinler (personel_id, baslangic, bitis) VALUES (?, ?, ?)",
                   (request.personel_id, request.baslangic, request.bitis))
    conn.commit()
    conn.close()
    return {"status": "İzin talebi başarıyla oluşturuldu."}

# Kalan izin gün sayısı
@app.get("/remaining_days/{personel_id}")
def remaining_days(personel_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(julianday(bitis) - julianday(baslangic)) FROM izinler WHERE personel_id = ?", (personel_id,))
    used_days = cursor.fetchone()[0] or 0
    total_days = 20  # Örnek toplam izin günü
    conn.close()
    return {"kalan_gun": total_days - used_days}

