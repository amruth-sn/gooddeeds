from flask import Flask, request
from flask_restful import Api, Resource
from models import db, User, Organization, Event, EventRegistration
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'latitude': user.latitude,
                'longitude': user.longitude,
                'distance': user.distance,
                'xp': user.xp
            }, 200
        return {'message': 'User not found'}, 404

    def post(self):
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'name', 'latitude', 'longitude', 'distance']
        for field in required_fields:
            if field not in data:
                return {'message': f'Missing required field: {field}'}, 400

        # Check if the email is unique
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return {'message': 'Email already exists'}, 400

        # Create a new user
        new_user = User(
            email=data['email'],
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            distance=data['distance'],
            xp=data.get('xp', 0)  # Default to 0 if xp not provided
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return {'message': 'User created', 'id': new_user.id}, 201

class OrganizationResource(Resource):
    def get(self, org_id=None):
        if org_id is not None:
            # Get a specific organization by ID
            organization = Organization.query.get(org_id)
            if organization:
                return {
                    'id': organization.id,
                    'name': organization.name,
                    'email': organization.email
                }, 200
            return {'message': 'Organization not found'}, 404
        
        # Get all organizations if no org_id is provided
        organizations = Organization.query.all()
        result = []
        for org in organizations:
            result.append({
                'id': org.id,
                'name': org.name,
                'email': org.email
            })
        return result, 200

    def post(self):
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'description']
        for field in required_fields:
            if field not in data:
                return {'message': f'Missing required field: {field}'}, 400

        # Check if the email is unique
        existing_org = Organization.query.filter_by(email=data['email']).first()
        if existing_org:
            return {'message': 'Email already exists'}, 400

        # Create a new organization
        new_organization = Organization(
            name=data['name'],
            email=data['email'],
            description=data['description']
        )
        
        db.session.add(new_organization)
        db.session.commit()
        
        return {'message': 'Organization created', 'id': new_organization.id}, 201

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
    
    # def near_user(self):
    #     data = request.get_json()
        
    #     # Validate required fields
    #     required_fields = ['user_id']
    #     for field in required_fields:
    #         if field not in data:
    #             return {'message': f'Missing required field: {field}'}, 400
            
        

api.add_resource(UserResource, '/users/<int:user_id>', '/users')
api.add_resource(OrganizationResource, '/organizations/<int:org_id>', '/organizations')
api.add_resource(EventResource, '/events/<int:event_id>', '/events')
api.add_resource(EventRegistrationResource, '/event-registrations')

if __name__ == '__main__':
    app.run(debug=True)
