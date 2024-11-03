import streamlit as st
import requests
import pandas as pd

def rank_users():
    st.title("Users by Rank")
    
    # Fetch user data from API
    user_data = fetch_user_data_from_api()
    
    if user_data:
        # Convert user data to DataFrame
        df = pd.DataFrame(user_data)
        
        # Sort users by XP in descending order
        df = df.sort_values('xp', ascending=False)
        
        # Add rank column
        df['rank'] = range(1, len(df) + 1)
        
        # Reorder columns
        df = df[['rank', 'name', 'email', 'latitude', 'longitude', 'xp']]
        
        # Display the table
        st.table(df)
    else:
        st.write("No user data available.")



def fetch_user_data_from_api():
    API_URL = st.session_state['api_url']
    response = requests.get(f"{API_URL}/getAllUsers")
    if response.status_code == 200:
        users = response.json()
        return users
    else:
        st.write("Unable to fetch users at this time. Please try again later.")
        return None


