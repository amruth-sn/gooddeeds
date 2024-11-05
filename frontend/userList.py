import streamlit as st
import requests
import pandas as pd

# def rank_users():
#     st.title("Users by Rank")
    
#     # Fetch user data from API
#     user_data = fetch_user_data_from_api()
    
#     if user_data:
#         # Convert user data to DataFrame
#         df = pd.DataFrame(user_data)
        
#         # Sort users by XP in descending order
#         df = df.sort_values('xp', ascending=False)
        
#         # Add rank column
#         df['rank'] = range(1, len(df) + 1)
        
#         # Reorder columns
#         df = df[['rank', 'name', 'email', 'latitude', 'longitude', 'xp']]

        
#         # Display the table without index using st.dataframe()
#         st.write(df.to_html(index=False), unsafe_allow_html=True)
#     else:
#         st.write("No user data available.")

def rank_users():
    st.title("Users by Rank")

    # Fetch user data from API
    user_data = fetch_user_data_from_api()

    # Define CSS styles to enhance the table's appearance
    st.markdown("""
    <style>
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 16px;
        font-family: sans-serif;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        border-radius: 8px;
        overflow: hidden;
    }

    .styled-table thead tr {
        background: linear-gradient(45deg, #4a8c0f, #45a049);
        color: #ffffff;
        text-align: center;
    }

    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
        text-align: center;
    }

    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
        transition: all 0.3s ease;
    }

    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }

    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #4a8c0f;
    }

    .styled-table tbody tr:hover {
        background-color: #f5f5f5;
        transform: scale(1.01);
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    .styled-table td:first-child {
        font-weight: bold;
        color: #4a8c0f;
        text-align: center;
    }

    /* Top 3 Rankings */
    .styled-table tbody tr:nth-child(1) td:first-child {
        color: #FFD700;
        font-size: 1.2em;
    }

    .styled-table tbody tr:nth-child(2) td:first-child {
        color: #C0C0C0;
        font-size: 1.1em;
    }

    .styled-table tbody tr:nth-child(3) td:first-child {
        color: #CD7F32;
        font-size: 1.1em;
    }

    @media screen and (max-width: 600px) {
        .styled-table {
            font-size: 14px;
        }
        .styled-table th,
        .styled-table td {
            padding: 8px 10px;
        }
    }
    </style>
""", unsafe_allow_html=True)

    if user_data:
        # Convert user data to DataFrame
        df = pd.DataFrame(user_data)

        # Sort users by XP in descending order
        df = df.sort_values('xp', ascending=False)

        # Add rank column
        df['rank'] = range(1, len(df) + 1)

        # Reorder columns
        df = df[['rank', 'name', 'email', 'zipcode', 'xp']]
        # df = df[['rank', 'name', 'email', 'zipcode', 'xp']]
        df = df.rename(columns={'rank': 'Rank', 'name': 'Name', 'zipcode': 'Zip Code', 'xp': 'XP', 'email': 'E-mail'})


    # Display table with custom CSS
        styled_table = df.to_html(
            index=False,
            classes="styled-table",
            table_id="user-rank-table",
            escape=False
        )
        st.markdown(styled_table, unsafe_allow_html=True)

        # Display table with custom CSS
        
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


