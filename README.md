# lifts

# To run the fronend:
```cd``` to the frontend directory, and run ```npm run dev``` and visit ```http://localhost:3000``` to see the frontend result.

# To run the tests for frontend:
```cd``` to the frontend directory, and run ```npx cypress open```. And choose component or E2E test of your choice and run specific specs correspondingly.

# To run the backend:
```cd``` to the backend directory, and run ```. venv/bin/activate``` first to trigger the virtual environment. Then run ```./bootstrap.sh``` to start the backend.

# To run the tests for backend:
Make sure you are in the virtual environment and then run ```./tests/test.sh``` or ```pytest```.

# TODO:
* check update_lift (pos, time) logic - continue, more test cases
* refactor state into a dataclass. e.g. state[0].cur_floor
* store pressed_floor info into the state variable - ```[(lift1CurrFloor, lift1Queue), (lift2CurrFloor, lift2Queue)]```
* pass prop into POST body.