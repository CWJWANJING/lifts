from flask import Flask, request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

mock_props = [
    {
        "floors": ["2", "1", "G"],
        "currFloor": "G",
        "direction": "up"
     }
]

pressed_floors = [[]] # idx corresponds to the idx of the lift too

last_called = 0
@app.route("/")
def get_liftInfo():
    return mock_props, 200

@app.route("/", methods=['POST'])
def receive_liftQueue():
    input = request.get_json()
    # pressed_floors = update_pressed_floors(input, pressed_floors)
    return "Data received", 200

def update_pressed_floors(response_data, pressed_floors):
    lift_num = response_data["lift"]
    pressed_floors[lift_num].append(response_data["pressed"])
    print(pressed_floors)
    if mock_props[lift_num]["direction"] == "up":
        pressed_floors = pressed_floors.sort()
    else:
        pressed_floors = pressed_floors.sort(reverse=True)
    return pressed_floors