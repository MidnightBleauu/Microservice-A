# Microservice-A
The implementation of microservice A sends in app alerts for price thresholds, weekly summaries, and high-volume alerts for cryptocurrencies.

# Communication Contract 
To request data from the microservice the program should send a POST request to the /notify endpoint with the paramaters. This enables the user to register price alert notifs for any asset(stock/cryptocurrency). 

## 1) Request Parameters: 
- **asset_symbol**: Cryptocurrency symbol (e.g., BTC, ETH).
- **alert_value**: The target price at which the user wants to be notified.
- **notification_type**: Type of alert (e.g., "Price Alert").
- **user_email**: The email address where the alert will be sent.


Examples: 
First: Define the data for registering the notification:
   ```python
   notif_data = {
       "asset_symbol": "BTC",
       "alert_value": 50000,
       "notification_type": "Price Alert",
       "user_email": "user@example.com"
   }
   ```

Second: Send the data to the `/notify` endpoint using the Python `requests` library:
   ```python
   import requests

   response = requests.post('http://localhost:5003/notify', json=notification_data)
   ```


Third: Checks if the request was indeed successful:
   ```python
   if response.status_code == 200:
       print("Notification alert registered successfully!")
       print("Response:", response.json())
   else:
       print("Error:", response.status_code, response.text)
   ```





## 2) Receiving Data from the Microservice

After the /notify endpoint has processed the request, then it returns a confirmation message in JSON format, and creates a JSON file that can be used to verify that the request was successful. Enabling it to be used for further processing to display the alert to the user. 


**Example Call to Receive Data**:
- When the request is successful, the response will contain the registered details:
  ```json
  {
      "asset_symbol": "BTC",
      "alert_value": 50000,
      "notification_type": "Price Alert",
      "user_email": "user@example.com",
      "message": "Notification alert registered successfully!"
  }
  ```


**Display the Response**:
1. Print the response details:
   ```python
   response_data = response.json()
   print("Response Data:", response_data)
