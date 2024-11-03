from flask import Flask, request, jsonify
from flask_restful import Resource
from models import Event  # Assuming Event model is defined in models.py

app = Flask(__name__)

class EventListResource(Resource):
    def get(self, org_id):
        # Query the Event database for events with the matching organization_id
        events = Event.query.filter_by(organization_id=org_id).all()
        # Convert the events to a list of dictionaries
        result = [
            {   
                'id': event.id,
                'name': event.name,
                'description': event.description,
                'date': event.time.strftime('%Y-%m-%d %H:%M:%S'),
                'latitude': event.latitude,
                'longitude': event.longitude,
                'organization_id': event.organization_id,
                'severity': event.severity
            }
            for event in events
        ]
        
        return result, 200

if __name__ == '__main__':
    app.run(debug=True)