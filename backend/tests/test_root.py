import pytest
from main.index import app, update_pressed_floors, update_lift, get_next_lift
import time

@pytest.fixture
def client():
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """

    app.config['TESTING'] = True
    client = app.test_client()

    yield client

mock_props = [{
    "currFloor": "G", 
    "direction": "up", 
    "floors": ["2","1","G"]
    }]

def test_get(client):
    response = client.get("/")
    expected_data = str(mock_props).replace(" ", "").replace("\'", "\"")+"\n"
    assert response.data.decode("utf-8") == expected_data
    assert response.status_code == 200

mock_post = {
    "lift": 0, # lift index is 0
    "pressed": [0] # the index of the button
}

def test_post(client):
    response = client.post("/", json=mock_post)
    expected_data = "Data received"
    assert response.data.decode("utf-8") == expected_data
    assert response.status_code == 200

def test_update_pressed_floors():
    responseData = {
        "lift": 0, # lift index is 0
        "pressed": [0] # the index of the button
    }
    pressed_floors = [[1]]
    expected_data = [[0, 1]]
    actual_data = update_pressed_floors(responseData, pressed_floors)
    assert actual_data == expected_data

def test_add_pressed_floors():
    responseData = {
        "lift": 0, # lift index is 0
        "pressed": [0] # the index of the button
    }
    pressed_floors = [[]]
    expected_data = [[0]]
    actual_data = update_pressed_floors(responseData, pressed_floors)
    assert actual_data == expected_data

def test_update_lift():
    state = [[2, [1]]] # [[[currFloor], [queue]]]
    t = 3
    last_updated = 0
    actual_state = update_lift(state, t, last_updated)
    liftOperateTime = 3 # sec
    time.sleep(liftOperateTime)
    expected_state = [[1, []]]
    assert actual_state == expected_state

def test_get_next_lift_only_one_lift():
    state = [[2, [1]]] # [[[currFloor], [queue]]]
    people_at_floor = 1
    actual_result = 0
    expected_result = get_next_lift(state, mock_props, people_at_floor)
    assert actual_result == expected_result

def test_get_next_lift_more_than_one_lift():
    mock_props = [{
        "currFloor": "G", 
        "direction": "up", 
        "floors": ["2","1","G"]
    },
    {
        "currFloor": "2", 
        "direction": "down", 
        "floors": ["2","1","G"]
    }]
    people_at_floor = 0 # index 0 - floor 2
    state = [[2, [1]], [1, [2]]] # [[[currFloor], [queue]]]
    actual_result = 0
    expected_result = get_next_lift(state, mock_props, people_at_floor)
    assert actual_result == expected_result