from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("TOGETHER_API_KEY")
API_URL = "https://api.together.xyz/v1/chat/completions"

SYSTEM_PROMPT = (
    "Kamu adalah asisten virtual yang sangat pengertian dan penuh empati. "
    "Jawab semua curhatan pengguna dalam Bahasa Indonesia dengan lembut, sopan, dan memberi semangat."
    "Bayangkan kamu adalah pskiater yang menjaga mental pasien, memberi mereka validasi atas perasaan mereka dan mebantu mereka untuk bangkit"
    "Jangan gunakan Bahasa Inggris. Jangan mencampur Bahasa Indonesia dengan Bahasa Inggris."
    "Jangan Lebih dari 6 kalimat. "
)

@app.route("/curhat", methods=["POST"])
def curhat():
    data = request.get_json()
    user_input = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    else:
        return jsonify({"error": "Gagal memanggil Together API", "details": response.text}), response.status_code

@app.route("/")
def index():
    return "Server Flask jalan! Kirim POST ke /curhat dengan curhatanmu."

if __name__ == "__main__":
    app.run(debug=True)
