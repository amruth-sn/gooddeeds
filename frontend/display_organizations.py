import streamlit as st
import streamlit_chat as message

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
    

    for msg in st.session_state['messages']:
        if msg['role'] == 'user':
            message(msg['content'], is_user=True)
        else:
            message(msg['content'])