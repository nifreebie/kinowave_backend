from flask import request, jsonify

from app import app
from service.user_service import UserService


@app.route('/register', methods=['POST'])
def register():
    """
       Регистрация нового пользователя.
       ---
       tags:
         - Auth
       consumes:
         - application/json
       parameters:
         - in: body
           name: body
           description: Данные для регистрации пользователя
           schema:
             type: object
             required:
               - username
               - password
             properties:
               username:
                 type: string
               password:
                 type: string
       responses:
         200:
           description: Регистрация прошла успешно
           schema:
             type: object
             properties:
               token:
                 type: string
         400:
           description: Некорректный запрос
         409:
           description: Пользователь с таким username уже существует
       """
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Некорректный запрос'}), 400

    user, error = UserService.register_user(data.get('username'), data.get('password'))
    if error:
        return jsonify({'message': error}), 409

    token = UserService.generate_jwt_token(user.id)
    return jsonify({'token': token}), 200


@app.route('/login', methods=['POST'])
def login():
    """
        Аутентификация пользователя.
        ---
        tags:
          - Auth
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            description: Данные для входа
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  type: string
                password:
                  type: string
        responses:
          200:
            description: Аутентификация успешна
            schema:
              type: object
              properties:
                token:
                  type: string
          400:
            description: Некорректный запрос
          401:
            description: Неверный username или password
        """
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Некорректный запрос'}), 400

    user = UserService.authenticate_user(data.get('username'), data.get('password'))
    if not user:
        return jsonify({'message': 'Неверный username или password'}), 401

    token = UserService.generate_jwt_token(user.id)
    return jsonify({'token': token}), 200