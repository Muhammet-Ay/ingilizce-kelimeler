# syntax=docker/dockerfile:1
#
# Ingilizce-Kelimeler — Auto-fetch English vocabulary cards for Obsidian
# https://github.com/Muhammet-Ay/ingilizce-kelimeler
#
# Build:
#   docker build -t ingilizce-kelimeler .
#
# Run (output to ./Kelimeler in your current directory):
#   Linux/Mac:
#     docker run --rm -v "$(pwd)/Kelimeler:/app/Kelimeler" ingilizce-kelimeler resilient
#   Windows (cmd):
#     docker run --rm -v "%cd%\Kelimeler:/app/Kelimeler" ingilizce-kelimeler resilient
#   Windows (PowerShell):
#     docker run --rm -v "${PWD}/Kelimeler:/app/Kelimeler" ingilizce-kelimeler resilient

FROM python:3.11-slim

LABEL org.opencontainers.image.title="Ingilizce-Kelimeler"
LABEL org.opencontainers.image.description="Auto-generate English vocabulary cards for Obsidian, with Turkish translations"
LABEL org.opencontainers.image.source="https://github.com/Muhammet-Ay/ingilizce-kelimeler"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Muhammet Ay"

# Bağımlılık yok — sadece standart kütüphane kullanılıyor
# Sadece script lazım

WORKDIR /app

# Script + örnek txt
COPY Araçlar/kelime_ekle.py /app/
COPY Araçlar/yeni_kelimeler.txt /app/yeni_kelimeler.txt

# Çıktı klasörü — kullanıcı bunu host'tan mount edecek
RUN mkdir -p /app/Kelimeler
VOLUME ["/app/Kelimeler"]

# Script'in --out parametresini default olarak ver
# Böylece kullanıcı "docker run ... resilient" yazınca kelime düzgün yere düşer
ENTRYPOINT ["python", "kelime_ekle.py", "--out", "/app/Kelimeler"]

# Argüman vermeden çalıştırırsa help göster
CMD ["--help"]
