import pytest
from main.index import app, update_pressed_floors, update_lift, get_next_lift, mock_props, liftInfo
import time
from dataclasses import dataclass, asdict
import json

@pytest.fixture
def client():
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """

    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_get(client):
    response = client.get("/")
    expected_data = json.dumps([asdict(x) for x in mock_props])
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
    mock_props[0].queue = [1]
    expected_data = mock_props
    expected_data[0].queue = [0, 1]
    actual_data = update_pressed_floors(responseData, mock_props)
    assert actual_data == expected_data

def test_add_pressed_floors():
    responseData = {
        "lift": 0, # lift index is 0
        "pressed": [0] # the index of the button
    }
    mock_props[0].queue = []
    expected_data = mock_props
    expected_data[0].queue = [0]
    actual_data = update_pressed_floors(responseData, mock_props)
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
    lift_prop = liftInfo(
        ["2", "1", "G"],
        "G",
        "up",
        [1]
    )
    mock_props = [
        lift_prop
    ]
    people_at_floor = 1 # indedx 1, floor 1
    des_direction = "up"
    expected_result = 0
    actual_result = get_next_lift(mock_props, people_at_floor, des_direction)
    assert actual_result == expected_result

def test_get_next_lift_more_than_one_lift():
    lift_prop1 = liftInfo(
        ["2", "1", "G"],
        "G",
        "up",
        [1]
    )
    lift_prop2 = liftInfo(
        ["2", "1", "G"],
        "1",
        "down",
        [2]
    )

    mock_props = [
        lift_prop1,
        lift_prop2
    ]

    people_at_floor = 2 # index 0 -> floor G
    des_direction = "up"
    expected_result = 1
    actual_result = get_next_lift(mock_props, people_at_floor, des_direction)
    assert actual_result == expected_result