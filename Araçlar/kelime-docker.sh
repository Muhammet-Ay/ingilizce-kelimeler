#!/usr/bin/env bash
# Mac/Linux wrapper — Docker container'ı transparan çağırır.
#
# Kullanım:
#   ./kelime-docker.sh resilient
#   ./kelime-docker.sh endeavor ubiquitous
#   ./kelime-docker.sh validation --seviye advanced
#
# Çıktı: ./Kelimeler/<harf>/<kelime>.md
# (komutu vault'unun kök klasöründe çalıştır — Kelimeler/ orada olacak)

set -e

if [ ! -d "$(pwd)/Kelimeler" ]; then
    echo "[HATA] Kelimeler/ klasörü yok. Vault kök klasöründe miyim?" >&2
    exit 1
fi

# yeni_kelimeler.txt opsiyonel
TXT_MOUNT=""
if [ -f "$(pwd)/Araçlar/yeni_kelimeler.txt" ]; then
    TXT_MOUNT="-v $(pwd)/Araçlar/yeni_kelimeler.txt:/app/yeni_kelimeler.txt:ro"
fi

docker run --rm \
    -v "$(pwd)/Kelimeler:/app/Kelimeler" \
    $TXT_MOUNT \
    ingilizce-kelimeler "$@"
