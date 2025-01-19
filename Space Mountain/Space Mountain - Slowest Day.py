import pandas as pd


# Load all months' CSV files into a dictionary
months_data = {
    'January': 'Space Mountain, January 2024, Disneyland.csv',
    'February': 'Space Mountain, February 2024, Disneyland.csv',
    'March': 'Space Mountain, March 2024, Disneyland.csv',
    'April': 'Space Mountain, April 2024, Disneyland.csv',
    'June': 'Space Mountain, June 2024, Disneyland.csv',
    'July': 'Space Mountain, July 2024, Disneyland.csv',
    'August': 'Space Mountain, August 2024, Disneyland.csv',
    'September': 'Space Mountain, September 2024, Disneyland.csv',
    'October': 'Space Mountain, October 2024, Disneyland.csv',
    'November': 'Space Mountain, November 2024, Disneyland.csv',
    'December': 'Space Mountain, December 2024, Disneyland.csv',
}

# Load all months' data into a single DataFrame
all_data = []
for month, file_path in months_data.items():
    month_data = pd.read_csv(file_path)
    month_data['Date/Time'] = pd.to_datetime(month_data['Date/Time'])  # Ensure datetime format
    month_data['Day'] = month_data['Date/Time'].dt.day_name()  # Add day of the week (e.g., Monday)
    month_data['Date'] = month_data['Date/Time'].dt.date  # Extract the date part
    all_data.append(month_data)

# Concatenate all the data into one DataFrame
all_data_df = pd.concat(all_data, ignore_index=True)

# Filter out days with 0 wait time and calculate how many hours of data are available for each date
all_data_df = all_data_df[all_data_df['Wait Time'] > 0]

# Group by date and calculate the number of hours of data for each date
all_data_df['Hour'] = all_data_df['Date/Time'].dt.hour
hourly_data_count = all_data_df.groupby('Date')['Hour'].nunique()

# Filter dates that have at least 5 hours of data
valid_dates = hourly_data_count[hourly_data_count >= 5].index
filtered_data = all_data_df[all_data_df['Date'].isin(valid_dates)]

# Now, group the data by day of the week and calculate the average wait time
average_wait_times_by_day = filtered_data.groupby('Day')['Wait Time'].mean()

# Reorder the days to have them in a proper order (Monday to Sunday)
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
average_wait_times_by_day = average_wait_times_by_day[day_order]

# Print the days ordered from slowest to busiest (lowest to highest average wait time)
print("Average wait times by day (slowest to busiest):")
sorted_days = average_wait_times_by_day.sort_values(ascending=True)  # Sort in ascending order for slowest to busiest
for day, wait_time in sorted_days.items():
    print(f"{day}: {wait_time:.2f} minutes")

# Find the single date in the entire year with the lowest average wait time (slowest day)
# Group by the full date to get daily averages
daily_avg_wait_time = filtered_data.groupby('Date')['Wait Time'].mean()

# Find the date with the lowest average wait time (slowest day)
slowest_date = daily_avg_wait_time.idxmin()
slowest_day_wait_time = daily_avg_wait_time.min()

# Find the date with the highest average wait time (busiest day)
busiest_date = daily_avg_wait_time.idxmax()
busiest_day_wait_time = daily_avg_wait_time.max()

# Print the results
print(f"\nThe single date with the lowest average wait time (slowest day) is {slowest_date} with an average wait time of {slowest_day_wait_time:.2f} minutes.")
print(f"The single date with the highest average wait time (busiest day) is {busiest_date} with an average wait time of {busiest_day_wait_time:.2f} minutes.")
