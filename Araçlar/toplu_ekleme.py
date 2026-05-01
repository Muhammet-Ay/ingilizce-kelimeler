#!/usr/bin/env python3
"""
Toplu Kelime Ekleme — CSV → Obsidian .md notları

Kullanım:
    1) kelimeler.csv dosyasına satır satır kelime ekle:
       kelime,anlam,ornek_cumle,seviye,kategori,ipa,tur,es_anlamli,zit_anlamli,en_tanim

    2) Bu klasörde komut satırını aç ve şu komutu çalıştır:
       python toplu_ekleme.py

    3) Bir üst klasördeki "Kelimeler/" altına her kelime için bir .md notu üretilir.

Argümanlar (opsiyonel):
    --csv PATH     : kullanılacak CSV (varsayılan: kelimeler.csv)
    --out PATH     : çıktı klasörü (varsayılan: ../Kelimeler)
    --overwrite    : aynı isimli not varsa üzerine yaz (varsayılan: atla)
"""

from __future__ import annotations
import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CSV = SCRIPT_DIR / "kelimeler.csv"
DEFAULT_OUT = SCRIPT_DIR.parent / "Kelimeler"


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\-_ ]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s or "kelime"


def render_basit(row: dict, today: str) -> str:
    return f"""---
tags: [vocabulary, beginner]
created: {today}
level: beginner
category: {row.get('kategori', '')}
---

# {row['kelime']}

**Anlam:** {row['anlam']}

**Örnek:** {row.get('ornek_cumle') or '_(örnek cümle ekle)_'}

---

## 🔁 Spaced Repetition

#flashcards/english

{row['kelime']}::{row['anlam']}
"""


def render_orta(row: dict, today: str) -> str:
    return f"""---
tags: [vocabulary, intermediate]
created: {today}
level: intermediate
category: {row.get('kategori', '')}
part_of_speech: {row.get('tur', '')}
---

# {row['kelime']}

> **Telaffuz:** /{row.get('ipa', '...') or '...'}/
> **Tür:** {row.get('tur', '—') or '—'}

## 📖 Anlam

{row['anlam']}

**İngilizce tanım:** {row.get('en_tanim') or '_(ekle)_'}

## 💬 Örnek Cümleler

1. {row.get('ornek_cumle') or '_(örnek 1)_'}
2. _(örnek 2)_
3. _(kendi cümlen)_

## 🔗 İlgili Kelimeler

- **Eş anlamlı:** {row.get('es_anlamli') or '_—_'}
- **Zıt anlamlı:** {row.get('zit_anlamli') or '_—_'}

---

## 🔁 Spaced Repetition

#flashcards/english

{row['kelime']}::{row['anlam']}<br>**Örnek:** {row.get('ornek_cumle', '')}
"""


def render_detayli(row: dict, today: str) -> str:
    return f"""---
tags: [vocabulary, advanced]
created: {today}
level: advanced
category: {row.get('kategori', '')}
part_of_speech: {row.get('tur', '')}
---

# {row['kelime']}

> **Telaffuz:** /{row.get('ipa', '...') or '...'}/ 🔊
> **Tür:** {row.get('tur', '—') or '—'}

---

## 📖 Anlam

### Türkçe
{row['anlam']}

### İngilizce
{row.get('en_tanim') or '_(ekle)_'}

---

## 💬 Örnek Cümleler

1. {row.get('ornek_cumle') or '_(resmi)_'}
2. _(günlük)_
3. _(edebi/yazılı)_

### Kendi cümlem
- _(kendi cümlen — hatırlamayı 3x artırır)_

---

## 🔗 İlişkiler

| Tür | Kelime |
|---|---|
| Eş anlamlı | {row.get('es_anlamli') or '—'} |
| Zıt anlamlı | {row.get('zit_anlamli') or '—'} |
| Kelime ailesi | _(noun / verb / adj formları)_ |

---

## 🔁 Spaced Repetition

#flashcards/english

{row['kelime']}::{row['anlam']}<br>**Tanım:** {row.get('en_tanim', '')}<br>**Örnek:** {row.get('ornek_cumle', '')}
"""


RENDERERS = {
    "beginner": render_basit,
    "intermediate": render_orta,
    "advanced": render_detayli,
}


def main():
    p = argparse.ArgumentParser(description="CSV'den Obsidian kelime notları üret.")
    p.add_argument("--csv", default=str(DEFAULT_CSV))
    p.add_argument("--out", default=str(DEFAULT_OUT))
    p.add_argument("--overwrite", action="store_true")
    args = p.parse_args()

    csv_path = Path(args.csv)
    out_dir = Path(args.out)

    if not csv_path.exists():
        print(f"[HATA] CSV bulunamadı: {csv_path}", file=sys.stderr)
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()

    created = 0
    skipped = 0
    errored = 0

    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # 2 = ilk veri satırı
            try:
                kelime = (row.get("kelime") or "").strip()
                anlam = (row.get("anlam") or "").strip()
                if not kelime or not anlam:
                    print(f"[atla] {i}. satır: kelime/anlam boş")
                    skipped += 1
                    continue

                seviye = (row.get("seviye") or "intermediate").strip().lower()
                renderer = RENDERERS.get(seviye, render_orta)
                md = renderer(row, today)

                fname = slugify(kelime) + ".md"
                fpath = out_dir / fname

                if fpath.exists() and not args.overwrite:
                    print(f"[atla] {fname} zaten var (--overwrite ile yaz)")
                    skipped += 1
                    continue

                fpath.write_text(md, encoding="utf-8")
                print(f"[+] {fname}")
                created += 1
            except Exception as e:
                print(f"[HATA] {i}. satır: {e}", file=sys.stderr)
                errored += 1

    print()
    print(f"Toplam: {created} oluşturuldu · {skipped} atlandı · {errored} hata")
    print(f"Çıktı klasörü: {out_dir}")


if __name__ == "__main__":
    main()
