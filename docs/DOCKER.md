# Docker ile Çalıştırma

Python yüklemek istemiyorsan, **Docker** ile direkt çalıştırabilirsin. Tek komutta image hazır, her platformda aynı şekilde çalışır.

> Önkoşul: [Docker Desktop](https://www.docker.com/products/docker-desktop/) yüklü olsun (Windows/Mac) veya `docker` CLI (Linux).

---

## 1. Image'ı oluştur (tek seferlik, ~30 saniye)

Repo kök klasöründe:

```bash
docker build -t ingilizce-kelimeler .
```

İlk seferde Python base image'ını indirir (~50 MB), sonraki build'ler saniyeler sürer.

---

## 2. Çalıştır

### Tek kelime

**Linux/Mac:**
```bash
docker run --rm \
  -v "$(pwd)/Kelimeler:/app/Kelimeler" \
  ingilizce-kelimeler resilient
```

**Windows (cmd):**
```cmd
docker run --rm ^
  -v "%cd%\Kelimeler:/app/Kelimeler" ^
  ingilizce-kelimeler resilient
```

**Windows (PowerShell):**
```powershell
docker run --rm `
  -v "${PWD}/Kelimeler:/app/Kelimeler" `
  ingilizce-kelimeler resilient
```

Hepsi `./Kelimeler/R/resilient.md` üretir.

### Birden fazla kelime

```bash
docker run --rm -v "$(pwd)/Kelimeler:/app/Kelimeler" \
  ingilizce-kelimeler endeavor ubiquitous meticulous
```

### Seçeneklerle

```bash
# Farklı seviye
docker run --rm -v "$(pwd)/Kelimeler:/app/Kelimeler" \
  ingilizce-kelimeler validation --seviye advanced

# Üzerine yaz (mevcut kart değişsin)
docker run --rm -v "$(pwd)/Kelimeler:/app/Kelimeler" \
  ingilizce-kelimeler guidance --overwrite

# Türkçe çeviriyi atla
docker run --rm -v "$(pwd)/Kelimeler:/app/Kelimeler" \
  ingilizce-kelimeler paradigm --no-translate
```

### Toplu liste — yeni_kelimeler.txt'den

`Araçlar/yeni_kelimeler.txt` dosyasına satır satır kelime yaz, sonra:

```bash
docker run --rm \
  -v "$(pwd)/Kelimeler:/app/Kelimeler" \
  -v "$(pwd)/Araçlar/yeni_kelimeler.txt:/app/yeni_kelimeler.txt:ro" \
  ingilizce-kelimeler
```

(Argüman vermediğinde script otomatik txt'yi okur.)

---

## 3. docker compose ile daha kolay

`docker-compose.yml` zaten yazılı. Komutlar daha kısa:

```bash
# Build
docker compose build

# Tek kelime
docker compose run --rm kelime resilient

# Birkaç kelime
docker compose run --rm kelime endeavor ubiquitous

# Toplu (yeni_kelimeler.txt)
docker compose run --rm kelime
```

Volume mount otomatik — `Kelimeler/` ve `yeni_kelimeler.txt` `compose.yml`'de tanımlı.

---

## 4. Wrapper script ile en kolay

Repo'da iki wrapper var:

**Windows — `Araçlar/kelime-docker.cmd`:**
```cmd
kelime-docker resilient
kelime-docker endeavor ubiquitous --seviye advanced
```

**Mac/Linux — `Araçlar/kelime-docker.sh`:**
```bash
chmod +x Araçlar/kelime-docker.sh
./Araçlar/kelime-docker.sh resilient
```

İkisi de uzun docker komutunu sarıyor — sen sanki normal `python kelime_ekle.py` çalıştırıyormuşsun gibi yazıyorsun.

PATH'e eklersen her yerden çağırabilirsin (`alias kelime=...` veya Windows'ta dizin ekle).

---

## 5. Image'ı paylaşma — Docker Hub

Eğer başkalarının image'ı build etmesini bile istemezsen, Docker Hub'a push edersin:

```bash
# Önce Docker Hub'da hesap aç → docker login
docker login

# Image'ı tagle
docker tag ingilizce-kelimeler muhammetay/ingilizce-kelimeler:latest

# Push
docker push muhammetay/ingilizce-kelimeler:latest
```

Sonra dünyanın herhangi bir yerinden:

```bash
docker run --rm -v "$(pwd)/Kelimeler:/app/Kelimeler" \
  muhammetay/ingilizce-kelimeler resilient
```

Build adımı yok, doğrudan pull + run.

> Not: Free tier'da public image'lar süresiz kalır. Private istersen aylık ücretli plan gerekir.

---

## 6. Sık sorunlar

**"Cannot connect to the Docker daemon"**

Docker Desktop açık değil. Aç ve birkaç saniye bekle.

**Volume mount Windows'ta çalışmıyor**

Windows'ta path ayraçları sorun çıkarabilir. PowerShell'de `${PWD}/Kelimeler:/app/Kelimeler` deneyin (forward slash olabilir).

**"permission denied" (Linux)**

Container içindeki user, host'ta yazdığı dosyaları farklı UID ile yazıyor olabilir. Çözüm:
```bash
docker run --rm -u $(id -u):$(id -g) \
  -v "$(pwd)/Kelimeler:/app/Kelimeler" \
  ingilizce-kelimeler resilient
```

**Çıktı dosyası görünmüyor**

Volume mount yanlış. Mutlaka `-v "ABSOLUTE_PATH:/app/Kelimeler"` formatında ver. `~` veya relative path kullanma.

**Image 50 MB'tan büyük**

`.dockerignore` dosyası repo'da var, sadece script'i kopyalar. Yeniden build et:
```bash
docker build --no-cache -t ingilizce-kelimeler .
```

---

## 7. Ne kadar büyük image?

- python:3.11-slim base: ~45 MB
- + script + ENTRYPOINT: ~46 MB toplam

Karşılaştırma: pip install yapan tipik bir Python uygulaması 200-500 MB olur. Bu küçük çünkü standart kütüphane dışında bağımlılık yok.

---

## Hangi yöntemi seçeyim?

| Senaryo | Öneri |
|---|---|
| Bilgisayarımda Python var | Direkt `python kelime_ekle.py` (Docker gereksiz) |
| Python yok, hızlıca denemek istiyorum | `docker compose run --rm kelime resilient` |
| Sürekli kullanıcam | Wrapper script (`kelime-docker resilient`) |
| Başka makinede de çalışsın | Docker Hub'a push, `docker run muhammetay/...` |
| CI/server'da otomatik çalışsın | Docker Hub image + GitHub Actions |
