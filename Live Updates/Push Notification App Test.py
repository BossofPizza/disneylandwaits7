from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from pushbullet import Pushbullet

app = Flask(__name__)

# Define your Pushover API token and User key
api_token = "your-api-token"  # Replace with your Pushover API token
user_key = "your-user-key"  # Replace with your Pushover User key

# Define the URL for the wait times
url = "https://www.thrill-data.com/waits/park/dlr/disneyland/"


@app.route('/')
def home():
    return render_template('index.html')  # Create an HTML page for the front-end


@app.route('/get_wait_time')
def get_wait_time():
    # Send a GET request to retrieve the page's content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all anchor tags with the title attribute containing the ride name
    ride_name_elements = soup.find_all("a", title=True)
    for ride in ride_name_elements:
        ride_name = ride.get_text(strip=True)

        # Only check Space Mountain
        if ride_name == "Space Mountain":
            parent_tr = ride.find_parent("tr")
            wait_time_td = parent_tr.find_all("td")[3]  # Fourth td for wait time

            # Extract the wait time or mark as closed if not available
            wait_time = wait_time_td.find("div")["title"] if wait_time_td.find("div") else "Closed"

            # Send notification using Pushover
            if wait_time != "Closed":
                message = f"Current Wait Time for Space Mountain: {wait_time}"
            else:
                message = "Space Mountain is currently closed."

            # Send the notification via Pushover
            send_pushover_notification(message)
            return message  # Display the message on the webpage

    return "Space Mountain not found!"


def send_pushover_notification(message):
    """Send a notification to the user via Pushover."""
    payload = {
        "token": api_token,
        "user": user_key,
        "message": message
    }
    # Send the request to Pushover API
    response = requests.post("https://api.pushover.net:443/1/messages.json", data=payload)

    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print("Failed to send notification.")


if __name__ == '__main__':
    app.run(debug=True)
