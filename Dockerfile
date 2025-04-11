FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python create_db.py

CMD ["python", "izin-mcp.py"]
