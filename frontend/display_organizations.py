import streamlit as st
import streamlit_chat as message
import requests


def display_organizations():
    API_URL = st.session_state['api_url']
    response = requests.get(f"{API_URL}/get-all-orgs")
    if response.status_code == 200:
        organizations = response.json()
        st.header("Organizations and Their Drives")
        for org in organizations:
            name = org['name']
            id = org['id']
            email = org['email']
            description = org['description']
            with st.expander(f'**{name}**  \t\t{email}'):
                st.write(f"**Description:** {description}")
                display_drive_details(name, id)

    else:
        st.write("Unable to fetch organizations at this time. Please try again later.")

    

def display_drive_details(name, id):
    API_URL = st.session_state['api_url']

    response = requests.get(f"{API_URL}/get-all-events/{id}")

    if response.status_code == 200:

        for event in response.json():
            eventname = event['name']
            description = event['description']
            date = event['date']
            id = event['id']
            latitude = event['latitude']
            longitude = event['longitude']
            st.title(f"Details for {eventname}")
            st.write(f"**Organized by:** {name}")
            st.write(f"**Description:** Detailed information about the {description} including what is needed and how users can help.")
            st.write(f"**Date & Time:** {date}")
            st.write(f"**Location:** {(latitude, longitude)}")

            if st.button("Volunteer for this event", key=id):
                response = requests.post(f"{API_URL}/event-registrations", json={"event_id": id, "user_id": st.session_state['user_id']})
                if response.status_code == 201:
                    st.write("You have successfully volunteered for this event!")
                else:
                    st.write("Unable to volunteer for this event at this time. Please try again later.")
    else:
        st.write("Unable to fetch events at this time. Please try again later.")

