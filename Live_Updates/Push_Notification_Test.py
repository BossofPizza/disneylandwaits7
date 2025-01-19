import streamlit as st
import requests
from bs4 import BeautifulSoup
from pushbullet import Pushbullet

# Define your Pushover API token and User key
api_token = "amqmtqh5hjne37tk68keg9iwytjwhd"  # Replace with your Pushover API token
user_key = "unb249suwmpir19ng1zguhxqxyyfgd"  # Replace with your Pushover User key

# Define the URL for the wait times
url = "https://www.thrill-data.com/waits/park/dlr/disneyland/"

# Function to get wait time for Space Mountain
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

# Function to send a Pushover notification
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

# Streamlit layout
st.title("Disneyland Wait Times Checker")
st.write("Click the button below to get the current wait time for Space Mountain!")

if st.button("Get Wait Time"):
    message = get_wait_time()
    st.write(message)  # Display the message on Streamlit page

