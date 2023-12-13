# lifts

# To run the fronend:
```cd``` to the frontend directory, and run ```npm run dev``` and visit ```http://localhost:3000``` to see the frontend result.

# To run the tests for frontend:
```cd``` to the frontend directory, and run ```npx cypress open```. And choose component or E2E test of your choice and run specific specs correspondingly.

# To run the backend:
```cd``` to the backend directory, and run ```. venv/bin/activate``` first to trigger the virtual environment. Then run ```./bootstrap.sh``` to start the backend.

# To run the tests for backend:
Make sure you are in the virtual environment and then run ```./tests/test.sh``` or ```pytest```.

# The logic
User clicked the floor they would like to go, and the button will change color as they click on it. Then after some fixed time the lift will arrive at the destination floor. There are texts displaying which direction are we going and we are currently at which floor.

To add more lifts, in the backend folder, file ```index.py```, replicate line 19 (and adjust the field values to your liking) and add the new lift_prop to line 21 ```mock_props```

# The demo
[the demo]([lift_web_app.mov](https://youtu.be/ssRi6c8ztoI))

# Self reflection
I got to practice more React methods, Cypress methods and Pytest. But I need to work on my system design skill.
