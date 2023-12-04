from flask import Flask, request
from flask_cors import CORS
import time
from dataclasses import dataclass, asdict
import dataclasses
import json
from typing import List

app = Flask(__name__)
CORS(app)

@dataclass
class liftInfo:
    floors: List[str]
    currFloor: str
    direction: str
    queue: List[str]

lift_prop = liftInfo(
    ["2", "1", "G"],
    "G",
    "up",
    []
)

mock_props = [
    json.dumps(asdict(lift_prop))
]

pressed_floors = [[] for _ in range(len(mock_props))] # idx corresponds to the idx of the lift too

t = 0

state = [[2, [1]]]

@app.route("/")
def get_liftInfo():
    last_updated = time.time() - t
    update_lift(state, t, last_updated)
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

def update_lift(state, t, last_updated):
    TIMETOFLOOR = 5 # sec
    while t > 0:
        for i in range(len(state)):
            if len(state[i]) != 0:
                state[i][0] = state[i][1][-1]
                del state[i][1][-1]
                t -= TIMETOFLOOR
    t = time.time() - last_updated
    return state