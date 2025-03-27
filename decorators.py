from flask import request, jsonify
import jwt
from functools import wraps
from app import app
from models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Токен отсутствует'}), 403

        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(payload['user_id'])
            if not current_user:
                return jsonify({'message': 'Неверный токен'}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Токен истек'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Неверный токен'}), 403

        return f(current_user, *args, **kwargs)

    return decorated
