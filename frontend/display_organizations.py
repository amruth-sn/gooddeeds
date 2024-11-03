import streamlit as st
import streamlit_chat as message
import requests
API_URL = "http://127.0.0.1:5000"


def display_organizations():
    # Sample data; replace with actual database call

    

    # organizations = {
    #     "Helping Hands": ["Food Drive", "Clothing Donation"],
    #     "Community Aid": ["Medical Camp", "Shelter Setup"],
    #     "Relief Now": ["Rebuilding Project", "Education Drive"]
    # }

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

    response = requests.get(f"{API_URL}/get-all-events/{id}")

    if response.status_code == 200:

        for event in response.json():
            eventname = event['name']
            description = event['description']
            date = event['date']
            latitude = event['latitude']
            longitude = event['longitude']
            st.title(f"Details for {eventname}")
            st.write(f"**Organized by:** {name}")
            st.write(f"**Description:** Detailed information about the {description} including what is needed and how users can help.")
            st.write(f"**Date & Time:** {date}")
            st.write(f"**Location:** {(latitude, longitude)}")

            # if st.button("Volunteer for this Drive", key=f"volunteer_{org}_{drive}"):
                # st.success(f"You have successfully enrolled for the {drive}.")
    else:
        st.write("Unable to fetch events at this time. Please try again later.")

    
    
    

    # for msg in st.session_state['messages']:
    #     if msg['role'] == 'user':
    #         message(msg['content'], is_user=True)
    #     else:
    #         message(msg['content'])