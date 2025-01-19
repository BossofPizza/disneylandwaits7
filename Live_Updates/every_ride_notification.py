import requests
import json
from bs4 import BeautifulSoup

# Pushover API info
pushover_user_key = "unb249suwmpir19ng1zguhxqxyyfgd"  # Replace with your Pushover User Key
pushover_api_token = "amqmtqh5hjne37tk68keg9iwytjwhd"  # Replace with your Pushover API Token
pushover_url = "https://api.pushover.net:443/1/messages.json"

# URL for Disneyland wait times
url = "https://www.thrill-data.com/waits/park/dlr/disneyland/"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# List of rides to find
target_rides = [
    "it's a small world\" Holiday",
    "Alice in Wonderland",
    "Astro Orbitor",
    "Autopia",
    "Big Thunder Mountain Railroad",
    "Buzz Lightyear Astro Blasters",
    "Casey Jr. Circus Train",
    "Chip 'n' Dale's GADGETcoaster",
    "Dumbo the Flying Elephant",
    "Finding Nemo Submarine Voyage",
    "Haunted Mansion",
    "Indiana Jones Adventure",
    "Jungle Cruise",
    "King Author Carrousel",
    "Mad Tea Party",
    "Matterhorn Bobsled",
    "Mickey's House and Meet Mickey Mouse",
    "Millennium Falcon: Smugglers Run",
    "Mr. Toad's Wild Ride",
    "Peter Pan's Flight",
    "Pinocchio's Daring Journey",
    "Pirates of the Caribbean",
    "Roger Rabbit's Car Toon Spin",
    "Snow White's Enchanted Wish",
    "Space Mountain",
    "Star Tours - The Adventures Continue",
    "Star Wars: Rise of the Resistance",
    "Storybook Land Canal Boats",
    "The Many Adventures of Winnie the Pooh",
    "Tiana's Bayou Adventure"
]

# Dictionary to store current rides info
current_rides_info = {}

# Load previous rides info from the JSON file
previous_rides_info = {}
try:
    with open("previous_rides_info.json", "r") as file:
        previous_rides_info = json.load(file)
except FileNotFoundError:
    pass  # If the file doesn't exist, we'll just continue with an empty dictionary

# Find all anchor tags with the title attribute containing the ride name
ride_name_elements = soup.find_all("a", title=True)

# Extract wait time for all the target rides
for ride in ride_name_elements:
    ride_name = ride.get_text(strip=True)

    # Only process the rides in the target list
    if ride_name in target_rides:
        # Find the parent row <tr>
        parent_tr = ride.find_parent("tr")

        if parent_tr:
            # Check if we can access the fourth <td> for wait time
            try:
                wait_time_td = parent_tr.find_all("td")[3]  # Fourth td for wait time
                wait_time = wait_time_td.find("div")["title"] if wait_time_td.find("div") else None

                if wait_time:
                    # Extract the number part of the wait time (removing extra text like "Minute Wait")
                    wait_time_number = wait_time.split(" ")[0]
                    current_rides_info[ride_name] = wait_time_number
                else:
                    current_rides_info[ride_name] = "Closed"
            except IndexError:
                # If out of range, mark the ride as "Closed"
                current_rides_info[ride_name] = "Closed"

# Accumulate all changes in a single message
changes_message = ""

# Compare current data with previous data for each ride
for ride_name, current_wait_time in current_rides_info.items():
    if ride_name in previous_rides_info:
        previous_wait_time = previous_rides_info[ride_name]
        if current_wait_time != previous_wait_time:
            changes_message += f"{ride_name}: Time Changed {previous_wait_time} -> {current_wait_time}\n"
    else:
        changes_message += f"{ride_name}: New ride\n"

# If there are any changes, send one notification with all the changes
if changes_message:
    payload = {
        "user": pushover_user_key,
        "token": pushover_api_token,
        "message": changes_message,
    }
    requests.post(pushover_url, data=payload)

# Save the current data in the JSON file for the next run
with open("previous_rides_info.json", "w") as file:
    json.dump(current_rides_info, file)

print("Data comparison complete. Notification sent.")
