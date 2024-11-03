import streamlit as st
from streamlit_chat import message
import requests
import json

from landing_page import landing_page
from login import login
from  display_organizations import *
from event import post_event
from profile import display_profile as profile
# Configurations
st.set_page_config(page_title="GoodDeeds", layout="wide")

# Custom CSS for Navigation and UI Styling
st.markdown(
    """
    <style>
    /* Navigation bar as a dropdown from the top */

    div[data-testid="stDialog"] div[role="dialog"] {
        background-color: #333333; /* Change background color */
        color: #ffffff; /* Change text color */
        border: 2px solid #4a8c0f; /* Change border color */
        border-radius: 10px; /* Round corners */
        padding: 20px; /* Add padding */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Add shadow */
    }

    
    

    div[data-testid="stDialog"] label {
        color: #ffffff !important; /* Change label text color */
    }

    .sidebar .sidebar-content {
        animation: slide-down 0.5s ease-in-out;
    }
    @keyframes slide-down {
        from { top: -100px; opacity: 0; }
        to { top: 0; opacity: 1; }
    }
    /* Main content area styling - more specific selectors */
    .main .block-container {
        background-color: #E5C687;
    }
    div[data-testid="stAppViewContainer"] {
        background-color: #E5C687;
    }
    div[class="stApp"] {
        background-color: #E5C687;
    }
    /* Button styling */
    .stButton>button {
        background-color: #4a8c0f;
        color: black;
        border: 1px solid black !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    /* Input field styling */
    .stTextInput>div>input, .stTextArea>div>textarea {
        background-color: #FFDAB9 !important;  /* Peach color for input fields */
        color: black !important;
        border: 1px solid black !important;
    }

    
    
    /* Style for input labels/prompts */
    .stTextInput > label, .stTextArea > label, .stNumberInput > label, .stDateInput > label {
        color: black !important;
    }
    
    /* Form field outlines */
    .stTextInput > div, .stTextArea > div, .stNumberInput > div, .stDateInput > div {
        # border: 1px solid black !important;
    }

    
    
    /* Number input styling */
    .stNumberInput > div > input {
        background-color: #FFDAB9 !important;
        color: black !important;
    }
    
    /* Date input styling */
    .stDateInput > div > input {
        background-color: #FFDAB9 !important;
        color: black !important;
    }
    
    /* Expander header styling */
    .stExpander {
        color: black;
        border: 2px solid black !important;
    }

    .stPopover {
        background-color: #FFDAB9 !important;
        color: white;
        }

    .st-expanderHeader {
        background-color: #4a8c0f;
        color: black;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    /* Keep sidebar styling the same */
    .stSidebar>div {
        background-color: #272D2D;
        color: white;
    }
    /* Additional elements styling */
    .stMarkdown {
        color: black;
    }
    .streamlit-expanderHeader {
        background-color: #4a8c0f;
        color: black;
    }
    /* Header styling */
    h1, h2, h3, h4 {
        color: black;
    }
    /* Success message styling */
    .element-container .stAlert {
        background-color: #4a8c0f;
        color: black;
    }
    button[title="View fullscreen"] {
        display: none;
    }
    
    /* Form elements container */
    form {
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background-color: #FFDAB9 !important;
        color: black !important;
    }
    
    /* Select box label */
    .stSelectbox > label {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)





# User Session State
if 'api_url' not in st.session_state:
    st.session_state['api_url'] = "https://gooddeeds.onrender.com"
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
            st.session_state['current_page'] = 'post_event'

        if st.sidebar.button("Manage Events"):
            st.session_state['current_page'] = 'post_event'
            st.rerun()  # Rerun to refresh the display

        if st.sidebar.button("Profile"):
            st.session_state['current_page'] = 'profile'
            st.rerun()


        if st.session_state['current_page'] == 'post_event':
            post_event()
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
