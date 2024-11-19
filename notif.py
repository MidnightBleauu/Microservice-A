# Author: Pramit Patel
# Date: 11/18/24
# Description: This microservice monitors cryptocurrency prices and sends in-app alerts for price thresholds and saves alerts in JSON format.

from flask import Flask, request, jsonify
import threading
import time
import json
import os

app = Flask(__name__)

# Store alert data in memory
alerts = []

# Store in-app notifications in memory
user_notifications = {}

# JSON file to store alert notifications
ALERTS_JSON_FILE = "alerts.json"


# Utility function to save alerts to a JSON file
def save_alert_to_json(alert_data):
    # If file doesn't exist, create an empty one
    if not os.path.exists(ALERTS_JSON_FILE):
        with open(ALERTS_JSON_FILE, 'w') as f:
            json.dump([], f)

    # Append the new alert to the file
    with open(ALERTS_JSON_FILE, 'r+') as f:
        alerts_list = json.load(f)
        alerts_list.append(alert_data)
        f.seek(0)
        json.dump(alerts_list, f, indent=4)


# Endpoint registers alerts
@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()

    # Gets  informations
    asset_symbol = data.get('asset_symbol')
    alert_value = data.get('alert_value')
    notification_type = data.get('notification_type')
    user_email = data.get('user_email')

    # Data validation
    if not all([asset_symbol, alert_value, notification_type, user_email]):
        return jsonify({"error": "Missing required request parameters."}), 400

    # Store the alert data
    alert = {
        "asset_symbol": asset_symbol,
        "alert_value": float(alert_value),
        "notification_type": notification_type,
        "user_email": user_email
    }
    alerts.append(alert)

    # Saves alert
    save_alert_to_json(alert)

    return jsonify({
        "message": "Notification alert registered successfully!",
        "alert": alert
    }), 200


# Endpoint to fetch in-app notifications for teh users
@app.route('/alerts/<user_email>', methods=['GET'])
def get_alerts(user_email):
    if user_email not in user_notifications:
        return jsonify({"message": "No alerts found for this user."}), 200

    return jsonify({"alerts": user_notifications[user_email]}), 200


# Endpoint to update current price of an asset
@app.route('/update_price', methods=['POST'])
def update_price():
    data = request.get_json()

    # Extract necessary information
    asset_symbol = data.get('asset_symbol')
    current_price = data.get('current_price')

    # Data validation
    if not all([asset_symbol, current_price]):
        return jsonify({"error": "Missing required request parameters."}), 400

    # Iterate over alerts and generate notifications
    for alert in alerts:
        if alert['asset_symbol'] == asset_symbol and current_price >= alert['alert_value']:
            user_email = alert['user_email']
            notification_message = f"The price of {asset_symbol} has reached the threshold of {alert['alert_value']}."

            if user_email not in user_notifications:
                user_notifications[user_email] = []

            user_notifications[user_email].append({
                "asset_symbol": asset_symbol,
                "current_price": current_price,
                "notification_type": alert['notification_type'],
                "message": notification_message
            })

            # Saves info to json file
            triggered_alert = {
                "user_email": user_email,
                "asset_symbol": asset_symbol,
                "current_price": current_price,
                "notification_type": alert['notification_type'],
                "message": notification_message
            }
            save_alert_to_json(triggered_alert)

            print(f"Notification created for {user_email}: {notification_message}")

    return jsonify({"message": "Price update processed successfully."}), 200


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)