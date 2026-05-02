#!/usr/bin/env python3
"""
Kelime Ekle — Sadece kelimeyi ver, internetten kendi araştırsın.

Akış:
    1) İngilizce sözlük API'sine (dictionaryapi.dev) sorar
       → IPA, tür (part of speech), İngilizce tanım, örnek cümle, eş/zıt anlamlı
    2) MyMemory çeviri API'sine sorar
       → Türkçe anlam ve örnek cümle çevirisi
    3) Sözlük yetersiz örnek verdiyse Tatoeba.org'dan ek cümle çeker
       → İngilizce + Türkçe birlikte gelir
    4) Şablon - Orta.md formatına uygun .md notu üretir
       → ../Kelimeler/<kelime>.md

Kullanım:
    python kelime_ekle.py resilient
    python kelime_ekle.py resilient endeavor ubiquitous
    python kelime_ekle.py             # yeni_kelimeler.txt veya interaktif

Argümanlar (opsiyonel):
    --out PATH        : çıktı klasörü (varsayılan: ../Kelimeler)
    --txt PATH        : kelime listesi dosyası
    --seviye LVL      : beginner | intermediate | advanced
    --overwrite       : aynı isimli not varsa üzerine yaz
    --no-translate    : Türkçe çeviriyi atla

Bağımlılık: yok — sadece Python 3.8+ standart kütüphane.
"""

from __future__ import annotations
import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUT = SCRIPT_DIR.parent / "Kelimeler"
DEFAULT_TXT = SCRIPT_DIR / "yeni_kelimeler.txt"

DICT_API = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
TRANSLATE_API = "https://api.mymemory.translated.net/get?q={q}&langpair=en|tr"
TATOEBA_API = "https://tatoeba.org/en/api_v0/search?from=eng&to=tur&query={q}&sort=relevance"

USER_AGENT = "ingilizce-kelimeler-vault/1.0"


# ---------- yardımcılar ----------

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\-_ ]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s or "kelime"


def http_get_json(url: str, timeout: float = 10.0):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", errors="replace"))
    except Exception as e:
        print(f"  [uyarı] istek başarısız ({e})", file=sys.stderr)
        return None


# ---------- API çağrıları ----------

def fetch_dictionary(word: str):
    """dictionaryapi.dev'den kelimeyle ilgili tüm bilgiyi çeker."""
    url = DICT_API.format(word=urllib.parse.quote(word.strip().lower()))
    data = http_get_json(url)
    if not data or not isinstance(data, list) or not data:
        return None

    entry = data[0]

    ipa = ""
    for ph in entry.get("phonetics", []) or []:
        text = (ph.get("text") or "").strip()
        if text:
            ipa = text.strip("/").strip()
            break
    if not ipa:
        ipa = (entry.get("phonetic") or "").strip().strip("/")

    parts_of_speech = []
    en_definitions = []
    examples = []
    synonyms = set()
    antonyms = set()

    for meaning in entry.get("meanings", []) or []:
        pos = (meaning.get("partOfSpeech") or "").strip()
        if pos and pos not in parts_of_speech:
            parts_of_speech.append(pos)

        for s in meaning.get("synonyms", []) or []:
            if s:
                synonyms.add(s)
        for a in meaning.get("antonyms", []) or []:
            if a:
                antonyms.add(a)

        for d in (meaning.get("definitions") or [])[:3]:
            defn = (d.get("definition") or "").strip()
            if defn and defn not in en_definitions:
                en_definitions.append(defn)
            ex = (d.get("example") or "").strip()
            if ex and ex not in examples:
                examples.append(ex)
            for s in d.get("synonyms", []) or []:
                if s:
                    synonyms.add(s)
            for a in d.get("antonyms", []) or []:
                if a:
                    antonyms.add(a)

    return {
        "ipa": ipa,
        "tur": ", ".join(parts_of_speech),
        "en_tanim": en_definitions[0] if en_definitions else "",
        "ornekler": examples[:3],
        "es_anlamli": ", ".join(sorted(synonyms)[:6]),
        "zit_anlamli": ", ".join(sorted(antonyms)[:5]),
    }


