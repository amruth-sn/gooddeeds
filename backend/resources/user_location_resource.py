from flask_restful import Resource
from flask import request
from models import User
import geopy.distance

   
class UserLocationResource(Resource):
    def get(self):
        
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        distance = request.args.get('distance', type=float)

        if lat is None or lon is None or distance is None:
            return {'message': 'Missing required parameters: lat, lon, and distance'}, 400
        
        def calculate_distance(lat1, lon1, lat2, lon2):
            return geopy.distance.geodesic((lat1, lon1), (lat2, lon2)).miles
        
        users_within_distance = []
        all_users = User.query.all()
        
        for user in all_users:
            user_distance = calculate_distance(lat, lon, user.latitude, user.longitude)
            if user_distance <= distance:
                users_within_distance.append({
                    'id': user.id,
                    'name': user.name,
                    'latitude': user.latitude,
                    'longitude': user.longitude,
                    'distance': user_distance
                })

        return {'users': users_within_distance}, 200
   