FROM n8nio/n8n

USER root

# Python ve pip kurulumu
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Gerekli Python paketlerini kopyala ve kur
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

USER node 