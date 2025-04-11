import sys
import json
import os
import sqlite3
from datetime import datetime

def list_permissions(cursor, personel_id):
    cursor.execute("SELECT * FROM izinler WHERE personel_id = ?", (personel_id,))
    rows = cursor.fetchall()
    return [{"id": row[0], "personel_id": row[1], "baslangic": row[2], "bitis": row[3]} for row in rows]

def request_permission(cursor, conn, personel_id, baslangic, bitis):
    cursor.execute("INSERT INTO izinler (personel_id, baslangic, bitis) VALUES (?, ?, ?)",
                   (personel_id, baslangic, bitis))
    conn.commit()
    return {"status": "İzin talebi başarıyla oluşturuldu."}

def remaining_days(cursor, personel_id):
    cursor.execute("SELECT SUM(julianday(bitis) - julianday(baslangic)) FROM izinler WHERE personel_id = ?", (personel_id,))
    used_days = cursor.fetchone()[0] or 0
    total_days = 20  # Örnek toplam izin günü
    return {"kalan_gun": total_days - used_days}

def main():
    db_path = os.environ.get("DB_PATH", "izin.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for line in sys.stdin:
        try:
            message = json.loads(line)
            name = message.get("name")
            args = message.get("args", {})
            if name == "personel_list":
                result = list_permissions(cursor, args.get("personel_id"))
            elif name == "izin_talep":
                result = request_permission(cursor, conn, args.get("personel_id"), args.get("baslangic"), args.get("bitis"))
            elif name == "izin_gun_sayisi":
                result = remaining_days(cursor, args.get("personel_id"))
            else:
                result = {"error": f"Bilinmeyen araç: {name}"}
            print(json.dumps({"name": name, "output": result}), flush=True)
        except Exception as e:
            print(json.dumps({"error": str(e)}), flush=True)

if __name__ == "__main__":
    main()
