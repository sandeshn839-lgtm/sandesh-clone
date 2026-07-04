import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

load_dotenv()

app = Flask(__name__)

CORS(app)

# PUT YOUR GEMINI API KEY HERE
API_KEY = os.getenv("GEMINI_API_KEY")

print("API_KEY loaded:", API_KEY is not None)
print("API_KEY prefix:", API_KEY[:8] if API_KEY else "None")


@app.route('/ask', methods=['POST'])
def ask_ai():

    try:

        data = request.get_json()

        user_message = data.get('message', '')

        if not user_message:
            return jsonify({
                'reply': 'No message received.'
            })

        url = (
            "https://generativelanguage.googleapis.com/"
            f"v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        )

        payload = {

            "contents": [
                {
                    "parts": [
                        {
                            "text": f'''
You are SANDESH-AI.

Rules:
- Give accurate answers
- Help with coding
- Help with cybersecurity legally and safely
- Explain clearly
- Be intelligent and helpful
- Give short answers for simple questions
- Give detailed answers for technical questions

User Question:
{user_message}
'''
                        }
                    ]
                }
            ],

            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048
            }

        }

        response = requests.post(
            url,
            json=payload
        )

        result = response.json()

        print(result)

        try:

            ai_reply = (
                result['candidates'][0]
                ['content']['parts'][0]['text']
            )

        except Exception as e:

            print(e)

            ai_reply = (
                "AI could not generate a response."
            )

        return jsonify({
            'reply': ai_reply
        })

    except Exception as e:

        print(e)

        return jsonify({
            'reply': 'Server Error'
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
