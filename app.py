from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a trading risk coach."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


@app.route("/")
def home():
    return "AI is running"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    result = ask_ai(data["prompt"])
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)