import streamlit as st
from landing_page import landing_page
from display_organizations import display_organizations
from event import post_event
from userList import rank_users
from profile import display_profile as profile

st.set_page_config(page_title="GoodDeeds", layout="wide", page_icon='❤️')

# Custom CSS for styling
st.markdown("""
    <style>
            /* Page Background Styling */
    .stApp {
        background-image: url('/mount/src/gooddeeds/frontend/assets/arches-1920x1080.png');
        # background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Sidebar styles */
    .css-1d391kg {
        padding-top: 3.5rem;
    }
    
    /* Sidebar title styling */
    .css-1v0mbdj.e115fcil1 {
        text-align: center;
        margin-bottom: 2rem;
    }
            
    
    /* Button container styling */
    div[data-testid="stSidebarNav"] {
        text-align: center;
    }
    
    /* Navigation button styling */
    .stButton > button {
        width: 90%;
        background: transparent;
        padding: 0.75rem 1rem;
        margin: 0.5rem auto;
        color: #263238;
        font-size: 1rem;
        transition: all 0.3s ease;
        border-radius: 0;
        text-align: center;
        position: relative;  /* Added for pseudo-element positioning */
        border: 1px solid #2E7D32;  /* Default border */
        box-sizing: border-box;  /* Ensures borders are included in element size */
    }
    
    /* Button hover effect */
    .stButton > button:hover {
        background-color: rgba(46, 125, 50, 0.1);
        color: #2E7D32;
        border: 1px solid #2E7D32;  /* Maintain border on hover */
        transform: translateY(5px);
    }
    button[title="View fullscreen"] {
        display: none;
    }
    /* Active button state */
    .stButton > button:active {
        background-color: rgba(46, 125, 50, 0.2);
        border: 1px solid #2E7D32;  /* Maintain border on active state */
    }
    
    
    /* Logout button specific styling */
    .stButton:last-child > button {
        margin-top: 2rem;
        border: 1px solid #D32F2F;  /* Red border for logout */
        color: #D32F2F;
    }
    
    .stButton:last-child > button:hover {
        background-color: rgba(211, 47, 47, 0.1);
        color: #D32F2F;
        border: 1px solid #D32F2F;  /* Maintain red border on hover */
    }
            
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(241, 241, 241, 1);
        color: #555;
        text-align: center;
        padding: 10px;
        font-size: 0.8rem;
    }
            
    [data-testid='stHeaderActionElements'] {display: none;}
    </style>
    <div class="footer">
        Made with ❤️ for BostonHacks 2024.
    </div>
""", unsafe_allow_html=True)

# Configurations

# User Session State
if 'api_url' not in st.session_state:
    st.session_state['api_url'] = "https://gooddeeds-z0x9.onrender.com"
    

if 'location' not in st.session_state:
    st.session_state['location'] = None
if 'miles' not in st.session_state:
    st.session_state['miles'] = None
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_type'] = None
    st.session_state['user_id'] = None

# Landing Page
if not st.session_state['logged_in']:
    landing_page()

# User is logged in
if st.session_state['logged_in']:
    user_type = st.session_state['user_type']
    
    st.sidebar.title("Navigation")
    
    if user_type == 'volunteer':
        if 'current_page' not in st.session_state or not st.session_state['current_page']:
            st.session_state['current_page'] = 'display_organizations'
        if st.sidebar.button("Volunteer Dashboard"):
            st.session_state['current_page'] = 'display_organizations'
            st.rerun()
        if st.sidebar.button("Profile"):
            st.session_state['current_page'] = 'profile'
            st.rerun()
        if st.sidebar.button("Leaderboard"):
            st.session_state['current_page'] = 'rank_users'
            st.rerun()
        if st.session_state['current_page'] == 'display_organizations':
            display_organizations()
        elif st.session_state['current_page'] == 'profile':
            profile()
        elif st.session_state['current_page'] == 'rank_users':
            rank_users()
    
    elif user_type == 'organization':
        if 'current_page' not in st.session_state or not st.session_state['current_page']:
            st.session_state['current_page'] = 'rank_users'
        if st.sidebar.button("Leaderboard"):
            st.session_state['current_page'] = 'rank_users'
            st.rerun()
        if st.sidebar.button("Post Events"):
            st.session_state['current_page'] = 'post_event'
            st.rerun()
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