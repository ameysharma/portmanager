from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api

from scripts.stselection import fetch_nifty_data 


#Main Scripts Writing


data=fetch_nifty_data(symbols)

app = Flask(__name__)
api = Api(app)

# Define your API key (this should be securely stored in production)
API_KEY = '#arshar#123'

# Mock data
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Doe", "email": "jane@example.com"}
]

# Custom decorator to check for API key in request headers
def require_api_key(view_function):
    def decorated_function(*args, **kwargs):
        if request.headers.get('Authorization') != f'Bearer {API_KEY}':
            abort(401, 'Unauthorized access')
        return view_function(*args, **kwargs)
    return decorated_function

class User(Resource):
    @require_api_key
    def get(self, user_id):
        user = next((user for user in users if user["id"] == user_id), None)
        if user:
            return jsonify(user)
        return {"message": "User not found"}, 404

    @require_api_key
    def put(self, user_id):
        data = request.get_json()
        user = next((user for user in users if user["id"] == user_id), None)
        if user:
            user.update(data)
            return jsonify(user)
        return {"message": "User not found"}, 404

    @require_api_key
    def delete(self, user_id):
        global users
        users = [user for user in users if user["id"] != user_id]
        return {"message": "User deleted"}

class UserList(Resource):
    @require_api_key
    def get(self):
        return jsonify(users)

    @require_api_key
    def post(self):
        data = request.get_json()
        new_user = {
            "id": users[-1]["id"] + 1 if users else 1,
            "name": data["name"],
            "email": data["email"]
        }
        users.append(new_user)
        return jsonify(new_user), 201

api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserList, '/users')

if __name__ == '__main__':
    app.run(debug=True)
