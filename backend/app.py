from flask import Flask
from flask_restful import Api
from resources.event_mailer_resource import EventMailerResource
from resources.user_mailer_resource import UserMailerResource
from resources.event_location_resource import EventLocationResource
from resources.event_registration_resource import EventRegistrationResource
from resources.event_resource import EventResource
from resources.login_resource import LoginResource
from resources.organization_resource import OrganizationResource
from resources.user_location_resource import UserLocationResource
from resources.user_resource import UserResource
from models import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

api.add_resource(UserResource, '/users/<int:user_id>', '/users')
api.add_resource(OrganizationResource, '/organizations/<int:org_id>', '/organizations')
api.add_resource(EventResource, '/events/<int:event_id>', '/events')
api.add_resource(EventLocationResource, '/events/location')  # For events by latitude/longitude/distance
api.add_resource(UserLocationResource, '/users/location')  # For events by latitude/longitude/distance
api.add_resource(EventRegistrationResource, '/event-registrations')
api.add_resource(UserMailerResource, '/usermailer')
api.add_resource(EventMailerResource, '/eventmailer')
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
