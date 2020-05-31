"""
sursa de inspiratie:
https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
"""
from flask_restful import Resource, reqparse
from util import Users
from flask import jsonify, make_response

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_raw_jwt)


parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        return data


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()

        if not data['username'] in Users.get_users().keys():
            return make_response(jsonify({'message': 'User doesn`t exist'}), 400)
        else:
            current_user = Users.get_users()[data['username']]

        if data['password'] == current_user['password']:
            access_token = create_access_token(identity=data['username'])

            return_value = make_response(jsonify({'message': 'Logged in as {}'.format(data['username']),
                                                 'access_token': access_token}))
        else:
            return_value = make_response(jsonify({'message':  "Wrong credentials!"}), 400)

        return return_value


class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}


class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}


class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}


class AllUsers(Resource):
    def get(self):
        return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}


class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
        }