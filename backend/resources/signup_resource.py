from flask import Flask, request, jsonify
from flask_restful import Resource
from models import User, Organization
from resources.organization_resource import OrganizationResource
from resources.user_resource import UserResource
from utils import retry_on_db_error

app = Flask(__name__)

class SignUpResource(Resource):
    @retry_on_db_error()
    def post(self):
        data = request.get_json()
        account_type = data.get('type')
        
        if account_type == 'organization':
            org_resource = OrganizationResource()
            response, status_code = org_resource.post()
            return response, status_code
        
        elif account_type == 'user':
            user_resource = UserResource()
            response, status_code = user_resource.post()
            return response, status_code
        
        else:
            return {"error": "Invalid account type specified."}, 400
        

if __name__ == '__main__':
    app.run(debug=True)
