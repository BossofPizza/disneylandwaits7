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

# Load the data for all months into a single DataFrame
all_data = []
for month, file_path in months_data.items():
    month_data = pd.read_csv(file_path)
    month_data['Date/Time'] = pd.to_datetime(month_data['Date/Time'])  # Ensure datetime format
    month_data['Month'] = month_data['Date/Time'].dt.month
    all_data.append(month_data)

all_data_df = pd.concat(all_data, ignore_index=True)

# Assign seasons based on month
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter (Dec, Jan, Feb)'
    elif month in [3, 4, 5]:
        return 'Spring (Mar, Apr, May)'
    elif month in [6, 7, 8]:
        return 'Summer (Jun, Jul, Aug)'
    elif month in [9, 10, 11]:
        return 'Fall (Sep, Oct, Nov)'

all_data_df['Season'] = all_data_df['Month'].apply(get_season)

# Calculate average wait times for each season
seasonal_averages = all_data_df.groupby('Season')['Wait Time'].mean().sort_values()

# Plot the results
plt.figure(figsize=(10, 6))
seasonal_averages.plot(kind='bar', color=['blue', 'green', 'orange', 'red'], edgecolor='black')
plt.title("Average Wait Times by Season", fontsize=14)
plt.ylabel("Average Wait Time (minutes)", fontsize=12)
plt.xlabel("Season", fontsize=12)
plt.xticks(rotation=0, fontsize=10)
plt.tight_layout()
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Print the results
print("Average Wait Times by Season:")
print(seasonal_averages)
