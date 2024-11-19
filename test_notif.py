import requests

# Base URL for the notification microservice
BASE_URL = "http://localhost:5003"

# Function to trigger a notification
def test_notification():
    # All necessary data to send to the microservice
    notification_data = {
        "asset_symbol": "BTC",
        "alert_value": 50000,  # Use a number here instead of a string
        "notification_type": "Price Alert",
        "user_email": "testuser@example.com"  # Add user email to the request
    }

    # Send a POST request to the /notify endpoint
    response = requests.post(f"{BASE_URL}/notify", json=notification_data)

    # Check and print the response
    if response.status_code == 200:
        print("Notification registered successfully.")
        print("Response:", response.json())
    else:
        print("Failed to register notification.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

if __name__ == "__main__":
    test_notification()