import streamlit as st
from streamlit_chat import message
import requests
import json

from landing_page import landing_page

from  display_organizations import display_organizations
from event import post_event
from userList import rank_users
from profile import display_profile as profile
from volunteer_dashboard import volunteer_dashboard
# Configurations
st.set_page_config(page_title="GoodDeeds", layout="wide")

# User Session State
if 'api_url' not in st.session_state:
    st.session_state['api_url'] = "https://gooddeeds.onrender.com"
    # st.session_state['api_url'] = "http://127.0.0.1:8080"

if 'location' not in st.session_state:
    st.session_state['location'] = None

if 'miles' not in st.session_state:
    st.session_state['miles'] = None

# Hide the Navbar at first
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_type'] = None
    st.session_state['user_id'] = None

# Landing Page
if not st.session_state['logged_in']:
    landing_page()
        

# User is logged in
if st.session_state['logged_in']:
    # Check user type and render respective pages
    user_type = st.session_state['user_type']
    
    # Make Navbar visible (simulated here with buttons for navigation)
    st.sidebar.title("Navigation")
    if user_type == 'volunteer':
        if 'current_page' not in st.session_state or not st.session_state['current_page']:
            st.session_state['current_page'] = 'display_organizations'

        if st.sidebar.button("Volunteer Dashboard"):
            st.session_state['current_page'] = 'volunteer_dashboard'
            st.rerun()

        if st.sidebar.button("Volunteer Events"):
            st.session_state['current_page'] = 'display_organizations'
            st.rerun()

        if st.sidebar.button("Profile"):
            st.session_state['current_page'] = 'profile'
            st.rerun()

        if st.session_state['current_page'] == 'display_organizations':
            display_organizations()
        elif st.session_state['current_page'] == 'profile':
            profile()
        # elif st.session_state['current_page'] == 'volunteer_dashboard':
        
        
    elif user_type == 'organization':
        if 'current_page' not in st.session_state or not st.session_state['current_page']:
            st.session_state['current_page'] = 'rank_users'

        if st.sidebar.button("Rank Users"):
            st.session_state['current_page'] = 'rank_users'
            st.rerun()

        if st.sidebar.button("Posts Events"):
            st.session_state['current_page'] = 'post_event'
            st.rerun()  # Rerun to refresh the display

        if st.sidebar.button("Profile"):
            st.session_state['current_page'] = 'profile'
            st.rerun()


        if st.session_state['current_page'] == 'post_event':
            post_event()
        if st.session_state['current_page'] == 'rank_users':
            rank_users()
        elif st.session_state['current_page'] == 'profile':
            profile()
        
        
    
    # Add logout button
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user_type'] = None
        st.session_state['user_id'] = None
        st.session_state['current_page'] = None
        st.rerun()

# Main App Logic
