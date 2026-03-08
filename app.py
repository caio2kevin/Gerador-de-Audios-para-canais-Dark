import os
import time
import numpy as np
import soundfile as sf
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "static", "outputs")
MODEL_PATH  = os.path.join(BASE_DIR, "kokoro-v1.0.onnx")
VOICES_PATH = os.path.join(BASE_DIR, "voices-v1.0.bin")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "uploads"), exist_ok=True)

VOICES = {
    "pf_dora":    "Dora (PT - Feminino)",
    "pm_alex":    "Alex (PT - Masculino)",
    "pm_santa":   "Santa (PT - Masculino)",
    "af_heart":   "Heart (EN - Feminino)",
    "af_bella":   "Bella (EN - Feminino)",
    "am_adam":    "Adam (EN - Masculino)",
    "am_michael": "Michael (EN - Masculino)",
    "ef_dora":    "Dora (ES - Feminino)",
    "em_alex":    "Alex (ES - Masculino)",
}

VOICE_LANG = {
    "pf_dora": "pt-br", "pm_alex": "pt-br", "pm_santa": "pt-br",
    "af_heart": "en-us", "af_bella": "en-us", "am_adam": "en-us", "am_michael": "en-us",
    "ef_dora": "es", "em_alex": "es",
}

kokoro_model = None

def load_model():
    global kokoro_model
    if kokoro_model is None:
        from kokoro_onnx import Kokoro
        kokoro_model = Kokoro(MODEL_PATH, VOICES_PATH)
    return kokoro_model

@app.route("/")
def index():
    return render_template("index.html", voices=VOICES)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        text  = request.form.get("text", "").strip()
        voice = request.form.get("voice", "pm_alex")
        speed = float(request.form.get("speed", "1.0"))

        if not text:
            return jsonify({"error": "Texto nao pode ser vazio."}), 400
        if len(text) > 8000:
            return jsonify({"error": "Texto muito longo."}), 400
        if voice not in VOICES:
            voice = "pm_alex"

        lang = VOICE_LANG.get(voice, "pt-br")
        output_filename = f"audio_{int(time.time())}.wav"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        model = load_model()
        samples, sample_rate = model.create(text, voice=voice, speed=speed, lang=lang)
        sf.write(output_path, samples, sample_rate)

        return jsonify({
            "success": True,
            "audio_url": f"/static/outputs/{output_filename}",
            "filename": output_filename
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro: {str(e)}"}), 500

@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(OUTPUT_FOLDER, secure_filename(filename))
    if not os.path.exists(path):
        return jsonify({"error": "Arquivo nao encontrado."}), 404
    return send_file(path, as_attachment=True, download_name=filename)

if __name__ == "__main__":
    print("\n DARK VOICE CLONER")
    print("=" * 40)
    print("  Engine  : Kokoro ONNX 0.5.0")
    print("  Acesse  : http://localhost:5000")
    print("=" * 40)
    app.run(debug=False, host="0.0.0.0", port=5000)
