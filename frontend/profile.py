import streamlit as st

def display_profile():
    value = 'User' if st.session_state['user_type'] == 'volunteer' else 'Organization'
    st.header(f'{value} Profile')
    st.text_input("Name", f'{value} Name', disabled=True)
    st.text_input("Email", "user@example.com", disabled=True)
    if st.session_state['user_type'] == 'volunteer':
        st.write(f"Your current level is level 1. Reach level 10 to start unlocking incentives!")
    
    st.button("Update Details")