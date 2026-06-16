from flask import Flask, request, jsonify, render_template_string
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional trading risk coach."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>TradeCheck AI</title>
    <style>
        body {
            font-family: Arial;
            background: #0f172a;
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px;
        }

        .box {
            width: 100%;
            max-width: 600px;
        }

        textarea {
            width: 100%;
            height: 120px;
            border-radius: 10px;
            padding: 10px;
        }

        button {
            margin-top: 10px;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            background: #3b82f6;
            color: white;
            cursor: pointer;
        }

        .response {
            margin-top: 20px;
            background: #1e293b;
            padding: 15px;
            border-radius: 10px;
            white-space: pre-wrap;
        }
    </style>
</head>

<body>
    <h1>📊 TradeCheck AI</h1>

    <div class="box">
        <textarea id="input" placeholder="Paste your trade here..."></textarea>
        <button onclick="send()">Analyze Trade</button>

        <div class="response" id="output"></div>
    </div>

<script>
async function send() {
    const prompt = document.getElementById("input").value;

    const res = await fetch("/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({prompt})
    });

    const data = await res.json();
    document.getElementById("output").innerText = data.result;
}
</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    result = ask_ai(data["prompt"])
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)