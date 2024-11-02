from flask_restful import Resource
from flask import request
from models import Event, db, Organization

class EventResource(Resource):
    def get(self, event_id):
        event = Event.query.get(event_id)
        if event:
            return {
                'id': event.id,
                'name': event.name,
                'organization_id': event.organization_id,
                'latitude': event.latitude,
                'longitude': event.longitude,
                'description': event.description,
                'time': event.time.isoformat()  # Return time in ISO format
            }, 200
        return {'message': 'Event not found'}, 404

    def post(self):
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'organization_id', 'latitude', 'longitude', 'time', 'volunteer_count', 'severity']
        for field in required_fields:
            if field not in data:
                return {'message': f'Missing required field: {field}'}, 400

        # Check if the organization exists
        organization = Organization.query.get(data['organization_id'])
        if not organization:
            return {'message': 'Organization not found'}, 404

        # Create a new event
        new_event = Event(
            name=data['name'],
            organization_id=data['organization_id'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            description=data.get('description', ''),  # Default to empty string if not provided
            time=data['time'],  # Ensure that 'time' is a proper datetime object
            volunteer_count=data['volunteer_count'],
            severity=data['severity']
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        return {'message': 'Event created', 'id': new_event.id}, 201