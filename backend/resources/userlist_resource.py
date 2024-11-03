from flask import Flask, request, jsonify
from flask_restful import Resource
from models import User

app = Flask(__name__)
class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        result = []
        for user in users:
            result.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'latitude': user.latitude,
                'longitude': user.longitude,
                'xp': user.xp
            })
        return result, 200

if __name__ == '__main__':
    app.run(debug=True)