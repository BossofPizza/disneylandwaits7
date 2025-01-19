import time
import requests
from bs4 import BeautifulSoup
import httpx

# Pushover credentials
api_token = "amqmtqh5hjne37tk68keg9iwytjwhd"
user_key = "unb249suwmpir19ng1zguhxqxyyfgd"

# Define the URL
url = "https://www.thrill-data.com/waits/park/dlr/disneyland/"

def send_notification():
    # Send a GET request to retrieve the page's content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all anchor tags with the title attribute containing the ride name
    ride_name_elements = soup.find_all("a", title=True)

    # Iterate through all found ride names to find Space Mountain
    for ride in ride_name_elements:
        ride_name = ride.get_text(strip=True)

        if ride_name == "Space Mountain":
            parent_tr = ride.find_parent("tr")
            td_elements = parent_tr.find_all("td")

            if len(td_elements) >= 4:
                wait_time_td = td_elements[3]
                wait_time = wait_time_td.find("div")["title"] if wait_time_td.find("div") else None
            else:
                wait_time = "closed"

            if wait_time == "closed":
                message = "Space Mountain is currently closed."
            else:
                message = f"Current Wait Time: {wait_time}"

            # Send the notification using Pushover
            pushover_response = httpx.post(
                "https://api.pushover.net/1/messages.json",
                data={
                    "token": api_token,
                    "user": user_key,
                    "title": "Space Mountain Wait Time",
                    "message": message
                }
            )

            print(f"Push Notification Sent: {message}")
            break  # Exit the loop once we find Space Mountain

while True:
    send_notification()
    time.sleep(300)  # Wait for 5 minutes (300 seconds)
