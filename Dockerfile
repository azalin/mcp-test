FROM python:3.10-slim

# Çalışma dizini ayarla
WORKDIR /app

# Gereksinim dosyasını kopyala
COPY requirements.txt .

# Gerekli Python paketlerini yükle
RUN pip install --no-cache-dir -r requirements.txt

# Projeyi kopyala
COPY . .

# Uvicorn'u çalıştır
CMD ["python", "izin-mcp.py"]
