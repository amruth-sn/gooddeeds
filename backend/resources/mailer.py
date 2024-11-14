from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, Email
from config import Config

def send(recipients, events):
    if not events:
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        
        message = Mail(
            from_email=Email(Config.SENDER_EMAIL),
            to_emails=To('gooddeedsplatform@gmail.com'),
            subject='Your help is needed!',
            plain_text_content='Testing some SendGrid awesomeness!'
        )
        
        # Add BCCs
        if isinstance(recipients, str):
            recipients = [recipients]
        for recipient in recipients:
            message.add_bcc(recipient)

        try:
            response = sg.send(message)
            return response.status_code
        except Exception as e:
            print(f"Error sending email: {e}")
            raise