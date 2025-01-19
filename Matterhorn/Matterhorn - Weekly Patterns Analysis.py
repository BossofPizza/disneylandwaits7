import pandas as pd
import matplotlib.pyplot as plt

# Load all months' CSV files into a dictionary
months_data = {
    'January': 'Matterhorn, January 2024, Disneyland.csv',
    'February': 'Matterhorn, February 2024, Disneyland.csv',
    'March': 'Matterhorn, March 2024, Disneyland.csv',
    'April': 'Matterhorn, April 2024, Disneyland.csv',
    'May': 'Matterhorn, May 2024, Disneyland.csv',
    'June': 'Matterhorn, June 2024, Disneyland.csv',
    'July': 'Matterhorn, July 2024, Disneyland.csv',
    'August': 'Matterhorn, August 2024, Disneyland.csv',
    'September': 'Matterhorn, September 2024, Disneyland.csv',
    'October': 'Matterhorn, October 2024, Disneyland.csv',
    'November': 'Matterhorn, November 2024, Disneyland.csv',
    'December': 'Matterhorn, December 2024, Disneyland.csv',
}

# Load the data for all months into a single DataFrame
all_data = []
for month, file_path in months_data.items():
    month_data = pd.read_csv(file_path)
    month_data['Date/Time'] = pd.to_datetime(month_data['Date/Time'])  # Ensure datetime format
    month_data['Day'] = month_data['Date/Time'].dt.day_name()  # Add day of the week
    all_data.append(month_data)

all_data_df = pd.concat(all_data, ignore_index=True)

# Calculate average wait times for each day of the week
weekly_averages = all_data_df.groupby('Day')['Wait Time'].mean()

# Ensure days of the week are in order
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekly_averages = weekly_averages.reindex(days_order)

# Plot the results
plt.figure(figsize=(10, 6))
weekly_averages.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Average Wait Times by Day of the Week", fontsize=14)
plt.ylabel("Average Wait Time (minutes)", fontsize=12)
plt.xlabel("Day of the Week", fontsize=12)
plt.xticks(rotation=0, fontsize=10)
plt.tight_layout()
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Print the results
print("Average Wait Times by Day of the Week:")
print(weekly_averages)
