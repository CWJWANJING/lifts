from flask import Flask
app = Flask(__name__)

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