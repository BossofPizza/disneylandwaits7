import streamlit as st
import requests
from bs4 import BeautifulSoup

# Define the URL
url = "https://www.thrill-data.com/waits/park/dlr/disneyland/"

def get_wait_time():
    """Scrapes the wait time for Space Mountain."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    ride_name_elements = soup.find_all("a", title=True)

    for ride in ride_name_elements:
        ride_name = ride.get_text(strip=True)

        if ride_name == "Space Mountain":
            parent_tr = ride.find_parent("tr")
            td_elements = parent_tr.find_all("td")

            if len(td_elements) >= 4:
                wait_time_td = td_elements[3]
                wait_time = wait_time_td.find("div")["title"] if wait_time_td.find("div") else None
            else:
                wait_time = "closed"

            return wait_time if wait_time else "closed"
    return "Ride not found"

# Streamlit UI
st.title("Space Mountain Wait Time")
st.write("This app shows the current wait time for Space Mountain at Disneyland.")

# Button to refresh wait time
if st.button("Check Wait Time"):
    wait_time = get_wait_time()
    if wait_time == "closed":
        st.error("Space Mountain is currently closed.")
    else:
        st.success(f"Current Wait Time: {wait_time}")

st.info("Refresh the page manually to check again.")
