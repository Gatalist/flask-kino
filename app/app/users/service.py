from flask import jsonify, request
from werkzeug.http import HTTP_STATUS_CODES
from datetime import timedelta, datetime
from functools import wraps
import jwt
from app.settings import Config
from app import db
from .models import User


class Authorization:
    def create_user(self, input_data):
        # create_validation_schema = CreateUserSchema()

        # errors = create_validation_schema.validate(input_data)
        # if errors:
        #     return {'username': 'len be 4', 'pass': 'len be 6'}

        check_username_exist = User.query.filter_by(username=input_data.get("username")).first()
        if check_username_exist:
            return jsonify({'error': 'Username already exist'})

        check_email_exist = User.query.filter_by(email=input_data.get("email")).first()
        if check_email_exist:
            return jsonify({'error': 'Email already taken'})

        new_user = User(
            username=input_data['username'],
            email=input_data['email'],
        )

        if new_user:
            new_user.set_password(input_data['password'])
            db.session.add(new_user)  # Adds new User record to database
            db.session.commit()  # Comment

            return jsonify({
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'token': self.generate_jwt_token(new_user),
            })

        return jsonify({"error": "user not created, server error"})

    def login_user(self, input_data):
        get_user = User.query.filter_by(email=input_data.get("email")).first()
        if get_user is None:
            return self.error_response(status_code=404, message="User not found")

        if get_user.check_password(input_data.get("password")):
            token = self.generate_jwt_token(get_user)
            return jsonify({Config.TOKEN_NAME: token})
        else:
            return self.error_response(status_code=404, message="Password is wrong")

    @staticmethod
    def error_response(status_code, message=None):
        payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
        if message:
            payload['message'] = message
        response = jsonify(payload)
        response.status_code = status_code
        return response

    @staticmethod
    def unsecret_token(token):
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        print(data)
        user = User.query.filter_by(id=data['id']).first()
        print(user)
        return user

    def token_required(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if not Config.TOKEN_NAME in request.headers:
                return jsonify({'message': 'not found token'})
            token = request.headers[Config.TOKEN_NAME]
            try:
                data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
                # print(data)
                user = User.query.filter_by(id=data['id']).first()
                if user.active:
                    kwargs["user_id"] = user.id
                else:
                    # return jsonify({'message': 'token is invalid'})
                    return self.error_response(status_code=404, message="token is invalid")
                # print(kwargs)
            except:
                # return jsonify({'message': 'token is invalid'})
                return self.error_response(status_code=404, message="token is invalid")
            return f(*args, **kwargs)

        return decorator

    @staticmethod
    def generate_jwt_token(data, lifetime=None):
        """ Generates a new JWT token, wrapping information provided by payload (dict)
        Lifetime describes (in minutes) how much time the token will be valid """
        payload = {"id": data.id, "email": data.email, "password": data.password}
        if lifetime:
            payload['exp'] = (datetime.now() + timedelta(minutes=lifetime)).timestamp()
        return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
