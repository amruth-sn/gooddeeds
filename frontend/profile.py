import streamlit as st
import requests

def display_profile():
    API_URL = st.session_state['api_url']
    response = requests.get(f"{API_URL}/users/{st.session_state['user_id']}")

    
    value = 'User' if st.session_state['user_type'] == 'volunteer' else 'Organization'
    st.header(f'Update {value} Profile')
    if response.status_code == 200:
        user_data = response.json()
        level = user_data['xp']
        st.write(f"**Current level: {level}**")
        if level < 10:
            st.write(f"Reach level 10 to start unlocking rewards!")
    else:
        st.write("No user data available.")
    st.text_input("Name", f'{value} Name')
    st.text_input("Email", "user@example.com")

    if st.session_state['user_type'] == 'volunteer':
        st.slider("**Update Distance:**", 0, 200, 1)
            
    elif st.session_state['user_type'] == 'organization':
        st.text_input("**Update Description**", "Write new description here...")

    if st.button("Update Details"):
        st.success("Details Updated!")