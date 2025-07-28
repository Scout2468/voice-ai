import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ask")
def ask():
    q = request.args.get("question")
    if not q:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": "Bearer <YOUR_GROQ_API_KEY>",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": q}]
            }
        )
        result = response.json()
        answer = result["choices"][0]["message"]["content"].strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
