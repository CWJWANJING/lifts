import pytest
from main.index import app, update_pressed_floors
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
    pressed_floors = [[2]]
    expected_data = [[0, 2]]
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
    state = [(2, [1])] # [(currFloor, queue)]
    actual_queue = update_lift()
    liftOperateTime = 3 # sec
    time.sleep(liftOperateTime)
    expected_queue = [[]]
    assert actual_queue == expected_queue