import pandas as pd

# Define the rides and months for the data
rides = ['Space Mountain']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Base directory path where the CSV files are stored
base_path = r'C:\Users\luked\PycharmProjects\disneyland'

# Define file paths for the rides for all months
ride_data = {
    'Space Mountain': 'Space Mountain, {} 2024, Disneyland.csv'
}

# Load data for all months
rides_df = {}

for ride, file_pattern in ride_data.items():
    all_month_data = []
    for month in months:
        file_path = f"{base_path}\\{ride}\\{file_pattern.format(month)}"
        try:
            df = pd.read_csv(file_path)
            row_count = len(df)  # Count the number of rows
            print(f"Loaded {row_count} rows for {ride} in {month}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
