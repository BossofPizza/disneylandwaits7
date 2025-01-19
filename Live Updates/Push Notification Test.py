import requests
from bs4 import BeautifulSoup
from pushbullet import Pushbullet
import time

# Set up Pushbullet API
api_key = "o.qsbbsuZVEE3HGrkftTBPbxqwAzbDV1Ao12"  # Replace with your API key
pb = Pushbullet(api_key)

# Define the URL
url = "https://www.thrill-data.com/waits/park/dlr/disneyland/"

# Send a GET request to retrieve the page's content
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find all anchor tags with the title attribute containing the ride name
ride_name_elements = soup.find_all("a", title=True)

# Iterate through all found ride names to find Space Mountain
for ride in ride_name_elements:
    ride_name = ride.get_text(strip=True)

    # Only check Space Mountain
    if ride_name == "Space Mountain":
        # Find the parent row <tr> and extract the wait time
        parent_tr = ride.find_parent("tr")

        # Look for the fourth <td> in the row (index 3 since it's zero-indexed)
        wait_time_td = parent_tr.find_all("td")[3]  # Fourth td for wait time

        # Get the title attribute to extract wait time (like "40 Minute Wait")
        wait_time = wait_time_td.find("div")["title"] if wait_time_td.find("div") else None

        # If wait time is found, send the push notification
        if wait_time:
            notification = pb.push_note(f"Space Mountain Wait Time", f"Current Wait Time: {wait_time}")
            print(f"Push Notification Sent: {notification}")
        break  # Exit the loop once we find Space Mountain
