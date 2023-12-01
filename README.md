# lifts

# To run the fronend:
```cd``` to the frontend directory, and run ```npm run dev``` and visit ```http://localhost:3000``` to see the frontend result.

# To run the tests for frontend:
```cd``` to the frontend directory, and run ```npx cypress open```. And choose component or E2E test of your choice and run specific specs correspondingly.

# To run the backend:
```cd``` to the backend directory, and run ```. venv/bin/activate``` first to trigger the virtual environment. Then run ```./bootstrap.sh``` to start the backend.

# To run the tests for backend:
Make sure you are in the virtual environment and then run ```./tests/test.sh```.

# TODO:
* pass prop into POST body.
* update elevator (pos, time)