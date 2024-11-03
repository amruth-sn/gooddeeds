from flask import Flask, request, jsonify
from flask_restful import Resource
from models import Organization


app = Flask(__name__)
class OrganizationListResource(Resource):
    def get(self):
        organizations = Organization.query.all()
        result = []
        for org in organizations:
            result.append({
                'id': org.id,
                'name': org.name,
                'email': org.email,
                'description': org.description
            })
        return result, 200

if __name__ == '__main__':
    app.run(debug=True)