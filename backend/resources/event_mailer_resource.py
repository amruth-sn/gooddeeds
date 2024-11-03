from flask_restful import Resource
from flask import request
from models import Organization, User, Event
import geopy.distance
import requests

def format(user_id, events):
    # Define the CSS and header part
    header = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        .event-container {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .event {
            margin-bottom: 30px;
            border-bottom: 1px solid #eee;
            padding-bottom: 20px;
        }
        
        .event:last-child {
            border-bottom: none;
        }
        
        .event-title {
            color: #2c3e50;
            font-size: 20px;
            margin-bottom: 5px;
        }
        
        .organization {
            color: #7f8c8d;
            font-size: 16px;
            margin-bottom: 10px;
        }
        
        .description {
            color: #34495e;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        .register-button {
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .register-button:hover {
            background-color: #2980b9;
        }
    </style>
</head>
<body>
    <div class="event-container">
        <h1 style="color: #2c3e50; margin-bottom: 30px;">Upcoming Events</h1>
'''

    # Define the footer
    footer = '''
    </div>
</body>
</html>'''

    # Generate HTML for each event
    event_contents = []
    for name, organization, description in events:
        # Create a URL-friendly version of the event name for the registration link
        register_link = f"#register-{name.lower().replace(' ', '-')}"
        
        event_html = f'''
        <div class="event">
            <div class="event-title">{name}</div>
            <div class="organization">{organization}</div>
            <div class="description">{description}</div>
            <a href="{register_link}" class="register-button">Register Now</a>
        </div>'''
        event_contents.append(event_html)
    
    # Combine all parts
    all_events = "\n".join(event_contents)
    complete_html = header + all_events + footer
    
    return complete_html

def send(recipients, html):
    requests.post(
        "https://api.mailgun.net/v3/sandboxb60fe2f98f7648a484618d404bf779ab.mailgun.org/messages",
        auth=("api", "85a45e972e315b848c6aca6512439175-72e4a3d5-8c1842e3"),
        data={"from": "<mailgun@sandboxb60fe2f98f7648a484618d404bf779ab.mailgun.org>",
            "to": ["bostonhacksgooddeeds@gmail.com"],
            "bcc": recipients,
            "subject": "Here are some events in the upcoming week!",
            "text": "test",
            "html": html})
   
class EventMailerResource(Resource):
    def get(self):
        
        def calculate_distance(lat1, lon1, lat2, lon2):
            return geopy.distance.geodesic((lat1, lon1), (lat2, lon2)).miles
        
        users = User.query.all();
        events = Event.query.all();
        
        for u in users:
            events_within_distance = []
            for e in events:
                distance = calculate_distance(u.latitude, u.longitude, e.latitude, e.longitude)
                if distance <= u.distance:
                    events_within_distance.append((e.name, e.organization, e.description))
            html = format(u.id, events_within_distance)
            send(u.get('email'), html)
            
        return {'mail': True}, 200
