import requests

def send(recipients, events):
    if not events:
        requests.post(
            "https://api.mailgun.net/v3/sandboxb60fe2f98f7648a484618d404bf779ab.mailgun.org/messages",
            auth=("api", "85a45e972e315b848c6aca6512439175-72e4a3d5-8c1842e3"),
            data={"from": "Excited User <mailgun@sandboxb60fe2f98f7648a484618d404bf779ab.mailgun.org>",
                "to": ["bostonhacksgooddeeds@gmail.com"],
                "bcc": recipients,
                "subject": "Your help is needed!",
                "text": "Testing some Mailgun awesomeness!"})