from flask import Flask, request
from flask_cors import CORS
import time
from dataclasses import dataclass, asdict
import json
from typing import List

app = Flask(__name__)
CORS(app)

@dataclass
class liftInfo:
    floors: List[int]
    cur_floor: int
    direction: str
    queue: List[int]

floors = [2, 1, 0] # all lifts go to the same floors

lift_prop = liftInfo(
    floors,
    0,
    "up",
    []
)

mock_props = [
    lift_prop
]

t = 0

@app.route("/")
def get_liftInfo():
    last_updated = time.time() - t
    update_lift(mock_props, t, last_updated)
    res_data = json.dumps([asdict(lift_prop)])
    return res_data, 200

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

def update_lift(mock_props, t, last_updated):
    TIMETOFLOOR = 5 # sec
    while t > 0:
        for i in range(len(mock_props)):
            last_floor = mock_props[i].queue[-1]
            if len(mock_props[i].queue) != 0:
                mock_props[i].queue.remove(last_floor)
                t -= TIMETOFLOOR
    t = time.time() - last_updated
    return mock_props

def get_next_lift(mock_props, people_at_floor):
    if len(mock_props) == 1:
        return 0
    next_lift = 0
    min_distance = float('inf')

    for lift in mock_props:
        if lift.direction == "up" and people_at_floor >= lift.cur_floor:
            distance = people_at_floor - lift.cur_floor
        elif lift.direction == "down" and people_at_floor <= lift.cur_floor:
            distance = lift.cur_floor - people_at_floor
        else:
            distance = abs(people_at_floor - lift.cur_floor)
        
        if distance < min_distance:
            min_distance = distance
            next_lift = mock_props.index(lift)
    return next_lift+1 # return the lift number instead of index