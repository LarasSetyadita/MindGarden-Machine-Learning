from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("TOGETHER_API_KEY")
API_URL = "https://api.together.xyz/v1/chat/completions"

SYSTEM_PROMPT = (
    "Klasifikasikan teks curhatan ini sebagai persaan bahagia, marah, sedih, jatuh cinta, takut, atau terkejut"
    "ketikkan 1 untuk bahagia, 2 untuk marah, 3 untuk sedih, 4 untuk jatuh cinta, 5 untuk takut, dan 6 untuk terkejut"
    "jangan berikan output apapun kecuali salah satu dari angka tersebut"
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