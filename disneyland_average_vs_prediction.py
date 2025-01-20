import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime

# URL for Disneyland wait times
url = "https://www.thrill-data.com/waits/park/dlr/disneyland/"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Ride names to look for
ride_names = ["Big Thunder Mountain Railroad", "Matterhorn Bobsleds", "Space Mountain"]


# Function to get the current wait time for a ride
def get_current_wait_time(ride_name):
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

    return current_wait_time


# Function to categorize the wait times
def categorize_wait_time(actual_wait_time, predicted_wait_time):
    if actual_wait_time < predicted_wait_time - 15:
        return "GREAT TIME to go"
    elif actual_wait_time < predicted_wait_time - 5:
        return "GOOD TIME to go"
    elif abs(actual_wait_time - predicted_wait_time) <= 5:
        return "AVERAGE TIME to go"
    elif actual_wait_time > predicted_wait_time + 5:
        return "BAD TIME to go"
    else:
        return "TERRIBLE TIME to go"


# Function to load all months' CSV files into a dictionary for a specific ride
def load_ride_data(ride_name):
    months_data = {
        'January': f'{ride_name}, January 2024, Disneyland.csv',
        'February': f'{ride_name}, February 2024, Disneyland.csv',
        'March': f'{ride_name}, March 2024, Disneyland.csv',
        'April': f'{ride_name}, April 2024, Disneyland.csv',
        'May': f'{ride_name}, May 2024, Disneyland.csv',
        'June': f'{ride_name}, June 2024, Disneyland.csv',
        'July': f'{ride_name}, July 2024, Disneyland.csv',
        'August': f'{ride_name}, August 2024, Disneyland.csv',
        'September': f'{ride_name}, September 2024, Disneyland.csv',
        'October': f'{ride_name}, October 2024, Disneyland.csv',
        'November': f'{ride_name}, November 2024, Disneyland.csv',
        'December': f'{ride_name}, December 2024, Disneyland.csv',
    }

    all_data = []
    for month, file_name in months_data.items():
        try:
            file_path = f'C:/Users/luked/PycharmProjects/disneyland/Live_Updates/{ride_name}/{file_name}'
            month_data = pd.read_csv(file_path)
            month_data['Date/Time'] = pd.to_datetime(month_data['Date/Time'])
            month_data['Date'] = month_data['Date/Time'].dt.date  # Extract the date part
            month_data['Day'] = month_data['Date/Time'].dt.day_name()  # Add day of the week
            month_data['Hour'] = month_data['Date/Time'].dt.hour  # Add hour of the day
            all_data.append(month_data)
        except FileNotFoundError:
            print(f"File not found: {file_path}")

    return pd.concat(all_data, ignore_index=True) if all_data else None


# Load data for each ride
ride_name_big_thunder = "Big Thunder Mountain Railroad"
ride_name_space_mountain = "Space Mountain"
ride_name_matterhorn = "Matterhorn"

ride_data_big_thunder = load_ride_data(ride_name_big_thunder)
ride_data_space_mountain = load_ride_data(ride_name_space_mountain)
ride_data_matterhorn = load_ride_data(ride_name_matterhorn)


# Ensure 'Wait Time' is numeric
def preprocess_data(ride_data):
    ride_data['Wait Time'] = pd.to_numeric(ride_data['Wait Time'], errors='coerce')
    ride_data['Day'] = ride_data['Day'].astype('category')
    ride_data['Month'] = ride_data['Date/Time'].dt.month.astype('category')

    # Convert 'Day' and 'Month' to numeric codes
    ride_data['Day_Code'] = ride_data['Day'].cat.codes
    ride_data['Month_Code'] = ride_data['Month'].cat.codes
    return ride_data


ride_data_big_thunder = preprocess_data(ride_data_big_thunder)
ride_data_space_mountain = preprocess_data(ride_data_space_mountain)
ride_data_matterhorn = preprocess_data(ride_data_matterhorn)


# Prepare data for linear regression
def prepare_data_for_regression(ride_data):
    X = ride_data[['Day_Code', 'Month_Code', 'Hour']].values
    y = ride_data['Wait Time'].values
    X_ = np.c_[np.ones(X.shape[0]), X]  # Add intercept term
    return X_, y


X_big_thunder, y_big_thunder = prepare_data_for_regression(ride_data_big_thunder)
X_space_mountain, y_space_mountain = prepare_data_for_regression(ride_data_space_mountain)
X_matterhorn, y_matterhorn = prepare_data_for_regression(ride_data_matterhorn)


# Compute the coefficients (beta values) using the normal equation
def compute_beta(X_, y):
    X_transpose = X_.T
    beta = np.linalg.inv(X_transpose.dot(X_)).dot(X_transpose).dot(y)
    return beta


beta_big_thunder = compute_beta(X_big_thunder, y_big_thunder)
beta_space_mountain = compute_beta(X_space_mountain, y_space_mountain)
beta_matterhorn = compute_beta(X_matterhorn, y_matterhorn)


# Function to predict wait time for a given day, month, and hour
def predict_wait_time(day: str, month: str, hour: int, beta, ride_data):
    day_code = pd.Categorical([day], categories=ride_data['Day'].cat.categories).codes[0]
    month_code = pd.Categorical([month], categories=ride_data['Month'].cat.categories).codes[0]
    X_input = np.array([1, day_code, month_code, hour]).reshape(1, -1)  # Add intercept term
    predicted_wait_time = X_input.dot(beta)
    return predicted_wait_time[0]


# Get the current day, month, and hour
current_datetime = datetime.now()
day_input = current_datetime.strftime('%A')  # Full weekday name (e.g., Monday)
month_input = current_datetime.strftime('%B')  # Full month name (e.g., January)
hour_input = round(current_datetime.hour)  # Round to nearest hour

# Example: Predict wait time for the current day, month, and rounded hour
predicted_time_big_thunder = predict_wait_time(day_input, month_input, hour_input, beta_big_thunder,
                                               ride_data_big_thunder)
predicted_time_space_mountain = predict_wait_time(day_input, month_input, hour_input, beta_space_mountain,
                                                  ride_data_space_mountain)
predicted_time_matterhorn = predict_wait_time(day_input, month_input, hour_input, beta_matterhorn, ride_data_matterhorn)

# Loop through each ride and print wait time with category and predicted time
for ride_name in ride_names:
    current_wait_time = get_current_wait_time(ride_name)

    if current_wait_time is None:
        print(f"Wait time not available for {ride_name}.")
    else:
        # Calculate the predicted wait time
        if ride_name == ride_name_big_thunder:
            predicted_time = predicted_time_big_thunder
        elif ride_name == ride_name_space_mountain:
            predicted_time = predicted_time_space_mountain
        elif ride_name == ride_name_matterhorn:
            predicted_time = predicted_time_matterhorn

        # Compare actual and predicted wait times
        category = categorize_wait_time(int(current_wait_time), predicted_time)

        # Print the results for each ride, including predicted wait time
        print(f"{ride_name} - Actual Wait Time: {current_wait_time} minutes, Predicted Wait Time: {round(predicted_time, 2)} minutes, ({category}) time to go")
