from flask import request, jsonify

from app import app
from util.decorators import token_required
from service.quiz_service import QuizService


@app.route('/quiz', methods=['GET'])
@token_required
def get_quiz(current_user):
    """
        Получение вопросов квиза.
        ---
        tags:
          - Quiz
        security:
          - Bearer: []
        responses:
          200:
            description: Список вопросов квиза
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  question_text:
                    type: string
                  options:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                        option_text:
                          type: string
          401:
            description: Неавторизованный запрос
        """
    return jsonify(QuizService.get_quiz()), 200


@app.route('/quiz/submit', methods=['POST'])
@token_required
def submit_quiz(current_user):
    """
       Отправка ответов квиза и получение рекомендаций.
       ---
       tags:
         - Quiz
       security:
         - Bearer: []
       consumes:
         - application/json
       parameters:
         - in: body
           name: body
           description: Ответы на вопросы квиза
           schema:
             type: object
             required:
               - answers
             properties:
               answers:
                 type: array
                 items:
                   type: object
                   properties:
                     question_id:
                       type: integer
                     option_id:
                       type: integer
       responses:
         200:
           description: Квиз завершён, возвращаются рекомендации и результаты
           schema:
             type: object
             properties:
               message:
                 type: string
               recommended_movies:
                 type: array
                 items:
                   type: object
                   properties:
                     id:
                       type: integer
                     title:
                       type: string
                     release_year:
                       type: integer
                     description:
                       type: string
               genre_scores:
                 type: object
                 additionalProperties:
                   type: integer
         400:
           description: Некорректный запрос или отсутствие ответов
         401:
           description: Неавторизованный запрос
       """
    data = request.get_json()
    error, response = QuizService.submit_quiz(current_user.id, data.get('answers', []))
    if error:
        return jsonify({'message': error}), 400
    return jsonify({'message': 'Квиз завершен', **response}), 200