def fetch_tatoeba(word: str, limit: int = 2):
    """Tatoeba'dan word'ü içeren İngilizce + Türkçe cümle çiftleri."""
    if not word:
        return []
    url = TATOEBA_API.format(q=urllib.parse.quote(word.strip()))
    data = http_get_json(url, timeout=12.0)
    if not data or not isinstance(data, dict):
        return []

    results = data.get("results") or []
    pairs = []

    for r in results:
        en = (r.get("text") or "").strip()
        if not en:
            continue
        tr = ""
        for group in r.get("translations") or []:
            if not isinstance(group, list):
                continue
            for t in group:
                if isinstance(t, dict) and t.get("lang") == "tur":
                    tr = (t.get("text") or "").strip()
                    if tr:
                        break
            if tr:
                break

        if en and tr:
            pairs.append((en, tr))
        if len(pairs) >= limit:
            break

    return pairs


_TR_CHARS = set("çğıöşüÇĞİÖŞÜâîû")
_BAD_MARKERS = (
    "MYMEMORY WARNING",
    "YOU USED ALL AVAILABLE",
    "PLEASE SELECT",
    "INVALID LANGUAGE",
    "QUERY LIMIT",
    "QUOTA EXCEEDED",
)


def fetch_translation(text: str) -> str:
    """MyMemory'den İngilizce → Türkçe çeviri. Geçersiz yanıtları boş döner."""
    if not text:
        return ""
    url = TRANSLATE_API.format(q=urllib.parse.quote(text))
    data = http_get_json(url)
    if not data:
        return ""

    rd = data.get("responseData") or {}
    translated = (rd.get("translatedText") or "").strip()

    if not translated:
        return ""

    # Uyarı / hata mesajları
    upper = translated.upper()
    if any(m in upper for m in _BAD_MARKERS):
        return ""

    # "NA", "N/A", "--", tek harf vs. — anlamsız yanıtlar
    if len(translated) <= 2:
        return ""
    if upper in {"NA", "N/A", "--", "—", "NULL", "NONE"}:
        return ""

    # MyMemory kelimeyi olduğu gibi geri döndürdüyse (çeviri yok)
    if translated.lower() == text.strip().lower():
        return ""

    # Match skoru çok düşük + içinde Türkçe karakter yok → muhtemelen anlamsız
    match = rd.get("match")
    has_tr = any(c in translated for c in _TR_CHARS)
    try:
        if match is not None and float(match) < 0.5 and not has_tr:
            # İngilizce kelimelerden oluşuyor olabilir — çeviri sayma
            ascii_only = all(ord(c) < 128 for c in translated)
            if ascii_only:
                return ""
    except (ValueError, TypeError):
        pass

    return translated


# ---------- markdown render ----------

def render_md(word: str, info: dict, today: str, level: str) -> str:
    word_slug = word.strip().lower()
    ipa = info.get("ipa") or "..."
    tur = info.get("tur") or "—"
    tr_anlam = info.get("tr_anlam") or "_(çeviri eklenemedi — manuel ekle)_"
    en_tanim = info.get("en_tanim") or "_(ekle)_"

    ornekler = info.get("ornekler") or []
    ornekler_tr = info.get("ornekler_tr") or []

    def fmt_ornek(idx: int, fallback: str) -> str:
        if idx >= len(ornekler):
            return fallback
        en = ornekler[idx]
        tr = ornekler_tr[idx] if idx < len(ornekler_tr) else ""
        if tr:
            return f"{en}\n   *{tr}*"
        return en

    e1 = fmt_ornek(0, "_(örnek 1 — ekle)_")
    e2 = fmt_ornek(1, "_(örnek 2 — ekle)_")

    sr_ornek = ornekler[0] if ornekler else ""

    es = info.get("es_anlamli") or "_—_"
    zit = info.get("zit_anlamli") or "_—_"

    return f"""---
tags: [vocabulary, {level}]
created: {today}
level: {level}
category:
part_of_speech: {tur}
auto_generated: true
---

# {word_slug}

> **Telaffuz:** /{ipa}/ 🔊
> **Tür:** {tur}

---

## 📖 Anlam

### Türkçe
{tr_anlam}

### İngilizce
{en_tanim}

---

## 💬 Örnek Cümleler

1. {e1}
2. {e2}
3. _(kendi cümlen — ekle)_

---

## 🔗 İlişkiler

| Tür | Kelime |
|---|---|
| Eş anlamlı | {es} |
| Zıt anlamlı | {zit} |
| Kelime ailesi | _(ekle: noun/verb/adj formları)_ |

---

## 🔁 Spaced Repetition

#flashcards/english

{word_slug}::{tr_anlam}<br>**Tanım:** {en_tanim}<br>**Örnek:** {sr_ornek}
"""


