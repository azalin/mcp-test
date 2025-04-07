# MCP-Test: Personel İzin Yönetim Sistemi

Bu proje, MCP (Model Control Protocol) kullanarak personel izin yönetimini sağlayan bir API sunucusudur.

## Özellikler

- Personel izin geçmişi görüntüleme
- İzin talep etme
- Kalan izin günü sorgulama
- Tarih çakışması kontrolü

## Kurulum

1. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Veritabanını oluşturun:
```bash
python create_db.py
```

3. Sunucuyu başlatın:
```bash
python izin-mcp.py
```

## API Kullanımı

MCP sunucusu `/sse` endpoint'i üzerinden aşağıdaki araçları sunar:

1. `personel_list`: Belirli bir personelin izin geçmişini döndürür
2. `izin_talep`: Yeni izin talebi oluşturur
3. `izin_gun_sayisi`: Personelin izin gün sayısı bilgisini döndürür

## Lisans

MIT Lisansı 