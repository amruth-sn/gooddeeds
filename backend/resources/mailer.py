import requests
from config import Config

def send(recipients, events):
    if not events:
        requests.post(
            f"https://api.mailgun.net/v3/{Config.MAILGUN_SANDBOX}.mailgun.org/messages",
            auth=("api", f"{Config.MAILGUN_API_KEY}"),
            data={"from": f"Excited User <mailgun@{Config.MAILGUN_SANDBOX}.mailgun.org>",
                "to": ["gooddeedsplatform@gmail.com"],
                "bcc": recipients,
                "subject": "Your help is needed!",
                "text": "Testing some Mailgun awesomeness!"
                "html"})