# TagKit

Producer tag synthesizer. Studio-rack UI. Two engines, one chassis.

<p align="center">
  <a href="https://austnnnnnn.github.io/plugmytag-local/"><b>→ Live (Browser mode)</b></a>
</p>

## Two modes

| Mode | Engine | Runs on | Deployable | Quality |
|---|---|---|---|---|
| **Browser** | [Piper](https://github.com/rhasspy/piper) VITS via WASM + Web Audio | Any device | GitHub Pages ✓ | Decent |
| **Mac** | macOS `say` + ffmpeg via `server.py` | macOS only, local | No | Much better |

UI auto-probes `/voices` on boot. Server reachable → engine toggle flips to **Mac** and loads 70+ system voices. Unreachable → **Browser** only.

## Controls

- **Model** — Piper voice (Browser) or `say` voice (Mac)
- **Speed knob** — 0.6× to 1.6× (drag, scroll, or double-click to center)
- **Pitch knob** — ±12 semitones
- **Reverb knob** — 0 to 1 wet
- **FX rockers** — reverb · delay · distortion · compression · low-pass · high-pass · bass

Browser mode renders through `OfflineAudioContext` (Convolver, Delay, WaveShaper, DynamicsCompressor, Biquad). Mac mode sends params to ffmpeg (`atempo`, `asetrate`, `aecho`, `acrusher`, `acompressor`, biquads).

## Presets

🎙️ Classic · 🔥 Trap God · 😈 Demon · 🐿️ Chipmunk · 📻 Radio DJ · ☎️ Telephone · 🎬 Cinematic · 📢 Stadium · 🌊 Underwater · 💿 Dusty Vinyl · 🎩 British Announcer · 🧼 Dry & Clean

Browser and Mac have separate preset tables tuned for each engine.

## Run — Browser mode

```bash
git clone https://github.com/AUstnnnnnn/plugmytag-local.git
cd plugmytag-local/docs
python3 -m http.server 8000
# open http://localhost:8000
```

Piper voice downloads on first generate (~20 MB, cached in OPFS).

## Run — Mac mode (macOS only)

Requires `ffmpeg` (`brew install ffmpeg`) + Python 3.

```bash
git clone https://github.com/AUstnnnnnn/plugmytag-local.git
cd plugmytag-local
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python server.py
# open http://localhost:5173
```

UI auto-switches to Mac mode.

## License

MIT.
