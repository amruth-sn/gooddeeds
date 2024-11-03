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
    st.markdown(
        """
        <style>
        .styled-table {
            font-family: Arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }
        .styled-table th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            padding: 8px;
            text-align: center;
        }
        .styled-table td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .styled-table tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .styled-table tr:hover {
            background-color: #ddd;
        }
        .highlight-top-rank {
            background-color: #FFD700; /* Gold for top ranks */
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if user_data:
        # Convert user data to DataFrame
        df = pd.DataFrame(user_data)

        # Sort users by XP in descending order
        df = df.sort_values('xp', ascending=False)

        # Add rank column
        df['rank'] = range(1, len(df) + 1)

        # Reorder columns
        df = df[['rank', 'name', 'email', 'latitude', 'longitude', 'xp']]
        # df = df[['rank', 'name', 'email', 'zipcode', 'xp']]


        # Display table with custom CSS
        styled_table = df.to_html(
            index=False,
            classes="styled-table",
            table_id="user-rank-table",
            escape=False
        )
        st.markdown(styled_table, unsafe_allow_html=True)
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


