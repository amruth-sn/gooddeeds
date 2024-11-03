from flask import Blueprint, jsonify, request
import openai
from models import Event, db

chat_bp = Blueprint('chat', __name__)

class ChatbotHelper:
    def __init__(self, api_key):
        openai.api_key = api_key
        
    def generate_response(self, event_description, user_message):
        try:
            # Create a system message that provides context about the event
            system_message = f"You are a helpful assistant providing information about the following event: {event_description}"
            
            # Create the messages array for the chat
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150
            )
            
            return response.choices[0].message['content']
        except Exception as e:
            return str(e)
