from flask_restful import Resource
from flask import request
from models import Event
import geopy.distance

class EventLocationResource(Resource):
    def get(self):
        
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        distance = request.args.get('distance', type=float)

        if lat is None or lon is None or distance is None:
            return {'message': 'Missing required parameters: lat, lon, and distance'}, 400
        
        def calculate_distance(lat1, lon1, lat2, lon2):
            return geopy.distance.geodesic((lat1, lon1), (lat2, lon2)).miles
        
        events_within_distance = []
        all_events = Event.query.all()
        
        for event in all_events:
            event_distance = calculate_distance(lat, lon, event.latitude, event.longitude)
            # print(event_distance)
            if event_distance <= distance:
                events_within_distance.append({
                    'id': event.id,
                    'name': event.name,
                    'organization_id': event.organization_id,
                    'latitude': event.latitude,
                    'longitude': event.longitude,
                    'description': event.description,
                    'time': event.time.isoformat(),
                    'distance': event_distance,
                    'severity': event.severity
                })

        return {'events': events_within_distance}, 200
 