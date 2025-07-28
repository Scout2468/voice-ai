import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/ask")
def ask():
    q = request.args.get("question")
    if not q:
        return jsonify({"error": "No question provided"}), 400
    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY is not set"}), 500

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": q}]
            }
        )
        data = response.json()
        if "choices" not in data:
            return jsonify({"error": f"Unexpected response: {data}"}), 500
        answer = data["choices"][0]["message"]["content"].strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
