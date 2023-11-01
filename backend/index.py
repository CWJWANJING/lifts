from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

mock_props = [
    {
        "floors": [2, 1, "G"],
        "currFloor": "G",
        "direction": "up"
     }
]

@app.route("/")
def get_liftInfo():
    return mock_props, 200