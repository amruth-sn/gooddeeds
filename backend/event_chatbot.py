import requests
import openai 
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



class EventChatbot:
    def __init__(self, event_id):
        self.event_id = event_id
        self.event_description = self.fetch_event_description()

    def fetch_event_description(self):
        try:
            print(self.event_id)
            api_url = f"https://gooddeeds.onrender.com/events/{self.event_id}"
            response = requests.get(api_url)

            if response.status_code == 200:
                event_data = response.json()
                description = f"""
                Event: {event_data.get('name', 'N/A')}
                Organization: {event_data.get('organization', {}).get('name', 'Unknown')}
                Description: {event_data.get('description', 'N/A')}
                Date and Time: {event_data.get('time', 'N/A')}
                Location: Latitude {event_data.get('latitude', 'N/A')}, Longitude {event_data.get('longitude', 'N/A')}
                Volunteers Needed: {event_data.get('volunteer_count', 'N/A')}
                Severity Level: {event_data.get('severity', 'N/A')}
                """
                return description
            else:
                return f"Failed to fetch event details. Status code: {response.status_code}"
        except Exception as e:
            return f"An error occurred while fetching event details: {str(e)}"

    def get_response(self, question, conversation_history):
        messages = [
            {"role": "system", "content": f"You are an AI assistant that answers questions about a specific event. Here's the event description: {self.event_description}"},
            *conversation_history,
            {"role": "user", "content": question}
        ]

        try:
            client = OpenAI()  # Create an instance of the OpenAI client
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            answer = response.choices[0].message.content
            return answer
        except Exception as e:
            return f"An error occurred: {str(e)}"