# PlugMyTag — Local

Free, offline producer-tag generator. Local clone of [plugmytag.com](https://www.plugmytag.com). No API keys, no cloud, no subscriptions. Uses the built-in macOS `say` engine for TTS and `ffmpeg` for effects.

<p align="center">
  <a href="https://austnnnnnn.github.io/plugmytag-local/">Landing page</a> ·
  <a href="#quickstart">Quickstart</a> ·
  <a href="#presets">Presets</a> ·
  <a href="#how-it-works">How it works</a>
</p>

## Features

- 100+ voices (every macOS system voice)
- 11 presets — Classic Tag, Trap God, Demon, Chipmunk, Radio DJ, Telephone, Cinematic, Stadium, Underwater, Dusty Vinyl, Dry & Clean
- Effects: reverb, delay, distortion, compression, low-pass, high-pass, bass boost, pitch (±12 semitones), rate (0.5–1.5×)
- WAV (lossless) and MP3 export
- Single-page UI — no build step
- Runs entirely on localhost — no network, no telemetry

## Quickstart

Requires macOS (for `say`), Python 3.9+, and ffmpeg.

```bash
brew install ffmpeg
git clone https://github.com/AUstnnnnnn/plugmytag-local.git
cd plugmytag-local
python3 -m venv .venv
.venv/bin/pip install flask
.venv/bin/python server.py
```

Open <http://127.0.0.1:5173>.

## Presets

| Preset | Vibe |
|---|---|
| Classic Tag | Clean producer drop with light reverb |
| Trap God | Pitched-down, distorted, heavy reverb |
| Demon | Extreme pitch-down, gritty |
| Chipmunk | High-pitched, sped-up |
| Radio DJ | Compressed, radio-ready |
| Telephone | Band-pass, lo-fi |
| Cinematic | Deep, delayed, trailer-style |
| Stadium | Huge reverb + delay |
| Underwater | Low-pass with long reverb |
| Dusty Vinyl | Slight crunch, warm rolloff |
| Dry & Clean | No effects, raw voice |

## How it works

```
text  ─▶  macOS `say`  ─▶  WAV  ─▶  ffmpeg -af <chain>  ─▶  WAV/MP3
              ↑                             ↑
           voice                     reverb / delay /
                                   distortion / EQ / pitch
```

- **Backend** (`server.py`): Flask, ~120 lines. Three routes: `/`, `/voices`, `/generate`.
- **Frontend** (`index.html`): single file, zero deps. Preset configs inline.

Effect mapping in `build_filter()`:
- Pitch → `asetrate=44100*<ratio>,aresample=44100,atempo=<1/ratio>`
- Reverb → `aecho=0.8:0.9:40|80|120:...`
- Delay → `aecho=0.8:0.88:300:0.5`
- Distortion → `acrusher=...bits=8:mode=log`
- Compression → `acompressor=threshold=-18dB:ratio=4`
- Bass → `bass=g=6`
- Low/high-pass → `lowpass=f=3000`, `highpass=f=200`

## Why

plugmytag.com charges $9.99–$19.99 for what amounts to TTS + ffmpeg. macOS ships both for free.

## Limitations

- macOS only (depends on `say`). Linux port: swap `say` for [piper](https://github.com/rhasspy/piper) or `espeak-ng`.
- Voice quality is the stock Apple TTS — good, not AI-generated. For higher realism, swap the TTS step for a local model like [Piper](https://github.com/rhasspy/piper) or [Coqui XTTS](https://github.com/coqui-ai/TTS).

## License

MIT
