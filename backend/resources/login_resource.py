from flask_restful import Resource
from flask import request
from models import User, Organization

class LoginResource(Resource):
    def get(self):
        email = request.args.get('email')
        
        if not email:
            return {'message': 'Missing required parameter: email'}, 400
        
        organization = Organization.query.filter_by(email=email).first()
        if organization:
            return {'message': 'Organization', 'org_id': organization.id}, 200
        
        user = User.query.filter_by(email=email).first()
        if user:
            return {'message': 'User', 'user_id': user.id}, 200
        
        return {'message': 'Email does not belong to a user or organization'}, 404