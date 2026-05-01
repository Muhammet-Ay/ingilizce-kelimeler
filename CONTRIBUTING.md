# Contributing

Thanks for considering a contribution. Keeping this lightweight.

## Easy contributions

- **Adapt to another language pair.** Fork, change the `TRANSLATE_API` and `TATOEBA_API` language codes in `Araçlar/kelime_ekle.py`, translate the markdown labels, open a PR or just link your fork in an issue — I'll list it in the README.
- **Bug reports.** A short reproduction (the word you typed, the output you got, the output you expected) is gold.
- **Better filtering.** If you find a MyMemory response pattern that returns junk and the script doesn't catch it, send the example.

## Code style

- Python 3.8+, standard library only — no `pip install` dependencies.
- Turkish comments are fine for now (matches the current codebase). If your contribution targets a different audience, English is also welcome.
- Keep functions small and pure where possible. The script's three layers — `fetch_*` (network), `render_md` (formatting), `process_word` (orchestration) — should stay separate.

## Adding a new feature

Open an issue first. Some directions I'd be happy to merge:

- Offline mode using a local Wiktionary or WordNet dump
- Anki `.apkg` exporter alongside the markdown notes
- Cross-platform plugin installer (Bash/Python equivalent of the PowerShell one)
- Word-frequency-based level detection (replacing the manual `--seviye` flag)
- A small TUI to review fetched data before saving

Some directions I'd probably *not* merge (just to set expectations):

- LLM-based generation (defeats the "free, no key, deterministic" promise)
- Custom forks of the markdown template that are too far from the existing structure
- Adding a GUI — keep this CLI

## Tests

There aren't any yet. If you want to add a test for `fetch_dictionary` parsing, mock `http_get_json` with the actual API response shape and check the parsed `info` dict. Same pattern for the other fetchers.
