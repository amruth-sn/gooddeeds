from flask import Flask, request, jsonify
from flask_restful import Resource
from models import User
from geopy.geocoders import Nominatim


app = Flask(__name__)

def latlong_to_zipcode(latitude, longitude):
    geolocator = Nominatim(user_agent="gooddeeds")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    
    # Extract ZIP code if available
    if location and 'postcode' in location.raw['address']:
        return location.raw['address']['postcode']
    else:
        return "ZIP code not found"

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        result = []
        for user in users:
            zipcode = latlong_to_zipcode(user.latitude, user.longitude)
            result.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'latitude': user.latitude,
                'longitude': user.longitude,
                'zipcode': zipcode,
                'xp': user.xp
            })
        return result, 200

if __name__ == '__main__':
    app.run(debug=True)