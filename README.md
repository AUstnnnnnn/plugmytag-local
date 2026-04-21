# PlugMyTag

Free producer-tag generator. Two engines, one UI. Inspired by [plugmytag.com](https://www.plugmytag.com).

<p align="center">
  <a href="https://austnnnnnn.github.io/plugmytag-local/"><b>→ Live app (Browser mode)</b></a>
</p>

## Two modes

| Mode | Engine | Runs on | Deployable | Quality |
|---|---|---|---|---|
| **Browser** | [Piper](https://github.com/rhasspy/piper) VITS models via WASM + Web Audio | Any device, any browser | GitHub Pages ✓ | Decent |
| **Mac** | macOS `say` + ffmpeg, via `server.py` | macOS only, local | No (needs CLI) | Much better |

The UI auto-detects the Mac server on boot. If reachable, the engine toggle flips to **Mac** and loads 70+ system voices. Otherwise stays in **Browser**.

## What it does

Type a tag (`"Prod by YourName"`), pick a preset, hit generate. Get a styled WAV.

## Presets

🎙️ Classic Tag · 🔥 Trap God · 😈 Demon · 🐿️ Chipmunk · 📻 Radio DJ · ☎️ Telephone · 🎬 Cinematic · 📢 Stadium · 🌊 Underwater · 💿 Dusty Vinyl · 🎩 British Announcer · 🧼 Dry & Clean

Each preset dials in voice / speed / pitch / reverb / FX. Browser and Mac have separate preset tables tuned for each engine.

## Controls

- **Voice** — Piper model (Browser) or system `say` voice (Mac)
- **Speed** — 0.6× to 1.6×
- **Pitch** — ±12 semitones
- **Reverb wet** — 0 to 1
- **FX** — reverb, delay, distortion, compression, low-pass, high-pass, bass boost

Browser mode uses Web Audio (`OfflineAudioContext` → WAV). Mac mode uses ffmpeg filter chains (`atempo`, `asetrate`, `aecho`, `acrusher`, `acompressor`, biquads).

## Run — Browser mode (any OS)

```bash
git clone https://github.com/AUstnnnnnn/plugmytag-local.git
cd plugmytag-local/docs
python3 -m http.server 8000
# open http://localhost:8000
```

Any static server works. Piper model downloads on first generate (~20 MB, cached in OPFS).

## Run — Mac mode (macOS only)

Requires `ffmpeg` (`brew install ffmpeg`) and Python 3.

```bash
git clone https://github.com/AUstnnnnnn/plugmytag-local.git
cd plugmytag-local
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python server.py
# open http://localhost:5173
```

Server serves `docs/index.html` + exposes `/voices` and `/generate`. UI auto-switches to Mac mode.

## License

MIT.
