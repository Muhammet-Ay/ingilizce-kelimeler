# Recording the Demo GIF

The README references `docs/demo.gif`. Here's a 5-minute recipe to record it.

## What to record

The whole point is to compress the magic into ~10 seconds:

1. Terminal window with cmd open in `Araçlar/`
2. You type: `python kelime_ekle.py validation`
3. Output streams: `[?] sözlük çağrılıyor... [?] türkçe çeviri... [+] validation.md`
4. Cut to Obsidian, sidebar shows `validation.md`
5. You click it, the fully populated card slides in
6. Brief pause showing the IPA, Türkçe + İngilizce sections, two examples with Turkish translations
7. End

Target length: 8–15 seconds. GIFs longer than 20 seconds rarely autoplay on LinkedIn.

## Tools

### Recommended: ScreenToGif (Windows, free)

Download: https://www.screentogif.com

Settings:
- Frame rate: 15 fps (good size/smoothness trade-off)
- Capture area: tight around terminal + Obsidian (resize windows so both are visible side-by-side)
- Encoder: FFmpeg, quality 85 → keeps file under 5 MB which LinkedIn likes

### Alternatives

- **LICEcap** (Windows/Mac) — simpler, lighter
- **OBS Studio** + Gifski — heavier but professional quality
- **Peek** (Linux) — straightforward
- **Kap** (Mac) — lovely UI

## Composition tips

- **Side-by-side, not overlapping.** Resize cmd to take left half of screen, Obsidian right half. The viewer should see both.
- **Increase font size in cmd.** Default is too small for a GIF. Right-click title bar → Properties → Font → set to 18–20pt.
- **Keep Obsidian theme readable.** A light theme reads better in GIFs than dark. Switch temporarily for the recording.
- **Highlight the cursor.** ScreenToGif has a "Show cursor" + "Show clicks" option — turn both on.
- **Don't show your real vocabulary list.** Use a fresh, empty `Kelimeler/` folder for the recording — feels less personal.
- **Single take.** Re-record if you mess up; trying to edit GIFs cleanly is painful.

## File size

Target: 2–5 MB. Above 10 MB and platforms re-encode it badly.

If your GIF is too big:
- Reduce frame rate to 10 fps
- Crop tighter
- Reduce length (cut the API output streaming if it's slow)
- Use ScreenToGif's "Reduce frames" tool to drop every other frame

## Replace the placeholder

Once you have it:

```bash
# Place it at docs/demo.gif (overwrites the placeholder)
mv ~/Downloads/demo.gif docs/demo.gif
git add docs/demo.gif
git commit -m "docs: add demo GIF"
git push
```

LinkedIn and GitHub both display it inline.

## Bonus: a 2-minute video

If you want to go beyond a GIF — record a 60–90 second screen capture (with or without voice over) showing:

1. The auto-fetch on a single word (5 sec)
2. Bulk mode reading from `yeni_kelimeler.txt` (10 sec)
3. The plugin installer running (15 sec)
4. Spaced Repetition review session in Obsidian (20 sec)
5. End card with repo URL (5 sec)

Upload to YouTube unlisted, embed in the README under the GIF. This catches viewers who want depth.
