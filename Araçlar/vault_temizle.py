#!/usr/bin/env python3
"""
Vault Temizleyici — Kelimeler/ klasöründeki anlamsız notları işaretler.

Bazen yanlışlıkla "of", "may", "into" gibi vocabulary değeri olmayan
kelimeler not olarak eklenebiliyor. Bu script onları şüpheli olarak
listeler ve sen onaylarsan siler.

Kullanım:
    python vault_temizle.py            # sadece listele (silme)
    python vault_temizle.py --sil      # listele ve onayla → sil

Hangi notlar şüpheli sayılır?
    1) Çok kısa kelimeler (1-2 harf)
    2) İngilizce'de en sık 200 kelime arasında olanlar (in, of, to, ...)
    3) Ortak yardımcı fiiller (may, will, should, ...)
    4) Boş veya neredeyse boş notlar
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DIR = SCRIPT_DIR.parent / "Kelimeler"

# İngilizce'de en yaygın "fonksiyonel" kelimeler — vocabulary kartı olmaz
COMMON_FUNCTION_WORDS = {
    # makaleler ve belirleyiciler
    "a", "an", "the", "this", "that", "these", "those",
    # bağlaçlar
    "and", "or", "but", "so", "yet", "for", "nor",
    # yer/zaman edatları
    "in", "on", "at", "by", "to", "of", "with", "from", "into", "onto",
    "about", "above", "below", "after", "before", "during", "through",
    "between", "among", "against", "without", "within", "across", "over",
    "under", "around",
    # zamirler
    "i", "you", "he", "she", "it", "we", "they",
    "me", "him", "her", "us", "them",
    "my", "your", "his", "its", "our", "their",
    "mine", "yours", "hers", "ours", "theirs",
    "this", "that", "who", "whom", "whose", "which", "what",
    # yardımcı fiiller
    "is", "am", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having",
    "do", "does", "did", "done",
    "will", "would", "shall", "should",
    "can", "could", "may", "might", "must",
    "ought",
    # bağlantı / söylem
    "also", "too", "very", "just", "only", "even", "still", "yet",
    "however", "therefore", "moreover", "furthermore", "thus", "hence",
    "though", "although", "while", "whereas",
    "as", "than", "if", "unless", "because", "since",
    # zaman / sıklık
    "now", "then", "here", "there", "when", "where", "why", "how",
    "always", "often", "sometimes", "never", "ever", "once", "twice",
    "today", "yesterday", "tomorrow",
    # sayılar (en yaygın)
    "one", "two", "three", "four", "five", "first", "second", "last",
    "many", "few", "some", "any", "all", "both", "each", "every",
    "no", "yes", "not",
    # seyrek olarak gerçek vocab olabilen ama genelde junk:
    "good", "bad", "big", "small", "new", "old", "more", "less",
    "much", "such",
}

# "of.md", "may.md" gibi bizim üretimimiz olmayan, ama genelde zararsız sayılan
# kelimeler — gerçekten junk olduğundan emin olmak için ayrıca işaretleyelim
TYPICAL_JUNK = {
    "of", "may", "also", "into", "should", "would", "could",
    "will", "shall", "must", "might",
}


def is_suspicious(word: str, content: str) -> tuple[bool, str]:
    """Bir not şüpheli mi? (evet/hayır, sebep)"""
    w = word.lower().strip()

    # 1) Çok kısa
    if len(w) <= 2:
        return True, "çok kısa (1-2 harf)"

    # 2) Bilinen junk listesinde
    if w in TYPICAL_JUNK:
        return True, "bilinen junk kelime"

    # 3) Yaygın fonksiyonel kelime
    if w in COMMON_FUNCTION_WORDS:
        return True, "yaygın fonksiyonel kelime"

    # 4) Boş veya neredeyse boş not
    body = content.split("---", 2)
    body_text = body[2] if len(body) >= 3 else content
    # placeholder dışı içerik var mı?
    cleaned = body_text.replace("_(ekle)_", "").replace("_(örnek 1 — ekle)_", "")
    cleaned = cleaned.replace("_(örnek 2 — ekle)_", "").replace("_—_", "")
    if len(cleaned.strip()) < 100:
        return True, "neredeyse boş not"

    return False, ""


def main():
    p = argparse.ArgumentParser(description="Vault'taki anlamsız vocabulary notlarını temizle")
    p.add_argument("--klasor", default=str(DEFAULT_DIR),
                   help=f"taranacak klasör (vars: {DEFAULT_DIR})")
    p.add_argument("--sil", action="store_true",
                   help="onaylarsan şüphelileri siler (varsayılan: sadece listeler)")
    args = p.parse_args()

    klasor = Path(args.klasor)
    if not klasor.exists():
        print(f"[HATA] klasör yok: {klasor}", file=sys.stderr)
        sys.exit(1)

    # Excalidraw drawing dosyalarını atla
    md_files = sorted(f for f in klasor.glob("*.md") if not f.name.endswith(".excalidraw.md"))
    print(f"[i] {len(md_files)} not bulundu: {klasor}")
    print()

    suspicious = []
    for f in md_files:
        word = f.stem  # dosya adı .md'siz
        try:
            content = f.read_text(encoding="utf-8")
        except Exception:
            continue
        suspicious_flag, reason = is_suspicious(word, content)
        if suspicious_flag:
            suspicious.append((f, reason))

    if not suspicious:
        print("[+] Şüpheli not yok. Vault temiz.")
        return

    print(f"[!] {len(suspicious)} şüpheli not:")
    for f, reason in suspicious:
        print(f"    {f.name:30s}  ({reason})")
    print()

    if not args.sil:
        print("Sadece listeleme modu. Silmek için: python vault_temizle.py --sil")
        return

    print("Bu dosyaları silmek istiyor musun?")
    print("  evet → hepsini sil")
    print("  sec  → tek tek sor")
    print("  iptal → hiçbir şey yapma")
    karar = input("Seçim: ").strip().lower()

    silinecek = []
    if karar in ("e", "evet", "y", "yes"):
        silinecek = [f for f, _ in suspicious]
    elif karar in ("s", "sec", "seç"):
        for f, reason in suspicious:
            cev = input(f"  {f.name} silinsin mi? (e/h): ").strip().lower()
            if cev in ("e", "evet", "y", "yes"):
                silinecek.append(f)
    else:
        print("[i] iptal edildi.")
        return

    for f in silinecek:
        try:
            f.unlink()
            print(f"  [-] silindi: {f.name}")
        except Exception as e:
            print(f"  [hata] {f.name}: {e}", file=sys.stderr)

    print()
    print(f"Toplam silinen: {len(silinecek)}")


if __name__ == "__main__":
    main()
