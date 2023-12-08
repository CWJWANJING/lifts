import pytest
from main.index import app, update_pressed_floors, update_lift, get_next_lift, mock_props, liftInfo, TIMETOFLOOR
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
    expected_data = [asdict(x) for x in mock_props]
    actual_data = json.loads(response.data.decode("utf-8"))
    for i in range(len(actual_data)):
        assert actual_data[i] == expected_data[i]
    assert response.status_code == 200

mock_post = {
    "lift": 0, # lift index is 0
    "pressed": [0] # the index of the button
}

def test_post(client):
    response = client.post("/", json=mock_post)
    expected_data = {
            "code": 200,
            "message": "Data received"
    }
    assert json.loads(response.data.decode('utf-8')) == expected_data

def test_update_pressed_floors_append_queue():
    responseData = {
        "lift": 0, # lift index is 0
        "pressed": [0] # the index of the button
    }
    mock_props[0].queue = [0, 1]
    expected_data = mock_props
    expected_data[0].queue = [0, 1]
    actual_data = update_pressed_floors(responseData, mock_props)
    assert actual_data == expected_data

def test_update_pressed_floors_sort_queue():
    responseData = {
        "lift": 0, # lift index is 0
        "pressed": [1] # the index of the button
    }
    mock_props[0].queue = [1, 2]
    expected_data = mock_props
    expected_data[0].queue = [2, 1]
    actual_data = update_pressed_floors(responseData, mock_props)
    assert actual_data == expected_data

def test_add_pressed_floors():
    responseData = {
        "lift": 0, # lift index is 0
        "pressed": [0] 
    }
    mock_props[0].queue = []
    expected_data = mock_props
    expected_data[0].queue = [0]
    actual_data = update_pressed_floors(responseData, mock_props)
    assert actual_data == expected_data

def test_update_lift_when_one_floor_in_queue():
    lift_prop = liftInfo(
        [2, 1, 0],
        0,
        "up",
        [1]
    )
    mock_props = [
        lift_prop
    ]
    actual_data = update_lift(mock_props, TIMETOFLOOR)
    time.sleep(TIMETOFLOOR)
    expected_data = mock_props
    expected_data[0].queue = []
    assert actual_data == expected_data

def test_update_lift_when_two_floors_in_queue():
    lift_prop = liftInfo(
        [2, 1, 0],
        0,
        "up",
        [2, 1]
    )
    mock_props = [
        lift_prop
    ]
    actual_data = update_lift(mock_props, TIMETOFLOOR)
    time.sleep(TIMETOFLOOR)
    expected_data = mock_props
    expected_data[0].queue = [2]
    assert actual_data == expected_data

def test_get_next_lift_only_one_lift():
    lift_prop = liftInfo(
        [2, 1, 0],
        0,
        "up",
        [1]
    )
    mock_props = [
        lift_prop
    ]
    people_at_floor = 1 
    expected_result = 0
    actual_result = get_next_lift(mock_props, people_at_floor)
    assert actual_result == expected_result

def test_get_next_lift_when_two_lifts():
    lift_prop1 = liftInfo(
        [2, 1, 0],
        0,
        "up",
        [1]
    )
    lift_prop2 = liftInfo(
        [2, 1, 0],
        1,
        "down",
        [0]
    )

    mock_props = [
        lift_prop1,
        lift_prop2
    ]

    people_at_floor = 1
    expected_result = 2
    actual_result = get_next_lift(mock_props, people_at_floor)
    assert actual_result == expected_result

def test_get_next_lift_when_three_lifts_two_lifts_the_same():
    lift_prop1 = liftInfo(
        [2, 1, 0],
        0,
        "up",
        [1]
    )
    lift_prop2 = liftInfo(
        [2, 1, 0],
        1,
        "down",
        [0]
    )
    lift_prop3 = liftInfo(
        [2, 1, 0],
        1,
        "down",
        [0]
    )

    mock_props = [
        lift_prop1,
        lift_prop2,
        lift_prop3
    ]

    people_at_floor = 1
    expected_result = 2
    actual_result = get_next_lift(mock_props, people_at_floor)
    assert actual_result == expected_result

def test_get_next_lift_when_three_lifts():
    lift_prop1 = liftInfo(
        [2, 1, 0],
        0,
        "up",
        [1]
    )
    lift_prop2 = liftInfo(
        [2, 1, 0],
        1,
        "down",
        [0]
    )
    lift_prop3 = liftInfo(
        [2, 1, 0],
        2,
        "down",
        [1]
    )

    mock_props = [
        lift_prop1,
        lift_prop2,
        lift_prop3
    ]

    people_at_floor = 1
    expected_result = 2
    actual_result = get_next_lift(mock_props, people_at_floor)
    assert actual_result == expected_result