import sys
import json
import os
import sqlite3
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, PromptMessage

# MCP Server oluşturma
mcp = FastMCP("Izin Takip")

# DB bağlantı ve işlemler
def get_db_connection():
    db_path = os.environ.get("DB_PATH", "personel.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# İzin listesi tool
@mcp.tool()
async def list_permissions(personel_id: int) -> str:
    """Personelin izin listesini getirir"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM izinler WHERE personel_id = ?", (personel_id,))
    rows = cursor.fetchall()
    conn.close()
    return json.dumps([{"id": row[0], "personel_id": row[1], "baslangic": row[2], "bitis": row[3]} for row in rows])

# İzin talep tool
@mcp.tool()
async def request_permission(personel_id: int, baslangic: str, bitis: str) -> str:
    """Yeni izin talebi oluşturur"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO izinler (personel_id, baslangic, bitis) VALUES (?, ?, ?)",
                   (personel_id, baslangic, bitis))
    conn.commit()
    conn.close()
    return json.dumps({"status": "İzin talebi başarıyla oluşturuldu."})

# Kalan izin günü tool
@mcp.tool()
async def remaining_days(personel_id: int) -> str:
    """Personelin kalan izin günlerini hesaplar"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(julianday(bitis) - julianday(baslangic)) FROM izinler WHERE personel_id = ?", (personel_id,))
    used_days = cursor.fetchone()[0] or 0
    total_days = 20
    conn.close()
    return json.dumps({"kalan_gun": total_days - used_days})

# MCP Server'ı başlat
if __name__ == "__main__":
    mcp.run()

