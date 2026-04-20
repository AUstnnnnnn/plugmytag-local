# PlugMyTag

Free producer-tag generator. Runs **entirely in your browser** — no server, no API keys, no cloud. Inspired by [plugmytag.com](https://www.plugmytag.com).

<p align="center">
  <a href="https://austnnnnnn.github.io/plugmytag-local/"><b>→ Live app</b></a>
</p>

## What it does

Type a tag (`"Prod by YourName"`), pick a preset, hit generate. Get a styled WAV download. All synthesis and effects run client-side via Web Audio API.

## Stack

| Layer | Tool |
|---|---|
| TTS | [sam-js](https://github.com/discordier/sam) — Software Automatic Mouth (~20KB) |
| Effects | Web Audio API — Convolver, Delay, WaveShaper, DynamicsCompressor, Biquad |
| Render | `OfflineAudioContext` → `AudioBuffer` → WAV encoder |
| Hosting | Static single file on GitHub Pages |

No build step. One HTML file. Loads sam-js from jsDelivr.

## Presets

🎙️ Classic Tag · 🔥 Trap God · 😈 Demon · 🐿️ Chipmunk · 📻 Radio DJ · ☎️ Telephone · 🎬 Cinematic · 📢 Stadium · 🌊 Underwater · 💿 Dusty Vinyl · 👽 Extraterrestrial · 🧼 Dry & Clean

Each preset dials in speed/pitch/throat/mouth at the TTS layer, plus an FX chain (reverb/delay/distortion/compression/EQ/bass).

## Voice character

SAM has four synthesis knobs:
- **Speed** — higher is slower (default 72)
- **Pitch** — higher is higher (default 64)
- **Throat** — formant 1 (default 128)
- **Mouth** — formant 2 (default 128)

Classic voices from the SAM manual:
| Voice | Speed | Pitch | Throat | Mouth |
|---|---|---|---|---|
| Default | 72 | 64 | 128 | 128 |
| Elf | 72 | 64 | 110 | 160 |
| Little Robot | 92 | 60 | 190 | 190 |
| Extraterrestrial | 100 | 64 | 150 | 200 |

## Run locally

```bash
git clone https://github.com/AUstnnnnnn/plugmytag-local.git
cd plugmytag-local/docs
python3 -m http.server 8000
# open http://localhost:8000
```

That's it. Any static server works.

## Why SAM and not a modern AI voice?

- **Zero model download** — SAM is 20KB of JS, not 50MB of weights
- **Instant boot** — no WASM warmup, no model load
- **Aesthetic fit** — retro robot voice pairs well with crunchy, pitched-down tag effects
- **Fully offline** after first load

For higher-quality voices, swap `sam-js` for [Piper WASM](https://github.com/wide-video/piper-wasm) (~30MB per voice) or a server-side engine.

## License

MIT for this repo. sam-js is reverse-engineered from 1980s SoftVoice SAM (abandonware status — see [sam-js license notes](https://github.com/discordier/sam#license)).
