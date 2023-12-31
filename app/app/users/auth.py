from flask import jsonify, request
from werkzeug.http import HTTP_STATUS_CODES
from datetime import timedelta, datetime
from functools import wraps
import jwt
from app.users.models import User
from app.settings import Config



def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token_name = 'Access-Token'
        if not token_name in request.headers:
            return jsonify({'message': 'not found token'})
        token = request.headers[token_name]
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            # print(data)
            user = User.query.filter_by(id=data['id']).first()
            if user.active:
                kwargs["user_id"] = user.id
            else:
                return jsonify({'message': 'token is invalid'})
            # print(kwargs)
        except:
            return jsonify({'message': 'token is invalid'})
        return f(*args, **kwargs)
    return decorator


def generate_jwt_token(data, lifetime=None):
    """ Generates a new JWT token, wrapping information provided by payload (dict)
    Lifetime describes (in minutes) how much time the token will be valid """
    payload = {"id": data.id, "email": data.email, "password": data.password}
    if lifetime:
        payload['exp'] = (datetime.now() + timedelta(minutes=lifetime)).timestamp()
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
