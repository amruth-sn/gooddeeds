import streamlit as st
import requests

def display_profile():
    API_URL = st.session_state['api_url']
    response = requests.get(f"{API_URL}/users/{st.session_state['user_id']}") if st.session_state['user_type'] == 'volunteer' else requests.get(f"{API_URL}/organizations/{st.session_state['user_id']}")

    value = 'User' if st.session_state['user_type'] == 'volunteer' else 'Organization'
    sliderval = 5
    st.header(f'Update {value} Profile')
    user_name = ''
    user_mail = ''
    level = 0
    description = ''
    if st.session_state['user_type'] == 'volunteer':
        if response.status_code == 200:
            user_data = response.json()
            user_name = user_data['name']
            user_mail = user_data['email']
            sliderval = int(user_data['distance'])
            level = user_data['xp']
            st.write(f"**Current level: {level}**")
        else:
            st.write("No user data available.")

        if level < 10:
            st.write(f"Reach level 10 to start unlocking rewards!")
        
    elif st.session_state['user_type'] == 'organization':
        if response.status_code == 200:
            user_data = response.json()
            user_name = user_data['name']
            user_mail = user_data['email']
            description = user_data['description']
        else:
            st.write("No organization data available.")

    user_name = st.text_input("Name", f'{user_name}')
    user_mail = st.text_input("Email", f"{user_mail}")

    if st.session_state['user_type'] == 'volunteer':
        sliderval = st.slider("**Update Distance:**", 0, 200, sliderval)
            
    elif st.session_state['user_type'] == 'organization':
        description = st.text_input("**Update Description**", f"{description}")

    if st.button("Update Details"):
        
        if st.session_state['user_type'] == 'volunteer':
            response = requests.put(f"{API_URL}/users/{st.session_state['user_id']}", json={"distance": sliderval, "name": user_name, "email": user_mail})
            if response.status_code != 200:
                st.error("Failed to update details. Please try again.")

        elif st.session_state['user_type'] == 'organization':
            response = requests.put(f"{API_URL}/organizations/{st.session_state['user_id']}", json={"description": description, "name": user_name, "email": user_mail})
            if response.status_code != 200:
                st.error("Failed to update details. Please try again.")
        st.success("Details Updated!")