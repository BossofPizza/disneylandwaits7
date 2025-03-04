import pandas as pd
import numpy as np
from datetime import datetime

# Load all months' CSV files into a dictionary with the correct file names
months_data = {
    'January': 'Big Thunder Mountain Railroad, January 2024, Disneyland.csv',
    'February': 'Big Thunder Mountain Railroad, February 2024, Disneyland.csv',
    'March': 'Big Thunder Mountain Railroad, March 2024, Disneyland.csv',
    'April': 'Big Thunder Mountain Railroad, April 2024, Disneyland.csv',
    'May': 'Big Thunder Mountain Railroad, May 2024, Disneyland.csv',
    'June': 'Big Thunder Mountain Railroad, June 2024, Disneyland.csv',
    'July': 'Big Thunder Mountain Railroad, July 2024, Disneyland.csv',
    'August': 'Big Thunder Mountain Railroad, August 2024, Disneyland.csv',
    'September': 'Big Thunder Mountain Railroad, September 2024, Disneyland.csv',
    'October': 'Big Thunder Mountain Railroad, October 2024, Disneyland.csv',
    'November': 'Big Thunder Mountain Railroad, November 2024, Disneyland.csv',
    'December': 'Big Thunder Mountain Railroad, December 2024, Disneyland.csv',
}

# Load all data into a single DataFrame
all_data = []
for month, file_path in months_data.items():
    month_data = pd.read_csv(file_path)
    month_data['Date/Time'] = pd.to_datetime(month_data['Date/Time'])
    month_data['Date'] = month_data['Date/Time'].dt.date  # Extract the date part
    month_data['Day'] = month_data['Date/Time'].dt.day_name()  # Add day of the week
    month_data['Hour'] = month_data['Date/Time'].dt.hour  # Add hour of the day
    all_data.append(month_data)

all_data_df = pd.concat(all_data, ignore_index=True)

# Ensure 'Wait Time' is numeric
all_data_df['Wait Time'] = pd.to_numeric(all_data_df['Wait Time'], errors='coerce')

# Convert 'Day' and 'Month' to categorical type
all_data_df['Day'] = all_data_df['Day'].astype('category')
all_data_df['Month'] = all_data_df['Date/Time'].dt.month.astype('category')

# Prepare data for manual linear regression model
X = all_data_df[['Day', 'Month', 'Hour']].values
y = all_data_df['Wait Time'].values

# Convert 'Day' and 'Month' from categorical to numeric codes
all_data_df['Day_Code'] = all_data_df['Day'].cat.codes
all_data_df['Month_Code'] = all_data_df['Month'].cat.codes

# Use 'Day_Code', 'Month_Code', and 'Hour' as features, 'Wait Time' as target
X = all_data_df[['Day_Code', 'Month_Code', 'Hour']].values
y = all_data_df['Wait Time'].values

# Add a column of ones for the intercept term in the linear regression formula
X_ = np.c_[np.ones(X.shape[0]), X]

# Compute the coefficients (beta values) using the normal equation
X_transpose = X_.T
beta = np.linalg.inv(X_transpose.dot(X_)).dot(X_transpose).dot(y)


# Function to predict wait time for a given day, month, and hour
def predict_wait_time(day: str, month: str, hour: int):
    # Convert the day and month to the corresponding numeric codes
    day_code = pd.Categorical([day], categories=all_data_df['Day'].cat.categories).codes[0]
    month_code = pd.Categorical([month], categories=all_data_df['Month'].cat.categories).codes[0]

    # Prepare the input for prediction (add intercept term)
    X_input = np.array([1, day_code, month_code, hour]).reshape(1, -1)

    # Predict the wait time using the linear regression formula
    predicted_wait_time = X_input.dot(beta)
    return predicted_wait_time[0]


# Get the current day, month, and hour
current_datetime = datetime.now()
day_input = current_datetime.strftime('%A')  # Full weekday name (e.g., Monday)
month_input = current_datetime.strftime('%B')  # Full month name (e.g., January)
hour_input = round(current_datetime.hour)  # Round to nearest hour

# Example: Predict wait time for the current day, month, and rounded hour
predicted_time = predict_wait_time(day_input, month_input, hour_input)
print(f"Predicted wait time for {day_input} in {month_input} at {hour_input}:00 is {predicted_time:.2f} minutes.")
