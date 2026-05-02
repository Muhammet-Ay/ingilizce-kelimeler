#!/usr/bin/env python3
"""
Vault'u alfabetik organize et — sözlük gibi.

Kelimeler/ altındaki tüm .md notlarını ilk harflerine göre alt
klasörlere taşır:
    Kelimeler/A/appreciate.md
    Kelimeler/A/adopted.md
    Kelimeler/B/base.md
    ...

Ayrıca _Sözlük.md dosyası üretir — A-Z butonlu navigasyon ve her
harf için Dataview ile dinamik kelime listesi içerir. Yeni kelime
eklediğinde sözlük otomatik güncellenir, sıfır bakım.

Kullanım:
    python vault_alfabetik_organize.py
        → Sadece neler yapılacağını gösterir (dry-run, dosya taşımaz)

    python vault_alfabetik_organize.py --uygula
        → Gerçekten taşır + _Sözlük.md üretir

    python vault_alfabetik_organize.py --uygula --indeksi-yenile
        → Sadece _Sözlük.md'yi yeniden üret (dosya taşımaz)

Önemli:
    - İdempotent — birden fazla kez çalıştırabilirsin, sorun çıkmaz
    - .excalidraw.md dosyaları taşınmaz (yerinde kalır)
    - Alt çizgi ile başlayan dosyalar (_Sözlük.md gibi) taşınmaz
    - Aynı isimli not zaten alt klasörde varsa atlar (uyarır)

Spaced Repetition uyarısı:
    Dosyalar yer değiştirdikten sonra Obsidian'da Ctrl+P → "Reload app
    without saving" yap. SR plugin yeni konumları yeniden indeksler,
    kart geçmişin korunur.
"""

from __future__ import annotations
import argparse
import shutil
import string
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DIR = SCRIPT_DIR.parent / "Kelimeler"
ALPHABET = list(string.ascii_uppercase)
MISC_FOLDER = "_diger"  # sayı veya alfabe dışı ile başlayanlar


def first_letter(filename: str) -> str:
    """Dosya adından harf klasörü adını döndürür (A-Z) ya da MISC_FOLDER."""
    if not filename:
        return MISC_FOLDER
    c = filename[0].upper()
    if c in ALPHABET:
        return c
    return MISC_FOLDER


def list_top_level_md(klasor: Path) -> list[Path]:
    """Kelimeler/ altındaki üst seviye .md dosyalarını listeler.

    Atlanır:
    - alt klasörlerin içindekiler (zaten organize)
    - .excalidraw.md çizimler
    - alt çizgi ile başlayanlar (_Sözlük.md gibi sistem notları)
    """
    out = []
    for f in klasor.iterdir():
        if not f.is_file():
            continue
        if not f.name.endswith(".md"):
            continue
        if f.name.endswith(".excalidraw.md"):
            continue
        if f.name.startswith("_"):
            continue
        out.append(f)
    return sorted(out)


def plan_moves(files: list[Path], klasor: Path) -> dict[str, list[tuple[Path, Path]]]:
    """Her dosya için (kaynak, hedef) çiftleri üret, harf bazında grupla."""
    plan: dict[str, list[tuple[Path, Path]]] = {}
    for f in files:
        letter = first_letter(f.name)
        target = klasor / letter / f.name
        plan.setdefault(letter, []).append((f, target))
    return plan


def apply_moves(plan: dict[str, list[tuple[Path, Path]]]) -> tuple[int, int, int]:
    """Taşıma planını uygula. (taşındı, atlandı, hata) döner."""
    moved = skipped = errored = 0
    for letter in sorted(plan.keys()):
        target_dir = next(iter(plan[letter]))[1].parent
        target_dir.mkdir(parents=True, exist_ok=True)
        for src, dst in plan[letter]:
            try:
                if dst.exists():
                    print(f"  [atla] {src.name} → {letter}/  (hedef zaten var)")
                    skipped += 1
                    continue
                shutil.move(str(src), str(dst))
                print(f"  [+] {src.name} → {letter}/")
                moved += 1
            except Exception as e:
                print(f"  [hata] {src.name}: {e}", file=sys.stderr)
                errored += 1
    return moved, skipped, errored


def existing_letter_dirs(klasor: Path) -> list[str]:
    """Kelimeler/ altındaki mevcut harf klasörlerini listeler."""
    if not klasor.exists():
        return []
    out = []
    for d in klasor.iterdir():
        if d.is_dir() and d.name in ALPHABET + [MISC_FOLDER]:
            # Sadece içinde .md varsa say
            if any(f.suffix == ".md" for f in d.iterdir() if f.is_file()):
                out.append(d.name)
    return sorted(out)


