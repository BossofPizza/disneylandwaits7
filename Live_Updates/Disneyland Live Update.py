import requests
from bs4 import BeautifulSoup
import csv

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

# List to store results
rides_info = []

# Find all anchor tags with the title attribute containing the ride name
ride_name_elements = soup.find_all("a", title=True)

# Iterate through each ride
for ride in ride_name_elements:
    ride_name = ride.get_text(strip=True)

    # Check if this ride is in the list of target rides
    if ride_name in target_rides:
        # Find the parent row <tr>
        parent_tr = ride.find_parent("tr")

        # Ensure we have the correct row and extract the wait time (first number in the fourth td)
        if parent_tr:
            wait_time_td = parent_tr.find_all("td")[3]  # Fourth td for wait time
            wait_time = wait_time_td.find("div")["title"] if wait_time_td.find("div") else None

            if wait_time:
                # Extract the number part of the wait time (removing extra text like "Minute Wait")
                wait_time_number = wait_time.split(" ")[0]
                rides_info.append({
                    "ride_name": ride_name,
                    "wait_time": wait_time_number
                })

# Save the data to CSV
with open("disneyland_wait_times.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["ride_name", "wait_time"])
    writer.writeheader()
    for ride in rides_info:
        writer.writerow(ride)

print("Data saved to 'disneyland_wait_times.csv'")
