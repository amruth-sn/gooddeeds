import streamlit as st
import requests
from geopy.geocoders import Nominatim
from datetime import datetime

def display_organizations():
    API_URL = st.session_state['api_url']
    userresponse = requests.get(f"{API_URL}/users/{st.session_state['user_id']}")
    if userresponse.status_code == 200:
        user = userresponse.json()
        st.write(f"Welcome, {user['name']}!")
        user_lat = user['latitude']
        user_long = user['longitude']
        user_distance = user['distance']
    else:
        st.write("Unable to fetch user details at this time. Please try again later.")

    # Fetch all organizations
    location_response = requests.get(
            f"{API_URL}/events/location",
            params={
                'lat': user_lat,
                'lon': user_long,
                'distance': user_distance
            }
        )
    if location_response.status_code == 200:
        events_within_distance = location_response.json().get('events', [])
        organization_ids_within_distance = {event['organization_id'] for event in events_within_distance}
        event_ids_within_distance = {event['id'] for event in events_within_distance}
        organizations = []
        ret = {}
        for orgid in organization_ids_within_distance:
            orgresponse = requests.get(f"{API_URL}/organizations/{orgid}")
            
            if orgresponse.status_code == 200:
                organizations.append(orgresponse.json())
                ret[orgid] = [event['id'] for event in events_within_distance if event['organization_id'] == orgid]
            else:
                st.write("Unable to fetch organizations at this time. Please try again later.")
        st.header("Nearby Organizations and Their Drives")

        # Filter options for date and time
        st.sidebar.header("Filter Events")
        start_date = st.sidebar.date_input("Start Date", datetime.now().date())
        start_time = st.sidebar.time_input("Start Time", datetime.now().time())
        end_date = st.sidebar.date_input("End Date", datetime.now().date())
        end_time = st.sidebar.time_input("End Time", datetime.now().time())

        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)

        for org in organizations:
            name = org['name']
            id = org['id']
            email = org['email']
            description = org['description']
            with st.expander(f'**{name}**  		{email}'):
                st.write(f"**Description:** {description}")

                # Fetch events for the organization
                event_response = ret[id]
                
                def latlong_to_zipcode(lat, long):
                    geolocator = Nominatim(user_agent="gooddeeds")
                    location = geolocator.reverse(f'{lat}, {long}', exactly_one=True)
                    return location.address if location else "Location not found"
                es = []
                filtered_events = []
                for event in event_response:
                    r = requests.get(f"{API_URL}/events/{event}")
                    if r.status_code == 200:
                        es.append(r.json())
                    else:
                        st.write("Unable to fetch events at this time. Please try again later.")
                for event in es:
                    event_datetime = datetime.fromisoformat(event['time'])

                    # Filter by the date and time range
                    if start_datetime <= event_datetime <= end_datetime:
                        filtered_events.append(event)

                if filtered_events:
                    for event in filtered_events:
                        eventname = event['name']
                        description = event['description']
                        date = event['time']
                        id = event['id']
                        latitude = event['latitude']
                        longitude = event['longitude']
                        severity = event['severity']

                        st.title(f"Details for {eventname}")
                        st.write(f"**Organized by:** {name}")
                        st.write(f"**Description:** {description}")
                        st.write(f"**Date & Time:** {date}")

                        location = latlong_to_zipcode(latitude, longitude)
                        st.write(f"**Location:** {location}")
                        st.write(f"**Severity:** {severity*'★'}")

                        if st.button("Volunteer for this event", key=id):
                            volresponse = requests.post(f"{API_URL}/event-registrations", json={"event_id": id, "user_id": st.session_state['user_id']})
                            if volresponse.status_code == 201:
                                st.write("You have successfully volunteered for this event!")
                            else:
                                st.write("Unable to volunteer for this event at this time. Please try again later.")
                else:
                    st.write("No events found for the selected date and time range.")
                
    else:
        st.write("Unable to fetch organizations at this time. Please try again later.")
