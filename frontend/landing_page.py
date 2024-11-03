import streamlit as st
import requests
from display_organizations import *
from event import post_event
from login import login
API_URL = "http://127.0.0.1:5000"

def landing_page():
    col0, col1, col2 = st.columns([1, 1, 1])  # Creates two equal columns
    with col2:  # Places image in right column
        st.image("../assets/rb_74201.png", width=200)
    
    st.title("Welcome to GoodDeeds!")
    st.subheader("Empowering communities through volunteerism")
    st.write("Join hands with NGOs to support post-disaster recovery efforts. Whether you're an organization looking for volunteers or a user willing to contribute, this platform connects you to impactful opportunities.")



    login_col, get_started_col = st.columns([1, 1])
    
    with login_col:
        @st.dialog("Login")
        def login_modal():
                email = st.text_input("Enter your email:")
                password = st.text_input("Enter your password:", type="password")
                if st.button("Submit"):
                    if email and password:
                        st.session_state['logged_in'] = True
                        st.write("Login successful!")
                        st.session_state['user_type'] = 'organization'
                        st.rerun()
                    else:
                        st.write("Login failed. Please enter a valid email and password.")

        if st.button("Login"):
            login_modal()
        
        
        


    with get_started_col:
        if st.button("Get Started"):
            st.write("Do you want to sign up as a Volunteer or an Organization?")
            volunteer_col, organization_col = st.columns([1, 1])
            with volunteer_col:
                with st.popover("Volunteer"):
                    st.write("Volunteers can sign up to help organizations in their community.")
                    if st.button("Sign up as Volunteer"):
                        st.session_state['user_type'] = 'volunteer'
                        st.session_state['logged_in'] = True
                        st.write("Volunteer account created successfully!")
            
            with organization_col:
                with st.popover("Organization"):
                    st.write("Organizations can post events and recruit volunteers.")
                    if st.button("Sign up as Organization"):
                        st.session_state['user_type'] = 'organization'
                        st.session_state['logged_in'] = True
                        st.write("Organization account created successfully!")
            # with volunteer_col:
            #     if st.button("Sign up as Volunteer"):
            #         # Collect required information for Volunteer sign-up
            #         name = st.text_input("Enter your name:")
            #         email = st.text_input("Enter your email:")
            #         latitude = st.number_input("Enter your latitude:")
            #         longitude = st.number_input("Enter your longitude:")
            #         distance = st.number_input("Enter your preferred distance:")
            #         if name and email:
            #             response = requests.post(f"{API_URL}/users", json={
            #                 "email": email,
            #                 "name": name,
            #                 "latitude": latitude,
            #                 "longitude": longitude,
            #                 "distance": distance
            #             })
            #             if response.status_code == 201:
            #                 user_data = response.json()
            #                 st.session_state['user_type'] = 'volunteer'
            #                 st.session_state['logged_in'] = True
            #                 st.session_state['user_id'] = user_data['id']
            #                 st.write("Volunteer account created successfully!")
            #             else:
            #                 st.write("Failed to create volunteer account.")
            
            # with organization_col:
            #     if st.button("Sign up as Organization"):
            #         # Collect required information for Organization sign-up
            #         name = st.text_input("Enter your organization name:")
            #         email = st.text_input("Enter your email:")
            #         description = st.text_area("Enter a description for your organization:")
            #         if name and email:
            #             response = requests.post(f"{API_URL}/organizations", json={
            #                 "name": name,
            #                 "email": email,
            #                 "description": description
            #             })
            #             if response.status_code == 201:
            #                 org_data = response.json()
            #                 st.session_state['user_type'] = 'organization'
            #                 st.session_state['logged_in'] = True
            #                 st.session_state['user_id'] = org_data['id']
            #                 st.write("Organization account created successfully!")
            #             else:
            #                 st.write("Failed to create organization account.")
