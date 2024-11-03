from flask import Flask, request, jsonify
from flask_restful import Resource
from models import User, Organization

app = Flask(__name__)

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"error": "Email and password are required."}, 400

        # Check in organizations database
        organization = Organization.query.filter_by(email=email).first()
        if organization:
            if organization.password == password:  # Direct password check, no hashing
                return {"role": "organization", "org_id": organization.id}, 200
            else:
                return {"error": "Invalid credentials."}, 401

        # Check in users database
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:  # Direct password check, no hashing
                return {"role": "volunteer", "user_id": user.id}, 200
            else:
                return {"error": "Invalid credentials."}, 401

        return {"error": "Email not found."}, 404

if __name__ == '__main__':
    app.run(debug=True)
