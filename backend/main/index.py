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
    lift_prop
]

t = 0

state = [[2, [1]]]

@app.route("/")
def get_liftInfo():
    last_updated = time.time() - t
    update_lift(state, t, last_updated)
    return str(mock_props), 200

@app.route("/", methods=['POST'])
def receive_liftQueue():
    input = request.get_json()
    # update_pressed_floors(input, pressed_floors)
    return "Data received", 200

def update_pressed_floors(response_data, mock_props):
    lift_num = response_data['lift']
    print(mock_props)
    if mock_props[lift_num].queue == []:
        mock_props[lift_num].queue = list(response_data["pressed"])
    else:
        preData = int(str(response_data["pressed"][-1]).strip("[]"))
        mock_props[lift_num].queue.append(preData)
    if mock_props[lift_num].direction == "up":
        mock_props[lift_num].queue.sort()
    else:
        mock_props[lift_num].queue.sort(reverse=True)
    return mock_props

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

def get_next_lift(state, mock_props, people_at_floor):
    if len(state) == 1:
        return 0
    # state = [[2, [1]]]
    next_lift = 0
    lenQ = len(mock_props["floors"])
    for i in range(len(state)):
        if len(state[i][1]) < lenQ:
            lenQ = state[i][1]
            next_lift = i
    return next_lift