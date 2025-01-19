import requests
from bs4 import BeautifulSoup

url = "https://www.thrill-data.com/waits/park/dlr/disneyland/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

# Set to track rides we've already processed
processed_rides = set()

# Find all anchor tags with the title attribute containing the ride name
ride_name_elements = soup.find_all("a", title=True)

# Iterate through all found ride names
for ride in ride_name_elements:
    ride_name = ride.get_text(strip=True)

    # We are specifically looking for "Big Thunder Mountain Railroad"
    if "Big Thunder Mountain Railroad" in ride_name and ride_name not in processed_rides:
        # Mark the ride as processed
        processed_rides.add(ride_name)

        # Find the parent row <tr> and extract the wait time from the fourth <td>
        parent_tr = ride.find_parent("tr")

        # Look for the fourth <td> in the row (index 3 since it's zero-indexed)
        wait_time_td = parent_tr.find_all("td")[3]  # Fourth td for wait time

        # Get the title attribute to extract wait time (like "40 Minute Wait")
        wait_time = wait_time_td.find("div")["title"] if wait_time_td.find("div") else None

        # Look for the fifth <td> in the row (index 4) for the time (e.g., "5:40 PM")
        time_td = parent_tr.find_all("td")[4]  # Fifth td for the time
        time = time_td.get_text(strip=True) if time_td else None

        # Print the wait time and time in one line
        if wait_time and time:
            print(f"{ride_name}: Wait Time - {wait_time}, Time - {time}")
        else:
            print(f"{ride_name}: Wait Time - Not available, Time - Not available")
