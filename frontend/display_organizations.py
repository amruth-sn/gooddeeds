import streamlit as st
import requests
from geopy.geocoders import Nominatim
from datetime import datetime

def init_chat_state(event_id):
    """Initialize chat state for a specific event"""
    if f'messages_{event_id}' not in st.session_state:
        st.session_state[f'messages_{event_id}'] = []
        # Add initial system message about the event
        st.session_state[f'messages_{event_id}'].append({
            "role": "system",
            "content": "I am an AI assistant here to help answer questions about this event."
        })

def display_chat(event_id, event_name, api_url):
    """Display chat interface for a specific event"""
    init_chat_state(event_id)
    
    # Create a container for the chat interface
    chat_container = st.container()
    
    with chat_container:
        st.subheader(f"Chat about: {event_name}")
        
        # Display chat messages (skip system message)
        for message in st.session_state[f'messages_{event_id}'][1:]:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input with unique key
        if prompt := st.chat_input(
            "Ask about this event...",
            key=f"chat_input_{event_id}"  # Add unique key for each event's chat input
        ):
            # Add user message to chat history
            st.session_state[f'messages_{event_id}'].append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.write(prompt)
            
            # Get AI response
            try:
                with st.spinner("Thinking..."):
                    response = requests.post(
                        f"{api_url}/chatbot/{event_id}",
                        json={
                            "message": prompt
                        }
                    )
                    
                    if response.status_code == 200:
                        ai_response = response.json()['response']
                        # Add AI response to chat history
                        st.session_state[f'messages_{event_id}'].append(
                            {"role": "assistant", "content": ai_response}
                        )
                        # Display AI response
                        with st.chat_message("assistant"):
                            st.write(ai_response)
                    else:
                        st.error("Failed to get response from the chatbot.")
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")


def display_organizations():
    API_URL = st.session_state['api_url']
    # print(st.session_state['user_id'])
    userresponse = requests.get(f"{API_URL}/users/{st.session_state['user_id']}")
    # print(userresponse)
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
        events_within_distance = location_response.json().get('events')
        # print(events_within_distance)
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


                        date = datetime.fromisoformat(date).strftime('%B %d, %Y, %I:%M%p')
                        day = event_datetime.day
                        if 4 <= day <= 20 or 24 <= day <= 30:
                            suffix = "th"
                        else:
                            suffix = ["st", "nd", "rd"][day % 10 - 1]

                        formatdate = event_datetime.strftime(f'%B {day}{suffix}, %Y, %I:%M%p')
                        st.title(f"Details for {eventname}")
                        st.write(f"**Organized by:** {name}")
                        st.write(f"**Description:** {description}")
                        st.write(f"**Date & Time:** {formatdate}")

                        location = latlong_to_zipcode(latitude, longitude)
                        st.write(f"**Location:** {location}")
                        st.write(f"**Severity:** {severity*'★'}")

                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            if st.button("Volunteer for this event", key=id):
                                volresponse = requests.post(f"{API_URL}/event-registrations", json={"event_id": id, "user_id": st.session_state['user_id']})
                                if volresponse.status_code == 201:
                                    st.write("You have successfully volunteered for this event!")
                                else:
                                    st.write("Unable to volunteer for this event at this time. Please try again later.")

                        with col2:
                            chat_button_key = f"chat_button_{id}"  # Added unique key for chat button
                            if st.button("Chat about event", key=chat_button_key):
                                st.session_state[f'show_chat_{id}'] = True
        
                        # Display chat interface if button was clicked
                        if st.session_state.get(f'show_chat_{id}', False):
                            display_chat(id, eventname, API_URL)
                            close_button_key = f"close_chat_{id}"  # Added unique key for close button
                            if st.button("Close Chat", key=close_button_key):
                                st.session_state[f'show_chat_{id}'] = False
                                st.rerun()

                        # with col2:
                        #     chat_button_key = f"chat_button_{id}"  # Added unique key for chat button
                        #     if st.button("Chat about event", key=chat_button_key):
                        #         st.session_state[f'show_chat_{id}'] = True
        
                        # # Display chat interface if button was clicked
                        # if st.session_state.get(f'show_chat_{id}', False):
                        #     display_chat(id, eventname, API_URL)
                        #     close_button_key = f"close_chat_{id}"  # Added unique key for close button
                        #     if st.button("Close Chat", key=close_button_key):
                        #         st.session_state[f'show_chat_{id}'] = False
                        #         st.rerun()


                else:
                    st.write("No events found for the selected date and time range.")
                
    else:
        st.write("Unable to fetch organizations at this time. Please try again later.")
