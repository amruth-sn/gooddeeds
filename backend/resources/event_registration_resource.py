from flask_restful import Resource
from flask import request
from models import Event, db, EventRegistration, User

class EventRegistrationResource(Resource):
    def get(self):
        event_id = request.args.get('event_id')
        user_id = request.args.get('user_id')

        # Validate required parameters
        if not event_id or not user_id:
            return {'message': 'Missing required parameters: event_id and user_id'}, 400

        # Check if the registration exists
        registration = EventRegistration.query.filter_by(event_id=event_id, user_id=user_id).first()

        if registration:
            return {'registered': True}, 200
        else:
            return {'registered': False}, 200
        
    def post(self):
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['event_id', 'user_id']
        for field in required_fields:
            if field not in data:
                return {'message': f'Missing required field: {field}'}, 400

        # Check if the event exists
        event = Event.query.get(data['event_id'])
        if not event:
            return {'message': 'Event not found'}, 404

        # Check if the user exists
        user = User.query.get(data['user_id'])
        if not user:
            return {'message': 'User not found'}, 404

        # Check if the registration already exists
        existing_registration = EventRegistration.query.filter_by(event_id=data['event_id'], user_id=data['user_id']).first()
        if existing_registration:
            return {'message': 'User is already registered for this event'}, 400

        # Create a new event registration
        new_registration = EventRegistration(
            event_id=data['event_id'],
            user_id=data['user_id']
        )
        
        db.session.add(new_registration)
        db.session.commit()
        
        return {'message': 'User registered for the event', 'event_id': new_registration.event_id, 'user_id': new_registration.user_id}, 201
    
