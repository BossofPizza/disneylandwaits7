from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

# URL for Disneyland wait times
url = "https://www.thrill-data.com/waits/park/dlr/disneyland/"
ride_names = ["Big Thunder Mountain Railroad", "Matterhorn Bobsleds", "Space Mountain"]

# Function to get the current wait time for a ride
def get_current_wait_time(soup, ride_name):
    try:
        ride_name_elements = soup.find_all("a", title=True)
        for ride in ride_name_elements:
            if ride_name in ride.get_text(strip=True):
                parent_tr = ride.find_parent("tr")
                if parent_tr:
                    wait_time_td = parent_tr.find_all("td")[3]
                    wait_time = wait_time_td.find("div")["title"] if wait_time_td.find("div") else None
                    if wait_time:
                        return int(wait_time.split(" ")[0])  # Return the actual wait time as an integer
    except Exception as e:
        print(f"Error fetching wait time for {ride_name}: {e}")
    return None

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

# Example regression data for prediction
ride_data = {
    "Big Thunder Mountain Railroad": [0.5, 1.0, 2.0, 3.0],
    "Matterhorn Bobsleds": [1.0, 1.5, 2.5, 3.5],
    "Space Mountain": [2.0, 2.5, 3.0, 4.0]
}

# Function to simulate a prediction
def predict_wait_time(day, month, hour, ride_name):
    # Simulate a prediction using basic regression coefficients
    beta = ride_data.get(ride_name, [0, 0, 0, 0])
    prediction = beta[0] + beta[1] * day + beta[2] * month + beta[3] * hour
    return prediction

@app.route('/')
def home():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        soup = BeautifulSoup(response.text, "html.parser")

        current_datetime = datetime.now()
        day_input = current_datetime.weekday()  # Day as an integer (Monday=0)
        month_input = current_datetime.month  # Numeric month
        hour_input = current_datetime.hour  # Hour of the day

        ride_data_list = []
        for ride_name in ride_names:
            current_wait_time = get_current_wait_time(soup, ride_name)
            if current_wait_time is None:
                ride_data_list.append({
                    "ride_name": ride_name,
                    "current_wait": "N/A",
                    "prediction": "N/A",
                    "category": "Data not available"
                })
            else:
                predicted_time = predict_wait_time(day_input, month_input, hour_input, ride_name)
                category = categorize_wait_time(current_wait_time, predicted_time)
                ride_data_list.append({
                    "ride_name": ride_name,
                    "current_wait": f"{current_wait_time} minutes",
                    "prediction": f"{predicted_time:.2f} minutes",
                    "category": category
                })

        return render_template('home.html', rides=ride_data_list)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('home.html', rides=[])

if __name__ == "__main__":
    app.run(debug=True)
