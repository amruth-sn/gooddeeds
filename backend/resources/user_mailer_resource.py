from flask_restful import Resource
from flask import request
from models import Organization, User, Event
import geopy.distance
import requests
from config import Config

def format(user_id, event_name, organization, severity, description, recipient_name=None):
    greeting = str(organization) + " needs your help!" if not recipient_name else f"Dear {recipient_name},"
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        .email-container {{
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .invitation-text {{
            font-size: 24px;
            color: #2c3e50;
            margin-bottom: 20px;
        }}
        
        .event-card {{
            border: 1px solid #eee;
            border-radius: 8px;
            padding: 25px;
            margin: 20px 0;
            background-color: #f9f9f9;
        }}
        
        .event-title {{
            color: #2c3e50;
            font-size: 28px;
            margin-bottom: 10px;
            text-align: center;
        }}
        
        .organization {{
            color: #7f8c8d;
            font-size: 18px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .description {{
            color: #34495e;
            line-height: 1.6;
            margin-bottom: 25px;
            font-size: 16px;
            text-align: left;
        }}
        
        .button-container {{
            text-align: center;
            margin: 30px 0;
        }}
        
        .register-button {{
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            font-size: 18px;
        }}
        
        .register-button:hover {{
            background-color: #2980b9;
        }}
        
        .closing {{
            text-align: center;
            color: #7f8c8d;
            margin-top: 30px;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <div class="invitation-text">{greeting}</div>
        </div>
        
        <div class="event-card">
            <div class="event-title">{event_name}</div>
            <div class="organization">{organization}</div>
            <div class="description">Severity: {severity*'★'}</div>
            <div class="description">{description}</div>
        </div>
        
        <div class="button-container">
            <a href="#rsvp" class="register-button">RSVP Now</a>
        </div>
        
        <div class="closing">
            <p>We hope to see you there!</p>
            <p>Best regards,<br>{organization} Team</p>
        </div>
    </div>
</body>
</html>'''
    
    return html

def send(recipients, html):
    requests.post(
        f"https://api.mailgun.net/v3/{Config.MAILGUN_SANDBOX}.mailgun.org/messages",
        auth=("api", f"{Config.MAILGUN_API_KEY}"),
        data={"from": f"<mailgun@{Config.MAILGUN_SANDBOX}.mailgun.org>",
            "to": ["gooddeedsplatform@gmail.com"],
            "bcc": recipients,
            "subject": "We need your help!",
            "text": "test",
            "html": html})
   
class UserMailerResource(Resource):
    def get(self):
        event_id = request.args.get('event_id', type=int)

        if event_id is None:
            return {'message': 'Missing required parameter: event_id'}, 400
        
        # Fetch the event details
        event = Event.query.get(event_id)
        if event is None:
            return {'message': 'Event not found'}, 404

        event_latitude = event.latitude
        event_longitude = event.longitude
        event_organization_id = event.organization_id
        organization = Organization.query.get(event_organization_id)
        
        def calculate_distance(lat1, lon1, lat2, lon2):
            return geopy.distance.geodesic((lat1, lon1), (lat2, lon2)).miles
        
        users_within_distance = []
        all_users = User.query.all()
                
        for user in all_users:
            distance = calculate_distance(event_latitude, event_longitude, user.latitude, user.longitude)
            if distance <= user.distance:
                users_within_distance.append({
                    'id': user.id,
                    'name': user.name,
                    'latitude': user.latitude,
                    'longitude': user.longitude,
                    'distance': distance,
                    'email': user.email
                })

        for u in users_within_distance:
            print(u)
            html = format(u.get('id'), event.name, organization.name, event.severity, event.description) 
            send(u.get('email'), html)
        return {'mail': True}, 200
