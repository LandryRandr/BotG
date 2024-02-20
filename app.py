from flask import Flask, request
import os
import requests

app = Flask(__name__)

# Vérification du token de vérification
VERIFY_TOKEN = os.getenv("FACEBOOK_VERIFY_TOKEN")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        else:
            return "Verification token mismatch", 403

    if request.method == "POST":
        data = request.json
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        message_text = messaging_event["message"]["text"]
                        # Utiliser l'API Graph pour envoyer une réponse
                        send_message(sender_id, "Votre réponse ici")
        return "OK", 200

def send_message(recipient_id, message_text):
    params = {
        "access_token": os.getenv("FACEBOOK_ACCESS_TOKEN")
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post("https://graph.facebook.com/v14.0/me/messages", params=params, headers=headers, json=data)
    if response.status_code != 200:
        print("Erreur lors de l'envoi du message:", response.text)

if __name__ == "__main__":
    app.run(debug=True)
