import requests
import time
import random

# Configuration for the target API endpoint
api_url = 'http://localhost:5000/input'  # Adjust this to your actual API URL

def post_data():
    """
    This function generates and posts data to the specified API endpoint
    at different intervals for each variable.
    """
    while True:
        # Generate random data within specified ranges
        data = {
            'X': random.uniform(-1, 1),
            'Y': random.uniform(-1, 1),
            'Z': random.uniform(-1, 1),
            'pitch': random.uniform(-1, 1),
            'roll': random.uniform(-1, 1),
            'yaw': random.uniform(-1, 1),
            'claw': random.choice([-1, 0, 1]),  # Assuming claw can also take -1 as a valid input
            'torp1': random.choice([True, False]),
            'torp2': random.choice([True, False])
        }

        # Send the data as a POST request to the server
        response = requests.post(api_url, json=data)
        print(f'Status Code: {response.status_code}, Response: {response.text}')

        # Sleep for a random time between updates
        time.sleep(random.uniform(0.5, 2.0))  # Update interval between 0.5 to 2 seconds

if __name__ == '__main__':
    post_data()
