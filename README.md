# Ingilizce-Kelimeler — Auto-Generated English Vocabulary Cards for Obsidian

> An [Obsidian](https://obsidian.md) vault that builds English vocabulary cards automatically. You type a word, a Python script fetches the IPA, part of speech, definition, example sentences, synonyms, and **Turkish translations** — then writes a polished markdown note ready for spaced repetition review.

🇹🇷 **[Türkçe README burada](README.tr.md)**

![demo](docs/demo.gif)

> *(Replace this GIF with your own — see [docs/RECORDING.md](docs/RECORDING.md) for a 5-minute recording guide.)*

---

## Why this exists

Most vocabulary apps give you flashcards. Few of them do all of these at once:

- Pull data from real dictionary sources (not hand-typed)
- Add Turkish translations automatically (or any second language with one config change)
- Live inside Obsidian so the notes are yours forever
- Work entirely with free, no-key APIs
- Take ~2 seconds per word

This is what I use myself. If it helps you too, that's the bonus.

## What it does

You run:

```bash
python kelime_ekle.py resilient
```

You get a fully populated `resilient.md` in your Obsidian vault:

```markdown
---
tags: [vocabulary, intermediate]
created: 2026-04-29
level: intermediate
part_of_speech: adjective
auto_generated: true
---

# resilient

> **Pronunciation:** /rɪˈzɪliənt/ 🔊
> **Type:** adjective

## Meaning

### Turkish
dirençli, çabuk toparlanan

### English
able to withstand or recover quickly from difficult conditions

## Example Sentences

1. The economy proved resilient after the crisis.
   *Ekonomi krizden sonra dirençli olduğunu kanıtladı.*
2. Children are remarkably resilient.
   *Çocuklar olağanüstü derecede dirençlidir.*
3. _(your own sentence — add)_

## Relations

| Type | Words |
|---|---|
| Synonyms | tough, hardy, robust, durable |
| Antonyms | fragile, weak, vulnerable |
| Word family | resilience (n), resiliently (adv) |

## Spaced Repetition

#flashcards/english

resilient::dirençli, çabuk toparlanan
```

## How it works

Three free APIs, in order:

1. **[dictionaryapi.dev](https://dictionaryapi.dev)** — IPA, parts of speech, definitions, examples, synonyms/antonyms (built on Wiktionary)
2. **[MyMemory Translation](https://mymemory.translated.net)** — Turkish translation of the word and example sentences
3. **[Tatoeba.org](https://tatoeba.org)** — fallback for example sentences when dictionary has none. Bonus: returns sentences with their human-translated Turkish counterparts.

No API keys. No `pip install`. Just Python 3.8+ and an internet connection.

## Quick start

### 1. Clone or download

```bash
git clone https://github.com/Muhammet-Ay/ingilizce-kelimeler.git
cd ingilizce-kelimeler
```

Or open the folder as an Obsidian vault directly.

### 2. Add a word

```bash
cd "Araçlar"
python kelime_ekle.py resilient
```

That's it. Open Obsidian, look in `Kelimeler/` — your card is there.

### 3. More options

```bash
# Multiple words at once
python kelime_ekle.py endeavor ubiquitous meticulous

# From a list (edit yeni_kelimeler.txt — one word per line)
python kelime_ekle.py

# Different difficulty level
python kelime_ekle.py validation --seviye advanced

# Re-fetch an existing word
python kelime_ekle.py guidance --overwrite

# Skip Turkish translation (English data only)
python kelime_ekle.py paradigm --no-translate
```

## Companion tools

This repo also ships with:

- **`toplu_ekleme.py`** — bulk-add from a CSV when you already have meanings written.
- **`eklentileri_kur.ps1` / `.bat`** — one-click installer for 8 useful Obsidian community plugins (Dataview, Templater, Translate, Calendar, Periodic Notes, Excalidraw, Various Complements, Obsidian to Anki). Windows only. Downloads from each plugin's official GitHub release.
- **Obsidian templates** — `Templates/Şablon - Basit/Orta/Detaylı.md` for three difficulty levels.
- **Spaced Repetition compatibility** — every generated card has `#flashcards/english` and `::` separators, ready for the [obsidian-spaced-repetition](https://github.com/st3v3nmw/obsidian-spaced-repetition) plugin.

## Customizing for other languages

The script targets Turkish translations by default. To change that, edit two lines at the top of `Araçlar/kelime_ekle.py`:

```python
TRANSLATE_API = "https://api.mymemory.translated.net/get?q={q}&langpair=en|tr"
TATOEBA_API = "https://tatoeba.org/en/api_v0/search?from=eng&to=tur&query={q}&sort=relevance"
```

Change `tr` to `es` (Spanish), `de` (German), `fr` (French), or any [ISO 639-1 code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes). Tatoeba uses the [639-3 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-3_codes) — `tur`, `spa`, `deu`, `fra`.

The markdown template (Turkish labels like "Telaffuz", "Anlam") lives in the `render_md` function in the same file.

## Project layout

```
.
├── README.md                      # this file
├── README.tr.md                   # Turkish version
├── LICENSE                        # MIT
├── Templates/
│   ├── Şablon - Basit.md          # beginner template
│   ├── Şablon - Orta.md           # intermediate (default)
│   └── Şablon - Detaylı.md        # advanced
├── Araçlar/
│   ├── kelime_ekle.py             # ⭐ main auto-fetch script
│   ├── toplu_ekleme.py            # CSV bulk import
│   ├── yeni_kelimeler.txt         # word list (one per line)
│   ├── eklentileri_kur.ps1        # plugin installer
│   ├── eklentileri_kur.bat        # double-click wrapper
│   └── README - Toplu Ekleme.md   # tool docs (Turkish)
├── Kelimeler/
│   ├── resilient.md               # example output
│   ├── endeavor.md
│   └── ubiquitous.md
└── docs/
    ├── RECORDING.md               # how to record a demo GIF
    └── LINKEDIN_POST.md           # social media post drafts
```

## Limitations

- **Internet required.** No offline mode yet. Could be added by bundling a Wiktionary dump.
- **MyMemory daily quota.** ~5,000 words/day. Plenty for personal use; if exceeded, translations come back empty until midnight UTC. Examples from Tatoeba still work.
- **dictionaryapi.dev coverage gaps.** Common technical words sometimes return 404. The script reports it and you can add the entry manually.
- **Windows-first install script.** `eklentileri_kur.ps1` is PowerShell. Mac/Linux users should install Obsidian plugins through the in-app store.

## Contributing

PRs welcome. If you adapt this for another language pair (Spanish learners, German learners, etc.), I'll gladly link to your fork from this README. See [CONTRIBUTING.md](CONTRIBUTING.md) for the small-print.

## License

MIT — do what you want, just keep the copyright notice.

## Acknowledgments

- [dictionaryapi.dev](https://dictionaryapi.dev) — free dictionary built on Wiktionary
- [MyMemory](https://mymemory.translated.net) — translation memory by Translated.net
- [Tatoeba](https://tatoeba.org) — community-built corpus of translated sentences
- [Obsidian](https://obsidian.md) — the knowledge base this all plugs into

Built by [Muhammet Ay](https://github.com/Muhammet-Ay) while learning English the hard way.
