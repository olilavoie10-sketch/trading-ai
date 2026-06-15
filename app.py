from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

def ask_ai(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

@app.route("/")
def home():
    return "AI is running"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    trade = data["trade"]

    prompt = f"""
You are a trading risk coach.

Analyze this trade:
{trade}

Say GOOD or BAD and why.
"""

    result = ask_ai(prompt)
    return jsonify({"result": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)