# ---------- işleme ----------

def process_word(word: str, out_dir: Path, today: str, level: str,
                 overwrite: bool, translate: bool) -> str:
    word = word.strip()
    if not word:
        return "skip"

    print(f"[?] {word}: sözlük çağrılıyor...")
    info = fetch_dictionary(word)
    if not info:
        print(f"  [hata] {word}: sözlükte bulunamadı (yazım hatası olabilir)")
        return "fail"

    if translate:
        print(f"  [?] türkçe çeviri çağrılıyor...")
        info["tr_anlam"] = fetch_translation(word)
        ornek_cevirileri = []
        for i, ornek in enumerate(info.get("ornekler") or []):
            if i > 0:
                time.sleep(0.3)
            print(f"  [?] örnek cümle {i+1} çevriliyor...")
            ornek_cevirileri.append(fetch_translation(ornek))
        info["ornekler_tr"] = ornek_cevirileri
    else:
        info["tr_anlam"] = ""
        info["ornekler_tr"] = []

    # Sözlük yetersiz örnek verdiyse Tatoeba'dan tamamla (en + tr birlikte gelir)
    eksik = 2 - len(info.get("ornekler") or [])
    if eksik > 0:
        print(f"  [?] Tatoeba'dan ek örnek aranıyor...")
        pairs = fetch_tatoeba(word, limit=eksik)
        if pairs:
            for en, tr in pairs:
                info["ornekler"].append(en)
                info["ornekler_tr"].append(tr)
            print(f"    [+] Tatoeba: {len(pairs)} cümle eklendi")
        else:
            print(f"    [—] Tatoeba'da uygun cümle bulunamadı")

    md = render_md(word, info, today, level)

    # Sözlük gibi alfabetik klasörlere yaz: Kelimeler/V/validation.md
    slug = slugify(word)
    first = slug[0].upper() if slug and slug[0].isalpha() else "_diger"
    letter_dir = out_dir / first
    letter_dir.mkdir(parents=True, exist_ok=True)
    fpath = letter_dir / (slug + ".md")

    if fpath.exists() and not overwrite:
        print(f"  [atla] {first}/{fpath.name} zaten var (--overwrite ile yaz)")
        return "skip"

    fpath.write_text(md, encoding="utf-8")
    print(f"  [+] {first}/{fpath.name}  (tür: {info.get('tur') or '—'})")
    return "ok"


# ---------- giriş kaynağı ----------

def collect_words(args):
    """Önce CLI argümanı, sonra txt dosyası, sonra interaktif."""
    if args.words:
        return args.words

    txt_path = Path(args.txt)
    if txt_path.exists():
        words = []
        for line in txt_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            words.append(line)
        if words:
            print(f"[i] {txt_path.name} dosyasından {len(words)} kelime okundu")
            return words

    print("[i] Kelime gir (boş Enter = çıkış):")
    words = []
    while True:
        try:
            w = input("Kelime? ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not w:
            break
        words.append(w)
    return words


def main():
    p = argparse.ArgumentParser(
        description="Tek kelime → internetten araştır → .md notu oluştur",
    )
    p.add_argument("words", nargs="*", help="işlenecek kelime(ler)")
    p.add_argument("--out", default=str(DEFAULT_OUT))
    p.add_argument("--txt", default=str(DEFAULT_TXT))
    p.add_argument("--seviye", default="intermediate",
                   choices=["beginner", "intermediate", "advanced"])
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--no-translate", action="store_true")
    args = p.parse_args()

    words = collect_words(args)
    if not words:
        print("[i] işlenecek kelime yok. çıkılıyor.")
        return

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()

    ok = fail = skip = 0
    for i, w in enumerate(words):
        if i > 0:
            time.sleep(0.4)
        result = process_word(w, out_dir, today, args.seviye,
                              args.overwrite, not args.no_translate)
        if result == "ok":
            ok += 1
        elif result == "fail":
            fail += 1
        else:
            skip += 1

    print()
    print(f"Toplam: {ok} oluşturuldu · {skip} atlandı · {fail} hata")
    print(f"Çıktı klasörü: {out_dir}")


if __name__ == "__main__":
    main()
