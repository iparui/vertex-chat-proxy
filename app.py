# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import generativeai as genai
import requests
import json
import secrets
import string
import random

app = Flask(__name__)
CORS(app)

# 🔐 Securely use your Vertex AI API Key
genai.configure(api_key="a337713a7918e2cb7b3051b78e1e2b70524f6e17")

# ✅ Create Gemini model instance
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

send_to_pope_url = "https://genai-app-confess2pope-1-1749573826203-978054810878.us-central1.run.app/gradio_api/queue/join?key=loaidoqvd5spvcq1"
get_from_pope_url = "https://genai-app-confess2pope-1-1749573826203-978054810878.us-central1.run.app/gradio_api/queue/data?session_hash="
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        user_input = data.get("user_input")

        if not user_input:
            return jsonify({"error": "Missing user_input"}), 400

        # send user input to genai 
        
        session_hash = generate_random_string()

        payload = json.dumps({
        "data": [
            str(user_input)
        ],
        "event_data": None,
        "fn_index": 0,
        "trigger_id": 9,
        "session_hash": str(session_hash)
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response_post = requests.request("POST", send_to_pope_url, headers=headers, data=payload)
        print(response_post.text)

        # get 
        get_from_pope_url_with_session_hash = get_from_pope_url + session_hash
        payload = {}
        headers = {}

        response_get = requests.request("GET", get_from_pope_url_with_session_hash, headers=headers, data=payload)

        print(response_get.text)



        # 🧠 Send input to Gemini model
        #response = chat.send_message(user_input)

        return jsonify({"result": response_get.text})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500



def generate_random_string(length=10):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=length))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
