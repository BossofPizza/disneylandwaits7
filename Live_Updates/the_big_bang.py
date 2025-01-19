import requests
from bs4 import BeautifulSoup
import csv
import os

# URL for Disneyland wait times
url = "https://www.thrill-data.com/waits/park/dlr/disneyland/"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Ride name to look for
ride_name = "Big Thunder Mountain Railroad"

# Find all anchor tags with the title attribute containing the ride name
ride_name_elements = soup.find_all("a", title=True)

# Extract the wait time for the specific ride
current_wait_time = None
for ride in ride_name_elements:
    if ride_name in ride.get_text(strip=True):
        parent_tr = ride.find_parent("tr")
        if parent_tr:
            wait_time_td = parent_tr.find_all("td")[3]  # Fourth td for wait time
            wait_time = wait_time_td.find("div")["title"] if wait_time_td.find("div") else None
            if wait_time:
                current_wait_time = wait_time.split(" ")[0]  # Extract the number part
                break

# If no wait time found
if current_wait_time is None:
    print("Ride not found or wait time not available.")
    exit()

# File paths for saving current and previous data
current_file = 'current_wait_times.csv'
previous_file = 'previous_wait_times.csv'

# Read the previous wait time for the ride if the previous file exists
previous_wait_time = None
if os.path.exists(previous_file):
    with open(previous_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["ride_name"] == ride_name:
                previous_wait_time = row["wait_time"]

# Compare current wait time with the previous one
if previous_wait_time:
    if current_wait_time == previous_wait_time:
        print(f"Stayed the same: {current_wait_time}")
    else:
        print(f"Time Changed: {previous_wait_time} -> {current_wait_time}")
else:
    print(f"New ride: {ride_name} with wait time {current_wait_time}")

# Save the current data to the current file
if os.path.exists(current_file):
    with open(current_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["ride_name", "wait_time"])
        writer.writerow({"ride_name": ride_name, "wait_time": current_wait_time})
else:
    with open(current_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["ride_name", "wait_time"])
        writer.writeheader()
        writer.writerow({"ride_name": ride_name, "wait_time": current_wait_time})

# Save the current wait time as the previous wait time for the next run
if os.path.exists(previous_file):
    os.remove(previous_file)

os.rename(current_file, previous_file)

print("Data saved.")
