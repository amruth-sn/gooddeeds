def generate_invitation_email(event_name, organization, description, recipient_name=None):
    """
    Generate HTML email content for a single event invitation.
    
    Args:
        event_name: Name of the event
        organization: Organization hosting the event
        description: Event description
        recipient_name: Name of the recipient (optional)
    
    Returns:
        String containing the complete HTML email
    """
    
    greeting = "You're invited!" if not recipient_name else f"Dear {recipient_name},"
    
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
            <div class="organization">Hosted by {organization}</div>
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

# Example usage
if __name__ == "__main__":
    # Sample event
    event = {
        "name": "Annual Tech Conference",
        "organization": "Tech Industry Association",
        "description": "Join us for three days of cutting-edge technology presentations, networking opportunities, and hands-on workshops with industry leaders. This year's conference features keynote speakers from leading tech companies, interactive sessions on emerging technologies, and valuable networking events."
    }
    
    # Generate the HTML
    html_output = generate_invitation_email(
        event["name"],
        event["organization"],
        event["description"],
    )
    
    print(html_output)