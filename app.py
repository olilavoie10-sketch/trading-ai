from flask import Flask, request, jsonify, render_template_string
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


# =========================
# AI TRADE DECISION ENGINE
# =========================
def ask_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are a PROP FIRM TRADE DECISION ENGINE v2.

You are strict, structured, and rule-based.

RULES:
- Max risk per trade = 0.5%
- If risk > 0.5% → NO TRADE
- No emotional language
- No guessing

PROCESS:
1. Analyze trade setup
2. Check risk compliance
3. Score setup (0–100)
4. Decide based on rules

OUTPUT FORMAT:

DECISION: BUY / SELL / NO TRADE

SETUP SCORE: 0–100

CONFIDENCE: 0–100%

RISK CHECK: PASS / FAIL

REASON:
- bullet points

VIOLATIONS:
- list issues or None

FINAL ACTION:
- one short instruction
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# =========================
# FRONTEND (SAAS UI)
# =========================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>TradeCheck AI</title>
    <style>
        body {
            margin: 0;
            font-family: Arial;
            background: #0b1220;
            color: white;
            display: flex;
        }

        .sidebar {
            width: 240px;
            background: #0f172a;
            height: 100vh;
            padding: 20px;
            position: fixed;
        }

        .logo {
            font-size: 20px;
            color: #60a5fa;
            font-weight: bold;
            margin-bottom: 30px;
        }

        .nav button {
            display: block;
            width: 100%;
            background: none;
            border: none;
            color: #cbd5e1;
            padding: 10px;
            text-align: left;
            cursor: pointer;
            border-radius: 8px;
        }

        .nav button:hover {
            background: #1e293b;
        }

        .main {
            margin-left: 260px;
            padding: 30px;
            width: 100%;
        }

        .section {
            display: none;
        }

        .active {
            display: block;
        }

        .card {
            background: #111827;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
        }

        textarea {
            width: 100%;
            height: 140px;
            border-radius: 10px;
            background: #0f172a;
            color: white;
            padding: 10px;
            border: 1px solid #374151;
        }

        button.primary {
            margin-top: 10px;
            width: 100%;
            padding: 12px;
            background: #3b82f6;
            border: none;
            color: white;
            border-radius: 10px;
            cursor: pointer;
        }

        .output {
            margin-top: 15px;
            background: #0f172a;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #334155;
            white-space: pre-wrap;
        }

        .pricing {
            display: flex;
            gap: 15px;
        }

        .plan {
            flex: 1;
            background: #111827;
            padding: 15px;
            border-radius: 12px;
        }

        .price {
            color: #60a5fa;
            font-size: 20px;
        }
    </style>
</head>

<body>

<div class="sidebar">
    <div class="logo">📊 TradeCheck AI</div>

    <div class="nav">
        <button onclick="show('home')">🏠 Home</button>
        <button onclick="show('analyzer')">📈 Analyzer</button>
        <button onclick="show('risk')">⚠️ Risk Tool</button>
        <button onclick="show('pricing')">💰 Pricing</button>
    </div>
</div>

<div class="main">

    <div id="home" class="section active">
        <div class="card">
            <h2>AI Prop Firm Trading Engine</h2>
            <p>Analyze trades. Enforce risk. Improve consistency.</p>
        </div>
    </div>

    <div id="analyzer" class="section">
        <div class="card">
            <h2>Trade Analyzer</h2>
            <textarea id="input" placeholder="Pair: EURUSD
Direction: Long
Risk: 1.2%
Setup: Breakout"></textarea>

            <button class="primary" onclick="send()">Analyze Trade</button>

            <div class="output" id="output">Waiting...</div>
        </div>
    </div>

    <div id="risk" class="section">
        <div class="card">
            <h2>Risk Calculator</h2>
            <p>Coming next: lot size + risk automation tool.</p>
        </div>
    </div>

    <div id="pricing" class="section">
        <div class="pricing">

            <div class="plan">
                <h3>Free</h3>
                <p class="price">$0</p>
                <p>Basic analysis</p>
            </div>

            <div class="plan">
                <h3>Pro</h3>
                <p class="price">$9/mo</p>
                <p>Risk engine + scoring</p>
            </div>

            <div class="plan">
                <h3>Elite</h3>
                <p class="price">$29/mo</p>
                <p>Full trading system</p>
            </div>

        </div>
    </div>

</div>

<script>
function show(section) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(section).classList.add('active');
}

async function send() {
    const prompt = document.getElementById("input").value;

    document.getElementById("output").innerText = "Analyzing...";

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