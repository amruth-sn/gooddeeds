from flask_restful import Resource
from flask import request
from models import User, db

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
                'password': user.password,
                'xp': user.xp
            }, 200
        return {'message': 'User not found'}, 404

    def post(self):
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'name', 'latitude', 'longitude', 'distance', 'password']
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
            password=data['password'],
            xp=data.get('xp', 0)  # Default to 0 if xp not provided
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return {'message': 'User created', 'id': new_user.id}, 201