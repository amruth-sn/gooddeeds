from flask_restful import Resource
from flask import request
from models import Event
from config import Config
from openai import OpenAI

class ChatbotHelper:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def generate_response(self, event_description, user_message):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant for an event with the following description: {event_description}"},
                    {"role": "user", "content": user_message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

class ChatbotResource(Resource):
    def __init__(self):
        self.chatbot = ChatbotHelper(Config.OPENAI_API_KEY)
    
    def post(self, event_id):
        try:
            # Get the user message from request
            data = request.get_json()
            user_message = data.get('message')
            
            # Get event description from database
            event = Event.query.get(event_id)
            if not event:
                return {'error': 'Event not found'}, 404
            
            # Generate response using OpenAI
            response = self.chatbot.generate_response(event.description, user_message)
            
            return {
                'response': response,
                'event_id': event_id
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500