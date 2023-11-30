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

pressed_floors = [[] for _ in range(len(mock_props))] # idx corresponds to the idx of the lift too

last_called = 0
@app.route("/")
def get_liftInfo():
    return mock_props, 200

@app.route("/", methods=['POST'])
def receive_liftQueue():
    input = request.get_json()
    update_pressed_floors(input, pressed_floors)
    return "Data received", 200

def update_pressed_floors(response_data, pressed_floors):
    lift_num = response_data['lift']
    if pressed_floors[lift_num] == []:
        pressed_floors[lift_num] = list(response_data["pressed"])
    else:
        preData = int(str(response_data["pressed"][-1]).strip("[]"))
        pressed_floors[lift_num].append(preData)
    if mock_props[lift_num]["direction"] == "up":
        pressed_floors[lift_num].sort()
    else:
        pressed_floors[lift_num].sort(reverse=True)
    return pressed_floors