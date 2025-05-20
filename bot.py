import json
import random
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "YOUR_BOT_TOKEN"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

# Handle incoming Telegram updates
@app.route(f"/{TOKEN}", methods=["POST"])
def handle_update():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]

        # Store user chat ID
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except:
            users = []

        if chat_id not in users:
            users.append(chat_id)
            with open("users.json", "w") as f:
                json.dump(users, f)

        # Optional reply
        requests.post(f"{API_URL}/sendMessage", data={
            "chat_id": chat_id,
            "text": "You will now receive daily messages!"
        })

    return "ok"

# Daily message sender
@app.route("/send_daily", methods=["GET"])
def send_daily():
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
        with open("messages.json", "r") as f:
            messages = json.load(f)
    except:
        return "Missing files"

    message = random.choice(messages)

    for user_id in users:
        requests.post(f"{API_URL}/sendMessage", data={
            "chat_id": user_id,
            "text": message
        })

    return "Sent!"
