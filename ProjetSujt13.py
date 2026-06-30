from flask import Flask, jsonify
import urllib.request
import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CHANNEL_ID = "3418678"
READ_API_KEY = "IJNZUAA52DI8F1ZU"

last_data = {
    "temp": 0,
    "smoke": 0,
    "fire": False,
    "mode": "INIT"
}

@app.route("/api/data")
def get_data():

    global last_data

    try:

        print("\n🔍 Test de disponibilité")

        url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=1"

        response = urllib.request.urlopen(url, timeout=10)

        if response.status != 200:
            raise Exception("ThingSpeak indisponible")

        data = json.loads(response.read())

        if len(data["feeds"]) == 0:
            raise Exception("Pas de données")

        last = data["feeds"][0]

        temp = float(last["field1"])
        smoke = float(last["field2"])

        fire = temp > 40 or smoke > 2000

        last_data = {
            "temp": temp,
            "smoke": smoke,
            "fire": fire,
            "mode": "ONLINE"
        }

        return jsonify(last_data)

    except Exception as e:

        print("❌ Erreur:", e)

        last_data["mode"] = "FAILOVER"

        return jsonify(last_data)


@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    })

app.run(host="0.0.0.0", port=5000)