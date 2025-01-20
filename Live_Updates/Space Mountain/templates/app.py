from flask import Flask, render_template_string
import disneyland_wait_times1  # Replace this with your script filename (without .py)

app = Flask(__name__)

@app.route('/')
def home():
    # Capture the output of your script
    output = []

    for ride_name in disneyland_wait_times.ride_names:
        current_wait_time = disneyland_wait_times.get_current_wait_time(ride_name)

        if current_wait_time is None:
            output.append(f"Wait time not available for {ride_name}.")
        else:
            if ride_name == disneyland_wait_times.ride_name_big_thunder:
                predicted_time = disneyland_wait_times.predicted_time_big_thunder
            elif ride_name == disneyland_wait_times.ride_name_space_mountain:
                predicted_time = disneyland_wait_times.predicted_time_space_mountain
            elif ride_name == disneyland_wait_times.ride_name_matterhorn:
                predicted_time = disneyland_wait_times.predicted_time_matterhorn

            category = disneyland_wait_times.categorize_wait_time(
                int(current_wait_time), predicted_time)
            output.append(
                f"{ride_name} - Wait Time {current_wait_time} minutes, ({category}) time to go")

    # Return the output as HTML
    html_output = "<br>".join(output)
    return render_template_string(f"<html><body>{html_output}</body></html>")

if __name__ == '__main__':
    app.run(debug=True)