def generate_sozluk(klasor: Path) -> str:
    """_Sözlük.md içeriğini üret — A-Z butonlar + Dataview blokları."""
    mevcut_harfler = existing_letter_dirs(klasor)

    # Üst kısım: A-Z butonları (sayfa içi anchor'lara link)
    nav_buttons = []
    for harf in ALPHABET:
        if harf in mevcut_harfler:
            nav_buttons.append(f"[**{harf}**](#{harf.lower()})")
        else:
            nav_buttons.append(f"<span style='color:#999'>{harf}</span>")
    nav = " · ".join(nav_buttons)

    # Diğer (sayı ile başlayanlar vs.)
    if MISC_FOLDER in mevcut_harfler:
        nav += f" · [**Diğer**](#diger)"

    # Her harf için Dataview bloğu
    sections = []
    for harf in ALPHABET:
        if harf not in mevcut_harfler:
            continue
        section = f"""## {harf}

```dataview
LIST
FROM "Kelimeler/{harf}"
SORT file.name ASC
```

[⬆️ yukarı](#a-z-sözlük)
"""
        sections.append(section)

    if MISC_FOLDER in mevcut_harfler:
        sections.append(f"""## Diğer

```dataview
LIST
FROM "Kelimeler/{MISC_FOLDER}"
SORT file.name ASC
```

[⬆️ yukarı](#a-z-sözlük)
""")

    body = "\n---\n\n".join(sections) if sections else "*Henüz kelime yok. `python kelime_ekle.py <kelime>` ile ekle.*"

    return f"""---
tags: [sözlük, index]
auto_generated: true
---

# 📖 A-Z Sözlük

> Kelimelerin tamamı, klasik sözlük gibi alfabetik gruplara ayrılmış.
> Yeni kelime eklediğinde otomatik güncellenir.

{nav}

---

{body}
"""


def main():
    p = argparse.ArgumentParser(description="Kelimeler/ klasörünü A-Z sözlük gibi organize et")
    p.add_argument("--klasor", default=str(DEFAULT_DIR),
                   help=f"taranacak klasör (vars: {DEFAULT_DIR})")
    p.add_argument("--uygula", action="store_true",
                   help="gerçekten taşı + _Sözlük.md üret (varsayılan: dry-run)")
    p.add_argument("--indeksi-yenile", action="store_true",
                   help="sadece _Sözlük.md'yi yeniden üret (dosya taşıma)")
    args = p.parse_args()

    klasor = Path(args.klasor)
    if not klasor.exists():
        print(f"[HATA] klasör yok: {klasor}", file=sys.stderr)
        sys.exit(1)

    if args.indeksi_yenile and args.uygula:
        # Sadece sözlük üret, dosya taşıma
        sozluk = klasor / "_Sözlük.md"
        sozluk.write_text(generate_sozluk(klasor), encoding="utf-8")
        print(f"[+] _Sözlük.md yenilendi: {sozluk}")
        return

    files = list_top_level_md(klasor)
    if not files:
        print("[i] Üst seviyede taşınacak dosya yok. (Belki zaten organize edilmiş?)")
        if args.uygula:
            sozluk = klasor / "_Sözlük.md"
            sozluk.write_text(generate_sozluk(klasor), encoding="utf-8")
            print(f"[+] _Sözlük.md güncellendi: {sozluk}")
        return

    plan = plan_moves(files, klasor)

    print(f"[i] {len(files)} dosya bulundu, {len(plan)} farklı harf grubuna ayrılacak:")
    print()
    for letter in sorted(plan.keys()):
        items = plan[letter]
        print(f"  📂 {letter}/  ({len(items)} kelime)")
        for src, _ in items[:5]:
            print(f"      - {src.name}")
        if len(items) > 5:
            print(f"      ... ve {len(items)-5} dosya daha")
    print()

    if not args.uygula:
        print("Bu sadece DRY-RUN — hiçbir şey taşınmadı.")
        print("Gerçekten taşımak için: python vault_alfabetik_organize.py --uygula")
        return

    print("[*] Taşıma başlıyor...")
    moved, skipped, errored = apply_moves(plan)
    print()
    print(f"  Taşındı: {moved}  ·  Atlandı: {skipped}  ·  Hata: {errored}")
    print()

    print("[*] _Sözlük.md üretiliyor...")
    sozluk = klasor / "_Sözlük.md"
    sozluk.write_text(generate_sozluk(klasor), encoding="utf-8")
    print(f"  [+] {sozluk.name}")
    print()

    print("=== TAMAMLANDI ===")
    print()
    print("ŞİMDİ Obsidian'da:")
    print("  1) Ctrl+P → 'Reload app without saving' (SR plugin yeni konumları indeksler)")
    print("  2) Sol panelde Kelimeler/A, Kelimeler/B, ... klasörlerini gör")
    print("  3) Kelimeler/_Sözlük.md aç — A-Z butonları + dinamik liste hazır")
    print()


if __name__ == "__main__":
    main()
