import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

app = Flask(__name__)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    caption = ""
    if request.method == "POST":
        prompt = request.form.get("prompt")
        niche = request.form.get("niche")

        custom_prompt = f"Write a eye catching,trendy and viral Instagram caption under 20 words in the {niche} niche. Topic: {prompt}"

        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [
                        {
                            "parts": [{"text": custom_prompt}]
                        }
                    ]
                }
            )

            data = response.json()

            if "candidates" in data:
                caption = data["candidates"][0]["content"]["parts"][0]["text"]
            elif "error" in data:
                caption = f"❌ Error: {data['error']['message']}"
            else:
                caption = "❌ Unexpected response from Gemini API."

        except Exception as e:
            caption = f"❌ Exception: {str(e)}"

    return render_template("index.html", caption=caption)

if __name__ == "__main__":
    app.run(debug=True)
