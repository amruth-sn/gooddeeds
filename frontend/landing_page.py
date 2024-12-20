import streamlit as st
import requests
from display_organizations import *
from geopy.geocoders import Nominatim
import time
import os


def landing_page():
    API_URL =st.session_state['api_url']
    # Initialize session states if they don't exist
    if 'signup_type' not in st.session_state:
        st.session_state.signup_type = None
    if 'show_options' not in st.session_state:
        st.session_state.show_options = False
    if 'modal_key' not in st.session_state:
        st.session_state.modal_key = 0
        
    def is_valid_zip(zip_code):
    # Check if the ZIP code is all digits and is either 5 or 9 characters long
        if zip_code.isdigit() and (len(zip_code) == 5 or len(zip_code) == 9):
            return True
    # Check if it's in the ZIP+4 format (5 digits, a hyphen, and 4 digits)
        if len(zip_code) == 10 and zip_code[:5].isdigit() and zip_code[5] == '-' and zip_code[6:].isdigit():
            return True
        return False
    
    def zipcode_to_latlong(zipcode):
        geolocator = Nominatim(user_agent="gooddeeds")
        location = geolocator.geocode(f'{zipcode}, USA')
        return location.latitude, location.longitude
    


    current_dir = os.path.dirname(__file__)
    col0, g, _ = st.columns([3, 1, 1])
    with col0:
        cola, colb = st.columns([2, 1])
        with cola:
            image_path = os.path.join(current_dir, "assets", "rb_74201.png")
            st.image(image_path, width=100)
            st.title("Welcome to GoodDeeds!")
            st.subheader("Empowering communities through volunteer initiatives.")
            st.write("Join hands with NGOs to support community service and post-disaster recovery efforts. Whether you're an organization looking for volunteers or a user willing to contribute, this platform connects you to impactful opportunities.")

            
        get_started_col, login_col, _ = st.columns([1, 1, 1])
        
        with login_col:
            @st.dialog("Login")
            def login_modal():
                email = st.text_input("Enter your email:")
                password = st.text_input("Enter your password:", type="password")
                if st.button("Submit"):
                    if email and password:
                        # check if in users table first and then check if in organizations table
                        response = requests.post(f"{API_URL}/login",json={"email": email, "password": password})
                        if response.status_code == 200:
                            st.session_state['logged_in'] = True
                            st.write("Login successful!")
                            st.session_state['user_type'] = response.json()['role']
                            st.session_state['user_id'] = response.json()['user_id'] if st.session_state['user_type'] == 'volunteer' else response.json()['org_id']
                            # print(st.session_state['user_type'])

                            st.rerun()
                        else:
                            st.write("Login failed. Please enter a valid email and password.")
                    else:
                        st.write("Login failed. Please enter a valid email and password.")
                        
            if st.button("Login"):
                login_modal()
    
        with get_started_col:
            def reset_states():
                st.session_state.show_options = True
                st.session_state.signup_type = None
                
            if st.button("Get Started"):
                reset_states()
                
                if st.session_state.show_options:
                    @st.dialog("How would you like to sign up?")
                    def type_modal():
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Sign up as Volunteer"):
                                if st.session_state.signup_type != 'volunteer':
                                    st.session_state.signup_type = 'volunteer'
                                    st.session_state.modal_key += 1
                                    st.rerun()
                                
                        with col2:
                            if st.button("Sign up as Organization"):
                                if st.session_state.signup_type != 'organization':
                                    st.session_state.signup_type = 'organization'
                                    st.session_state.modal_key += 1
                                    st.rerun()
                type_modal()
        
            if st.session_state.signup_type == 'volunteer':
                @st.dialog("Volunteer Registration")
                def volunteer_modal():
                    st.write("Volunteers can sign up to help organizations in their community.")
                    name = st.text_input("Enter your name:", key=f"v_name_{st.session_state.modal_key}")
                    email = st.text_input("Enter your email:", key=f"v_email_{st.session_state.modal_key}")
                    password = st.text_input("Enter your password:", type="password", key=f"v_pass_{st.session_state.modal_key}")
                    password2 = st.text_input("Re-enter your password:", type="password", key=f"v_pass2_{st.session_state.modal_key}")
                    location = st.text_input("Enter your location as a zip code:", key=f"v_loc_{st.session_state.modal_key}")
                    slider = st.slider("Select your preferred distance:", 0, 200, 1, key=f"v_slider_{st.session_state.modal_key}")
                    
                    col1, col2 = st.columns([1,3])
                    with col1:
                        if st.button("Cancel", key=f"v_cancel_{st.session_state.modal_key}"):
                            reset_states()
                            st.rerun()
                    with col2:
                        if st.button("Sign up", key=f"v_submit_{st.session_state.modal_key}"):
                            if password != password2:
                                st.write("Passwords do not match. Please try again.")
                            elif not is_valid_zip(location):
                                st.write("Please enter a valid zip code.")
                            elif email and password:
                                latitude, longitude = zipcode_to_latlong(location)
                                response = requests.post(f"{API_URL}/signup", json={
                                "type": "user",
                                "name": name,
                                "email": email,
                                "password": password,
                                "latitude": latitude,
                                "longitude": longitude,
                                "distance": slider
                            })
                                if response.status_code == 201:
                                    st.write("Volunteer account created successfully! Please log in.")
                                    time.sleep(2)
                                    reset_states()
                                    st.rerun()
                                elif response.status_code == 500:
                                    st.write("Please refresh the page and try again.")
                                else:
                                    
                                    st.write("Sign up failed. Please try again.")

                                
                            else:
                                st.write("Sign up failed. Please enter all required fields.")
                volunteer_modal()
                
            elif st.session_state.signup_type == 'organization':
                @st.dialog("Organization Registration")
                def organization_modal():
                    st.write("Organizations can make posts about events impacting communities.")
                    email = st.text_input("Enter your email:", key=f"o_email_{st.session_state.modal_key}")
                    password = st.text_input("Enter your password:", type="password", key=f"o_pass_{st.session_state.modal_key}")
                    password2 = st.text_input("Re-enter your password:", type="password", key=f"o_pass2_{st.session_state.modal_key}")
                    name = st.text_input("Enter your organization's name:", key=f"o_name_{st.session_state.modal_key}")
                    description = st.text_area("Enter a brief description of your organization:", key=f"o_desc_{st.session_state.modal_key}")

                    col1, col2 = st.columns([1,3])
                    with col1:
                        if st.button("Cancel", key=f"o_cancel_{st.session_state.modal_key}"):
                            reset_states()
                            st.rerun()
                    with col2:
                        if st.button("Sign up", key=f"o_submit_{st.session_state.modal_key}"):
                            if password != password2:
                                st.write("Passwords do not match. Please try again.")
                            elif email and password and name:
                                response = requests.post(f"{API_URL}/signup", json={
                                "type": "organization",
                                "name": name,
                                "email": email,
                                "password": password,
                                "description": description
                            })

                                if response.status_code == 201:
                                    st.write("Organization account created successfully! Please log in.")
                                    time.sleep(2)
                                    reset_states()
                                    st.rerun()
                                elif response.status_code == 500:
                                    st.write("Please refresh the page and try again.")
                                else:
                                    st.write("Sign up failed. Please enter all required fields.")
                            else:
                                st.write("Sign up failed. Please enter all required fields.")
                organization_modal()
        
    with g:
            st.write("")
            newimage_path = os.path.join(current_dir, "assets", "rb_58875.png")
            st.image(newimage_path, use_column_width=False, width=500)
