from flask import Flask, request
from flask_cors import CORS
import time
from dataclasses import dataclass, asdict
import json
from typing import List
import threading

app = Flask(__name__)
CORS(app)

@dataclass
class liftInfo:
    floors: List[int]
    cur_floor: int
    direction: str
    queue: List[int]

floors = [2, 1, 0] # all lifts go to the same floors

lift_prop1 = liftInfo(
    floors,
    0,
    "-",
    []
)

lift_prop2 = liftInfo(
    floors,
    1,
    "-",
    []
)

mock_props = [
    lift_prop1,
    lift_prop2
]

TIMETOFLOOR = 5 # sec

@app.route("/")
def get_liftInfo():
    pre_data = update_lift(mock_props, TIMETOFLOOR)
    res_data = []
    for r in pre_data:
        res_data.append(asdict(r))
    return res_data, 200

@app.route("/", methods=['POST'])
def receive_liftQueue():
    input = request.get_json()
    update_pressed_floors(input, mock_props)
    res = {
            "code": 200,
            "message": "Data received"
    }
    return res

def update_pressed_floors(response_data, mock_props):
    lift_num = response_data['lift']
    if len(mock_props[lift_num].queue) == 0:
        mock_props[lift_num].queue = list(response_data["pressed"])
        if len(response_data["pressed"]) == 1 and (response_data["pressed"][0] > mock_props[lift_num].cur_floor):
                mock_props[lift_num].direction = "up"
        elif len(response_data["pressed"]) == 1 and (response_data["pressed"][0] < mock_props[lift_num].cur_floor):
                mock_props[lift_num].direction = "down"
    else:
        if isinstance(response_data["pressed"], list) and response_data["pressed"] != []:
            if len(response_data["pressed"]) == 1 and (response_data["pressed"][0] > mock_props[lift_num].cur_floor):
                mock_props[lift_num].direction = "up"
            elif len(response_data["pressed"]) == 1 and (response_data["pressed"][0] < mock_props[lift_num].cur_floor):
                mock_props[lift_num].direction = "down"
            else:
                preData = int(str(response_data["pressed"][-1]).strip("[]"))
                mock_props[lift_num].queue.append(preData)

    if mock_props[lift_num].direction == "up":
        mock_props[lift_num].queue.sort(reverse=True)
    else:
        mock_props[lift_num].queue.sort()
    return mock_props

def update_lift(mock_props, TIMETOFLOOR):
    # Create an event to signal when the delay is over
    event = threading.Event()

    # Define a function to remove the end of the list after the delay
    def remove_end():
        event.wait(TIMETOFLOOR)
        for i in range(len(mock_props)):
            if len(mock_props[i].queue) != 0:
                last_floor = mock_props[i].queue[-1]
                mock_props[i].cur_floor = last_floor
                mock_props[i].queue.remove(last_floor)

    # Start a new thread to run the remove_end function
    thread = threading.Thread(target=remove_end)
    thread.start()

    # Ensure that the main thread does not wait for the delay
    event.set()
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
    return next_lift