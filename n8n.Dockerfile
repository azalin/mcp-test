FROM n8nio/n8n

USER root

# Python ve pip kurulumu (Alpine Linux için)
RUN apk add --no-cache python3 py3-pip

# Gerekli Python paketlerini kopyala ve kur
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

USER node 