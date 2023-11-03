import unittest
import index
from index import *

def test_updatePressedFloors():
    responseData = {
        "lift": 0, # lift index is 0
        "pressed": "2"
    }
    expected_data = [["2"]]
    print(updatePressedFloors(responseData, pressed_floors))
    actual_data = updatePressedFloors(responseData, pressed_floors)
    assert actual_data == expected_data

if __name__ == '__main__':
    # unittest.main()
    test_updatePressedFloors()