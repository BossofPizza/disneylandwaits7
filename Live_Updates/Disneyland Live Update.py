import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
from datetime import datetime, timedelta

# URL for Disneyland wait times (Thrill Data)
url = "https://www.thrill-data.com/waits/park/dlr/disneyland/"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# List of target rides (Big Thunder, Space Mountain, Matterhorn)
target_rides = [
    "Big Thunder Mountain Railroad", "Space Mountain", "Matterhorn Bobsleds"
]

# List to store results
rides_info = []

# Find all anchor tags with the title attribute containing the ride name
ride_name_elements = soup.find_all("a", title=True)

# Extract actual wait times from Thrill Data
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
                    "actual_wait_time": wait_time_number
                })

# Save the actual data to CSV (for later use)
with open("actual_disneyland_wait_times.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["ride_name", "actual_wait_time"])
    writer.writeheader()
    for ride in rides_info:
        writer.writerow(ride)

print("Actual data saved to 'actual_disneyland_wait_times.csv'")


# Function to load projected data (CSV files)
def load_ride_data(ride_name, base_dir):
    all_data = []
    for month in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]:
        file_name = f"{ride_name}, {month} 2024, Disneyland.csv"
        file_path = os.path.join(base_dir, ride_name, file_name)
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
            month_data = pd.read_csv(file_path)
            month_data['Date/Time'] = pd.to_datetime(month_data['Date/Time'])
            month_data['Date'] = month_data['Date/Time'].dt.date
            month_data['Day'] = month_data['Date/Time'].dt.day_name()
            month_data['Hour'] = month_data['Date/Time'].dt.hour
            month_data['Month'] = month_data['Date/Time'].dt.month_name()  # Added Month column
            all_data.append(month_data)
        else:
            print(f"File not found: {file_path}")

    if all_data:
        all_data_df = pd.concat(all_data, ignore_index=True)
        return all_data_df
    else:
        raise ValueError(f"No data found for {ride_name}")


# Path to the directory containing the ride folders
base_dir = "C:/Users/luked/PycharmProjects/disneyland/Live_Updates"

# Load data for the three target rides
try:
    big_thunder_data = load_ride_data('Big Thunder Mountain Railroad', base_dir)
    space_mountain_data = load_ride_data('Space Mountain', base_dir)
except ValueError as e:
    print(e)
    big_thunder_data = space_mountain_data = None

# Matterhorn Bobsleds doesn't have CSV data, so we skip it and only rely on actual wait times from Thrill Data
matterhorn_data = None


# Function to predict and categorize ride wait time
def predict_and_categorize_ride_for_today(ride_data, thrill_actual_data, ride_name):
    today = datetime.today()
    day = today.strftime('%A')
    month = today.strftime('%B')
    hour = today.hour

    if ride_data is not None:
        # Compute the rolling average wait time by focusing on surrounding days (5 days before and after)
        date_range = pd.date_range(today - timedelta(days=5), today + timedelta(days=5))
        ride_data_filtered = ride_data[ride_data['Date'].isin(date_range.date)]

        # Calculate the average wait time for this specific day/hour using the surrounding data
        avg_wait_time = ride_data_filtered.groupby(['Day', 'Month', 'Hour'])['Wait Time'].mean().reset_index()

        # Get the predicted (projected) wait time for the given day, month, and hour
        avg_time = avg_wait_time[
            (avg_wait_time['Day'] == day) & (avg_wait_time['Month'] == month) & (avg_wait_time['Hour'] == hour)][
            'Wait Time'].mean()

        # Actual wait time from "Thrill Data" for today
        actual_wait_time = thrill_actual_data.get(ride_name, {}).get(str(today.date()), None)

        if actual_wait_time is None:
            # If the actual wait time is missing, fallback to the rolling average of surrounding days
            actual_wait_time = ride_data_filtered.groupby(['Day', 'Month', 'Hour'])['Wait Time'].mean().reset_index()[
                (ride_data_filtered['Day'] == day) & (ride_data_filtered['Month'] == month) & (
                            ride_data_filtered['Hour'] == hour)
                ]['Wait Time'].mean()

        return actual_wait_time, avg_time, categorize_wait_time(actual_wait_time, avg_time)
    else:
        # If there's no data, only return actual wait time from Thrill Data
        actual_wait_time = thrill_actual_data.get(ride_name, {}).get(str(today.date()), None)
        return actual_wait_time, None, None


# Function to categorize the wait times
def categorize_wait_time(actual_wait_time, average_wait_time):
    if actual_wait_time < average_wait_time - 15:
        return "GREAT TIME to go"
    elif actual_wait_time < average_wait_time - 5:
        return "GOOD TIME to go"
    elif abs(actual_wait_time - average_wait_time) <= 5:
        return "AVERAGE TIME to go"
    elif actual_wait_time > average_wait_time + 5:
        return "BAD TIME to go"
    else:
        return "TERRIBLE TIME to go"


# Load the actual wait times from the CSV generated earlier (for Thrill Data)
actual_data = {}
with open('actual_disneyland_wait_times.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        actual_data[row['ride_name']] = {str(datetime.today().date()): int(row['actual_wait_time'])}


# Get today's data for the three target rides
def get_today_data():
    rides = ['Big Thunder Mountain Railroad', 'Space Mountain', 'Matterhorn Bobsleds']
    results = {}
    for ride in rides:
        ride_data = {
            'Big Thunder Mountain Railroad': big_thunder_data,
            'Space Mountain': space_mountain_data,
            'Matterhorn Bobsleds': matterhorn_data  # We are not using CSV data for Matterhorn
        }[ride]

        actual_wait_time, avg_time, category = predict_and_categorize_ride_for_today(ride_data, actual_data, ride)
        results[ride] = {
            'Actual Wait Time': actual_wait_time,
            'Projected Wait Time': avg_time,
            'Category': category
        }

    return results


# Get today's data for the three rides
today_data = get_today_data()

# Print the results for today
for ride, data in today_data.items():
    print(
        f"{ride} - Actual: {data['Actual Wait Time']} min, Projected: {data['Projected Wait Time']} min, Category: {data['Category']}")
