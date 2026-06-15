import requests

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

trade = """
Trade:
EURUSD long
Risk: 1.8%
Result: Win
User rule: max risk 0.5%
"""

prompt = f"""
You are a trading risk coach.

Analyze this trade:
{trade}

Say:
- if it's GOOD or BAD
- why
- how to improve
"""

print(ask_ai(prompt))