@echo off
REM Windows wrapper — Docker container'ı transparan çağırır.
REM
REM Kullanım (cmd'den):
REM   kelime-docker resilient
REM   kelime-docker endeavor ubiquitous
REM   kelime-docker validation --seviye advanced
REM
REM Çıktı: %cd%\Kelimeler\<harf>\<kelime>.md
REM (komutu vault'unun kök klasöründe çalıştır — Kelimeler/ orada olacak)

if not exist "%cd%\Kelimeler" (
    echo [HATA] Kelimeler\ klasoru yok. Vault kok klasorunde miyim?
    exit /b 1
)

docker run --rm ^
    -v "%cd%\Kelimeler:/app/Kelimeler" ^
    -v "%cd%\Araclar\yeni_kelimeler.txt:/app/yeni_kelimeler.txt:ro" ^
    ingilizce-kelimeler %*
