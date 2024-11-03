import streamlit as st
from datetime import datetime
import requests
from geopy.geocoders import Nominatim

def post_event():
    API_URL = st.session_state['api_url']
    st.header("Post an Event/Drive")
    
    event_name = st.text_input("Event Name")
    event_description = st.text_area("Event Description")
    event_date = st.date_input("Date of Event")
    event_time = st.time_input("Time of Event")
    event_zipcode = st.text_input("Event Zipcode")
    severity = st.slider("Severity", 1, 5, 3)
    volunteer_count = st.number_input("Number of Volunteers Needed", min_value=1, value=1)
    
    if st.button("Post Event"):
        # Combine date and time
        event_datetime = datetime.combine(event_date, event_time)
    
        # Get latitude and longitude from zipcode
        geolocator = Nominatim(user_agent="gooddeeds")
        location = geolocator.geocode(f"{event_zipcode}, USA")
        
        if location:
            latitude = location.latitude
            longitude = location.longitude
            
            # Prepare data for API request
            event_data = {
                "name": event_name,
                "organization_id": st.session_state['user_id'],  # Assuming you store the org ID in session state
                "latitude": latitude,
                "longitude": longitude,
                "description": event_description,
                "time": event_datetime.isoformat(),
                "volunteer_count": volunteer_count,
                "severity": severity
            }
            
            # Make API request to create event
            response = requests.post(f"{API_URL}/events", json=event_data)
            
            if response.status_code == 201:
                st.success("Event posted successfully.")
            else:
                st.error(f"Failed to post event. Error: {response.json().get('message', 'Unknown error')}")
        else:
            st.error("Invalid zipcode. Could not determine location.")
