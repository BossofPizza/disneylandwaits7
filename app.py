from flask import Flask, render_template_string
import disneyland_average_vs_prediction  # Replace this with your script filename (without .py)
import requests
import time
from threading import Timer

app = Flask(__name__)

# Pushover API credentials
PUSHOVER_USER_KEY = 'unb249suwmpir19ng1zguhxqxyyfgd'
PUSHOVER_API_TOKEN = 'amqmtqh5hjne37tk68keg9iwytjwhd'
PUSHOVER_URL = 'https://api.pushover.net:443/1/messages.json'

# Function to send a Pushover notification
def send_pushover_notification(message):
    data = {
        'token': PUSHOVER_API_TOKEN,
        'user': PUSHOVER_USER_KEY,
        'message': message
    }
    response = requests.post(PUSHOVER_URL, data=data)
    return response

@app.route('/')
def home():
    output = []

    for ride_name in disneyland_average_vs_prediction.ride_names:
        current_wait_time = disneyland_average_vs_prediction.get_current_wait_time(ride_name)

        if current_wait_time is None:
            output.append(f"Wait time not available for {ride_name}.")
        else:
            if ride_name == disneyland_average_vs_prediction.ride_name_big_thunder:
                predicted_time = disneyland_average_vs_prediction.predicted_time_big_thunder
            elif ride_name == disneyland_average_vs_prediction.ride_name_space_mountain:
                predicted_time = disneyland_average_vs_prediction.predicted_time_space_mountain
            elif ride_name == disneyland_average_vs_prediction.ride_name_matterhorn:
                predicted_time = disneyland_average_vs_prediction.predicted_time_matterhorn

            category = disneyland_average_vs_prediction.categorize_wait_time(int(current_wait_time), predicted_time)
            ride_output = f"{ride_name} - Wait Time {current_wait_time} minutes, ({category}) time to go"
            output.append(ride_output)

            # Send the output as a Pushover notification
            send_pushover_notification(ride_output)

    html_output = "<br>".join(output)
    return render_template_string(f"<html><body>{html_output}</body></html>")

# Function to run the app every 5 minutes
def run_every_5_minutes():
    app.run(debug=True)
    Timer(300, run_every_5_minutes).start()  # Run the function every 5 minutes (300 seconds)

if __name__ == '__main__':
    # Start the Flask app and schedule to run every 5 minutes
    run_every_5_minutes()

