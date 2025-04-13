# İzin Takip MCP Server

Bu proje, personel izin takibi için geliştirilmiş bir MCP (Model Context Protocol) server uygulamasıdır.

## Özellikler

- Personel izin listesi görüntüleme
- İzin talebi oluşturma
- Kalan izin günü hesaplama
- SQLite veritabanı entegrasyonu
- MCP protokolü desteği

## Kurulum

1. Gereksinimleri yükleyin:

```bash
pip install -r requirements.txt
```

2. Veritabanını oluşturun:

```bash
python create_db.py
```

## Docker ile Çalıştırma

```bash
docker-compose up --build
```

## MCP Server Kullanımı

Server'a iki şekilde bağlanabilirsiniz:

1. Doğrudan (Development):

```bash
python izin-mcp.py
```

2. Smithery.ai üzerinden (Production):

- URL: https://smithery.ai/server/@azalin/mcp-test/api
- Transport: STDIO

## n8n Entegrasyonu

n8n'de MCP Client bağlantısı için:

1. Connection Type: Command Line (STDIO)
2. Command: python
3. Arguments: -m mcp.client.stdio https://smithery.ai/server/@azalin/mcp-test/api

## Lisans

MIT
