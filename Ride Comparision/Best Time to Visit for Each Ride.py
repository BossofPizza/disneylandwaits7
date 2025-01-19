import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the rides and months for the data
rides = ['Matterhorn', 'Space Mountain', 'Big Thunder Mountain Railroad']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']

# Base directory path where the CSV files are stored
base_path = r'C:\Users\luked\PycharmProjects\disneyland'


# Function to load ride data for all months
def load_ride_data(ride_name):
    all_data = []
    for month in months:
        file_path = f'{base_path}\\{ride_name}\\{ride_name}, {month} 2024, Disneyland.csv'
        try:
            month_data = pd.read_csv(file_path)
            month_data['Date/Time'] = pd.to_datetime(month_data['Date/Time'])
            month_data['Day'] = month_data['Date/Time'].dt.day_name()  # Add day of the week
            month_data['Hour'] = month_data['Date/Time'].dt.hour  # Add hour of the day
            all_data.append(month_data)
            print(f"Loaded data for {ride_name} in {month}")
        except FileNotFoundError:
            print(f"File not found for {ride_name} in {month}")
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()


# Load data for each ride
rides_data = {}
for ride in rides:
    rides_data[ride] = load_ride_data(ride)

# Ensure 'Wait Time' is numeric for all rides
for ride, data in rides_data.items():
    if not data.empty:
        data['Wait Time'] = pd.to_numeric(data['Wait Time'], errors='coerce')

# Find the best times to visit (i.e., lowest wait times for each ride)
best_times = {}
for ride, data in rides_data.items():
    if not data.empty:
        best_time = data.groupby('Hour')['Wait Time'].min()
        best_times[ride] = best_time.idxmin()

# Print best times for each ride
for ride, best_time in best_times.items():
    print(f"The best time to visit {ride} is at {best_time}:00 for the shortest wait time.")


# Function to plot wait time by hour for each ride on the same graph
def plot_wait_times(rides_data):
    plt.figure(figsize=(10, 6))
    for ride, data in rides_data.items():
        if not data.empty:
            # Group by hour and calculate average wait time for the ride
            avg_wait_time = data.groupby('Hour')['Wait Time'].mean()
            sns.lineplot(x=avg_wait_time.index, y=avg_wait_time.values, marker='o', label=ride)

    # Adding plot details
    plt.title('Average Wait Time by Hour for Each Ride')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Average Wait Time (minutes)')
    plt.xticks(range(24))  # Ensure all 24 hours are shown on x-axis
    plt.grid(True)
    plt.legend(title='Ride')
    plt.show()


# Call the function to plot for all rides
plot_wait_times(rides_data)
