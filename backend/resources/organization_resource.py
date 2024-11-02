from flask_restful import Resource
from flask import request
from models import db, Organization

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