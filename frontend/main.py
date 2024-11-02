import streamlit as st
from streamlit_chat import message
import requests
import json

# Configurations
st.set_page_config(page_title="GoodDeeds", layout="wide")

# Custom CSS for Navigation and UI Styling
st.markdown(
    """
    <style>
    /* Navigation bar as a dropdown from the top */
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
if 'location' not in st.session_state:
    st.session_state['location'] = None
if 'miles' not in st.session_state:
    st.session_state['miles'] = None

# Google SSO Login Placeholder (actual implementation should use an authentication library)
def google_login():
    st.info("Logging in with Google SSO...")
    # Replace this with real SSO login logic
    return True

def landing_page():
    col0, col1, col2 = st.columns([1, 1, 1])  # Creates two equal columns
    with col2:  # Places image in right column
        st.image("../assets/rb_74201.png", width=200)
    st.title("Welcome to GoodDeeds!")
    st.subheader("Empowering communities through volunteerism")
    st.write("Join hands with NGOs to support post-disaster recovery efforts. Whether you're an organization looking for volunteers or a user willing to contribute, this platform connects you to impactful opportunities.")
    st.button("Get Started")
    




def user_signup():
    if google_login():
        st.success("Successfully signed up!")
        if st.session_state['location'] is None:
            with st.form("location_form"):
                location = st.text_input("Enter your current location:")
                miles = st.number_input("Enter the number of miles you're willing to travel:", min_value=1)
                submit_button = st.form_submit_button("Submit")

                if submit_button and location and miles:
                    st.session_state['location'] = location
                    st.session_state['miles'] = miles
                    st.success(f"Location set to {location} and travel distance to {miles} miles.")

def display_organizations():
    # Sample data; replace with actual database call
    organizations = {
        "Helping Hands": ["Food Drive", "Clothing Donation"],
        "Community Aid": ["Medical Camp", "Shelter Setup"],
        "Relief Now": ["Rebuilding Project", "Education Drive"]
    }

    st.header("Organizations and Their Drives")
    for org, drives in organizations.items():
        with st.expander(org):
            for drive in drives:
                st.subheader(drive)
                if st.button(f"Details for {drive}", key=f"details_{org}_{drive}"):
                    display_drive_details(org, drive)

def display_drive_details(org, drive):
    st.title(f"Details for {drive}")
    st.write(f"**Organized by:** {org}")
    st.write(f"**Description:** Detailed information about the {drive} including what is needed and how users can help.")
    st.write(f"**Date & Time:** TBD")
    st.write(f"**Location:** Example Location")

    if st.button("Volunteer for this Drive", key=f"volunteer_{org}_{drive}"):
        st.success(f"You have successfully enrolled for the {drive}.")
        # Add logic to enroll the user into the database
    
    # Chatbot placeholder (using OpenAI or other chat service)
    st.header("Chat with our AI Assistant")
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    user_input = st.text_input("You: ", "", key="user_input")
    if user_input:
        st.session_state['messages'].append({"role": "user", "content": user_input})
        # Sample AI response logic (use actual API integration)
        st.session_state['messages'].append({"role": "assistant", "content": f"Response to '{user_input}'"})

    for msg in st.session_state['messages']:
        if msg['role'] == 'user':
            message(msg['content'], is_user=True)
        else:
            message(msg['content'])

def user_profile():
    st.header("User Profile")
    st.text_input("Name", "User Name", disabled=True)
    st.text_input("Email", "user@example.com", disabled=True)
    st.write(f"Your current level is level 1. Reach level 10 to start unlocking incentives!")
    st.button("Update Details")

def organization_signup():
    st.header("Organization Signup")
    st.text_input("Organization Name")
    st.text_area("Description")
    st.text_input("Contact Email")
    if st.button("Sign Up Organization"):
        st.success("Organization registered successfully.")
        # Add logic to store organization details in the database

def post_event():
    st.header("Post an Event/Drive")
    st.text_input("Event Name")
    st.text_area("Event Details")
    st.date_input("Date of Event")
    st.text_input("Event Location")
    if st.button("Post Event"):
        st.success("Event posted successfully.")
        # Add logic to save event details in the database

# Main App Logic
menu = st.sidebar.radio("Navigation", ["Landing Page", "User Signup", "Organizations & Drives", "User Profile", "Organization Signup", "Post Event"])

if menu == "Landing Page":
    landing_page()
elif menu == "User Signup":
    user_signup()
elif menu == "Organizations & Drives":
    display_organizations()
elif menu == "User Profile":
    user_profile()
elif menu == "Organization Signup":
    organization_signup()
elif menu == "Post Event":
    post_event()
