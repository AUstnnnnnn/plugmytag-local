#!/usr/bin/env python3
"""Local producer-tag generator. Text -> macOS `say` -> ffmpeg effects -> WAV.

Serves docs/index.html so the same UI runs in Mac mode (this server) or
Browser mode (static GitHub Pages).
"""
import subprocess
import tempfile
import os
import re
from flask import Flask, request, send_file, jsonify, send_from_directory

app = Flask(__name__, static_folder=None)

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")


def list_voices():
    out = subprocess.run(["say", "-v", "?"], capture_output=True, text=True).stdout
    voices = []
    for line in out.splitlines():
        m = re.match(r"^(\S+(?:\s\S+)*?)\s{2,}([a-z]{2}_[A-Z]{2})\s+#", line)
        if m:
            voices.append({"name": m.group(1).strip(), "locale": m.group(2)})
    return voices


def build_filter(effects):
    """Compose ffmpeg -af filter chain from effect params."""
    chain = []

    rate = float(effects.get("rate", 1.0))
    if abs(rate - 1.0) > 0.01:
        rate = max(0.5, min(2.0, rate))
        chain.append(f"atempo={rate}")

    pitch = float(effects.get("pitch", 0))  # semitones
    if abs(pitch) > 0.01:
        ratio = 2 ** (pitch / 12.0)
        chain.append(f"asetrate=44100*{ratio},aresample=44100,atempo={1/ratio}")

    if effects.get("reverb"):
        wet = float(effects.get("reverbAmount", 0.5))
        chain.append(f"aecho=0.8:0.9:40|80|120:{wet}|{wet*0.7}|{wet*0.4}")

    if effects.get("delay"):
        chain.append("aecho=0.8:0.88:300:0.5")

    if effects.get("distortion"):
        amt = float(effects.get("distortionAmount", 0.3))
        chain.append(f"acrusher=level_in=1:level_out=1:bits=8:mode=log:mix={amt}")

    if effects.get("compression"):
        chain.append("acompressor=threshold=-18dB:ratio=4:attack=5:release=50:makeup=4")

    if effects.get("lowpass"):
        chain.append("lowpass=f=3000")

    if effects.get("highpass"):
        chain.append("highpass=f=200")

    if effects.get("bass"):
        chain.append("bass=g=6")

    chain.append("volume=1.2")
    return ",".join(chain)


@app.route("/")
def index():
    return send_from_directory(DOCS, "index.html")


@app.route("/<path:p>")
def static_docs(p):
    return send_from_directory(DOCS, p)


@app.route("/voices")
def voices():
    return jsonify(list_voices())


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    text = (data.get("text") or "").strip()
    voice = data.get("voice") or "Alex"
    fmt = data.get("format", "wav").lower()
    effects = data.get("effects") or {}

    if not text:
        return jsonify({"error": "text required"}), 400
    if fmt not in ("wav", "mp3"):
        fmt = "wav"

    with tempfile.TemporaryDirectory() as td:
        raw = os.path.join(td, "raw.wav")
        out = os.path.join(td, f"tag.{fmt}")

        try:
            subprocess.run(
                ["say", "-v", voice, "-o", raw,
                 "--file-format=WAVE", "--data-format=LEI16@44100", text],
                check=True, capture_output=True, timeout=30,
            )
        except subprocess.CalledProcessError as e:
            return jsonify({"error": f"say failed: {e.stderr.decode()}"}), 500

        af = build_filter(effects)
        cmd = ["ffmpeg", "-y", "-i", raw]
        if af:
            cmd += ["-af", af]
        if fmt == "mp3":
            cmd += ["-codec:a", "libmp3lame", "-q:a", "2"]
        cmd.append(out)

        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=30)
        except subprocess.CalledProcessError as e:
            return jsonify({"error": f"ffmpeg failed: {e.stderr.decode()}"}), 500

        return send_file(
            out, mimetype=f"audio/{fmt}", as_attachment=False,
            download_name=f"tag.{fmt}",
        )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5173, debug=False)
