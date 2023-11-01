from __init__ import client

mock_props = [{
    "currFloor": "G", 
    "direction": "up", 
    "floors": [2,1,"G"]
    }]

def test_get(client):
    response = client.get("/")
    expected_data = str(mock_props).replace(" ", "").replace("\'", "\"")+"\n"
    assert response.data.decode("utf-8") == expected_data
    assert response.status_code == 200