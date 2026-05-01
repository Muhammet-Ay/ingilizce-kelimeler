# 📦 Toplu Ekleme — Hızlı Başlangıç

## Ne işe yarar?

`kelimeler.csv` dosyasındaki her satırı, Obsidian vault'undaki `Kelimeler/` klasörüne ayrı bir `.md` notu olarak çevirir. **Tek seferde 50, 100 kelime** ekleyebilirsin.

## Önkoşul

- Bilgisayarda **Python 3.8+** yüklü olmalı.
  - Kontrol: `python --version` (Windows) veya `python3 --version` (Mac/Linux).
  - Kurulu değilse: <https://www.python.org/downloads/>

## Adım Adım

### 1) CSV'ye kelime ekle

`Araçlar/kelimeler.csv` dosyasını **Excel** veya not defteriyle aç. Sütunlar:

| Sütun | Zorunlu? | Örnek |
|---|---|---|
| kelime | ✅ | `appreciate` |
| anlam | ✅ | `takdir etmek` |
| ornek_cumle |  | `I really appreciate it.` |
| seviye |  | `beginner` / `intermediate` / `advanced` |
| kategori |  | `daily`, `business`, `academic` |
| ipa |  | `əˈpriːʃieɪt` |
| tur |  | `verb`, `noun`, `adjective` |
| es_anlamli |  | `value, recognize` |
| zit_anlamli |  | `undervalue` |
| en_tanim |  | `to recognize the value of something` |

> **Not:** `seviye`'ye göre üretilen şablon değişir (basit / orta / detaylı). Belirtilmezse "intermediate" varsayılır.

> Boş bir CSV başlangıcı hazır: `kelimeler.csv`. 10 satırlık dolu bir örnek için: `kelimeler_ornek.csv`.

### 2) Komut satırını aç

**Windows:**
- `Araçlar/` klasörünü Dosya Gezgini'nde aç.
- Adres çubuğuna `cmd` yaz, Enter.

**Mac/Linux:**
- Terminal'de `cd` ile bu klasöre git.

### 3) Çalıştır

```
python toplu_ekleme.py
```

veya Mac/Linux'ta:

```
python3 toplu_ekleme.py
```

Çıktı şöyle görünür:

```
[+] appreciate.md
[+] accomplish.md
[+] resilient.md
...
Toplam: 10 oluşturuldu · 0 atlandı · 0 hata
Çıktı klasörü: /.../Kelimeler
```

### 4) Obsidian'da gör

Obsidian'da sol panelde `Kelimeler/` klasörüne bak — yeni notların hepsi orada. Her birini açıp örnek cümle, eş anlamlı vb. ekleyerek zenginleştir.

## ⚡ Otomatik Mod — `kelime_ekle.py` (yalnızca kelimeyi ver)

CSV'ye anlam, IPA, tür yazmak istemiyorsan: **sadece kelimeyi yaz, gerisini script halletsin**. İnternetten araştırır, doldurur, kaydeder.

**Veri kaynakları:**
- [dictionaryapi.dev](https://dictionaryapi.dev) → IPA, tür, İngilizce tanım, örnek cümle, eş/zıt anlamlı
- [MyMemory](https://mymemory.translated.net) → Türkçe çeviri

Üç farklı şekilde kullanabilirsin (üçü de aynı script):

### A) Komut satırında doğrudan yaz
```
python kelime_ekle.py resilient
python kelime_ekle.py resilient endeavor ubiquitous meticulous
```

### B) Liste dosyasından oku — `yeni_kelimeler.txt`
`Araçlar/yeni_kelimeler.txt` dosyasını aç, her satıra bir kelime yaz, kaydet. Sonra:
```
python kelime_ekle.py
```
Argüman vermezsen önce txt'yi okumayı dener. `#` ile başlayan satırlar yorum sayılır.

### C) İnteraktif soru
Argüman yok, txt boş → script `Kelime?` diye sorar. Yazıp Enter, tekrar sorar. Boş Enter ile çıkar.
```
python kelime_ekle.py
Kelime? endeavor
Kelime? ubiquitous
Kelime?
```

### Seçenekler

| Argüman | Ne yapar |
|---|---|
| `--seviye advanced` | `beginner` / `intermediate` / `advanced` (vars: intermediate) |
| `--out yolu/klasor` | Notları başka klasöre üret |
| `--txt yolu/baska.txt` | Farklı bir liste dosyası kullan |
| `--overwrite` | Aynı isimli not varsa üzerine yaz |
| `--no-translate` | Türkçe çeviriyi atla, sadece İngilizce verileri kullan |

Örnek:
```
python kelime_ekle.py resilient endeavor --seviye advanced --overwrite
```

> **Not:** Bağımlılığı yok — `pip install` gerekmiyor, sadece Python 3.8+ yeterli.
> Üretilen notların frontmatter'ında `auto_generated: true` etiketi olur, böylece elden zenginleştirdiklerini ayırt edebilirsin.

## Seçenekler (toplu_ekleme.py)

| Argüman | Ne yapar |
|---|---|
| `--csv yolu/dosya.csv` | Farklı bir CSV kullan |
| `--out yolu/klasor` | Notları başka bir klasöre üret |
| `--overwrite` | Aynı isimde not varsa **üzerine yazsın** (varsayılan: atlar) |

Örnek:

```
python toplu_ekleme.py --csv haftalik.csv --overwrite
```

## Sık Sorunlar

**"python: command not found"**  
→ Python yüklü değil ya da PATH'e eklenmemiş. Yeniden kur, "Add Python to PATH" kutusunu işaretle.

**Türkçe karakterler bozuk görünüyor**  
→ CSV'yi UTF-8 olarak kaydet. Excel'de: "Save As" → "CSV UTF-8 (Comma delimited)".

**"kelimeler.csv bulunamadı"**  
→ `python toplu_ekleme.py` komutunu `Araçlar/` klasörünün **içinde** çalıştır. Veya `--csv` ile tam yolu ver.

**Aynı kelimeyi yeniden ürettim, eskisi gitti mi?**  
→ Hayır, varsayılan davranış **atlamak**. `--overwrite` argümanını eklemediysen güvendesin.
