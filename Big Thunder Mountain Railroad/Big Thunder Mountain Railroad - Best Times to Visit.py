import pandas as pd
import matplotlib.pyplot as plt
print("No May Data Available\n")
# Load all months' CSV files into a dictionary
months_data = {
    'January': 'Big Big Thunder Mountain Railroad Railroad, January 2024, Disneyland.csv',
    'February': 'Big Big Thunder Mountain Railroad Railroad, February 2024, Disneyland.csv',
    'March': 'Big Big Thunder Mountain Railroad Railroad, March 2024, Disneyland.csv',
    'April': 'Big Big Thunder Mountain Railroad Railroad, April 2024, Disneyland.csv',
    'May': 'Big Big Thunder Mountain Railroad Railroad, May 2024, Disneyland.csv',
    'June': 'Big Big Thunder Mountain Railroad Railroad, June 2024, Disneyland.csv',
    'July': 'Big Big Thunder Mountain Railroad Railroad, July 2024, Disneyland.csv',
    'August': 'Big Big Thunder Mountain Railroad Railroad, August 2024, Disneyland.csv',
    'September': 'Big Big Thunder Mountain Railroad Railroad, September 2024, Disneyland.csv',
    'October': 'Big Big Thunder Mountain Railroad Railroad, October 2024, Disneyland.csv',
    'November': 'Big Big Thunder Mountain Railroad Railroad, November 2024, Disneyland.csv',
    'December': 'Big Big Thunder Mountain Railroad Railroad, December 2024, Disneyland.csv',
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

# Filter out hours with insufficient data (less than 5 hours of non-zero wait times)
hourly_valid_data = all_data_df[all_data_df['Wait Time'] > 0].groupby(['Date', 'Hour'])['Wait Time'].count()
valid_hours = hourly_valid_data[hourly_valid_data >= 5].reset_index()
valid_hours['Valid'] = True

# Merge back to filter original DataFrame
all_data_df = all_data_df.merge(valid_hours[['Date', 'Hour', 'Valid']], how='left', on=['Date', 'Hour'])
all_data_df = all_data_df[all_data_df['Valid'] == True]

# Aggregate data by day of the week and hour to calculate average wait time
best_times = all_data_df.groupby(['Day', 'Hour'])['Wait Time'].mean().reset_index()

# Find the best times to visit (shortest average wait times)
shortest_wait_times = best_times.nsmallest(10, 'Wait Time')

# Plotting Best Times to Visit
plt.figure(figsize=(12, 6))
for day in best_times['Day'].unique():
    daily_data = best_times[best_times['Day'] == day]
    plt.plot(daily_data['Hour'], daily_data['Wait Time'], label=day)

plt.title('Average Wait Time by Hour and Day of the Week', fontsize=14)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Average Wait Time (minutes)', fontsize=12)
plt.xticks(range(0, 24), labels=[f'{hour}:00' for hour in range(0, 24)], rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title='Day of the Week', fontsize=10)
plt.tight_layout()
plt.show()

# Print the results
print("Top 10 Best Times to Visit (Shortest Average Wait Times):")
print(shortest_wait_times)