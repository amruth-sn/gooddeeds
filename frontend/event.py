import streamlit as st

def post_event():
    st.header("Post an Event/Drive")
    st.text_input("Event Name")
    st.text_area("Event Details")
    st.date_input("Date of Event")
    st.text_input("Event Location")
    if st.button("Post Event"):
        st.success("Event posted successfully.")
        # Add logic to save event details in the database