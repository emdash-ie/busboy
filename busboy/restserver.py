import json
from flask import Flask
app = Flask(__name__)

import busboy.constants as c
import busboy.database as db
from busboy.model import TripId

@app.route("/")
def hello():
   return f"<h1>Hello Down There!</h1><p>Church cross east’s id: {c.church_cross_east}</p>"

@app.route("/points/<trip_id>/")
def trip_points(trip_id: str):
    tps = db.trip_points(db.default_connection(), TripId(trip_id))
    response = json.dumps(tps.to_json())
    return (response, {"Content-Type": "text/json", "Access-Control-Allow-Origin": "*"})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
