from flask import request, jsonify, current_app
from app import app, db
from models import Movie, Actor, Director, Genre, User, QuizQuestion, QuizOption, UserQuizAnswer
from datetime import datetime, timedelta
from decorators import token_required

import jwt
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/search', methods=['GET'])
def search():
    title = request.args.get('title', '')
    release_year = request.args.get('release_year', '')
    genre_name = request.args.get('genre', '')
    actor_name = request.args.get('actor', '')
    director_name = request.args.get('director', '')

    query = Movie.query

    if title:
        query = query.filter(Movie.title.ilike(f'%{title}%'))
    if release_year:
        try:
            year = int(release_year)
            query = query.filter(Movie.release_year == year)
        except ValueError:
            pass
    if genre_name:
        query = query.join(Movie.genres).filter(Genre.name.ilike(f'%{genre_name}%'))
    if actor_name:
        query = query.join(Movie.actors).filter(Actor.name.ilike(f'%{actor_name}%'))
    if director_name:
        query = query.join(Movie.directors).filter(Director.name.ilike(f'%{director_name}%'))

    movies = query.all()
    movies_list = []
    for movie in movies:
        movies_list.append({
            'id': movie.id,
            'title': movie.title,
            'release_year': movie.release_year,
            'description': movie.description,
            'genres': [genre.name for genre in movie.genres],
            'actors': [actor.name for actor in movie.actors],
            'directors': [director.name for director in movie.directors]
        })

    return jsonify(movies_list)

@app.route('/movies', methods=['GET'])
def get_all_movies():
    movies = Movie.query.all()
    movies_list = []
    for movie in movies:
        movies_list.append({
            'id': movie.id,
            'title': movie.title,
            'release_year': movie.release_year,
            'description': movie.description,
            'actors': [actor.name for actor in movie.actors],
            'directors': [director.name for director in movie.directors],
            'genres': [genre.name for genre in movie.genres]
        })
    return jsonify(movies_list)

def generate_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Некорректный запрос'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Некорректный запрос'}), 400

    if User.query.filter((User.username == username)).first():
        return jsonify({'message': 'Пользователь с таким username уже существует'}), 409

    hashed_password = generate_password_hash(password)

    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    token = generate_jwt_token(user.id)

    return jsonify({'token': token}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Некорректный запрос'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Пожалуйста, укажите username и password'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Неверный username или password'}), 401

    token = generate_jwt_token(user.id)

    return jsonify({'token': token}), 200

@app.route('/quiz', methods=['GET'])
@token_required
def get_quiz(current_user):
    questions = QuizQuestion.query.all()
    quiz_data = []
    for q in questions:
        options = QuizOption.query.filter_by(question_id=q.id).all()
        quiz_data.append({
            'id': q.id,
            'question_text': q.question_text,
            'options': [{'id': o.id, 'option_text': o.option_text} for o in options]
        })
    return jsonify(quiz_data), 200


@app.route('/quiz/submit', methods=['POST'])
@token_required
def submit_quiz(current_user):
    data = request.get_json()
    answers = data.get('answers', [])

    if not answers:
        return jsonify({'message': 'Нет ответов'}), 400

    for ans in answers:
        question_id = ans.get('question_id')
        option_id = ans.get('option_id')
        if question_id and option_id:
            answer = UserQuizAnswer(
                user_id=current_user.id,
                question_id=question_id,
                option_id=option_id
            )
            db.session.add(answer)
    db.session.commit()

    genre_scores = {}
    for ans in answers:
        option = QuizOption.query.get(ans.get('option_id'))
        if option and option.genre_id:
            genre_scores[option.genre_id] = genre_scores.get(option.genre_id, 0) + option.weight

    if genre_scores:
        best_genre_id = max(genre_scores, key=genre_scores.get)
    else:
        best_genre_id = None

    if best_genre_id:
        movies = Movie.query.join(Movie.genres).filter(Genre.id == best_genre_id).all()
    else:
        movies = []

    movies_list = [{
        'id': m.id,
        'title': m.title,
        'release_year': m.release_year,
        'description': m.description
    } for m in movies]

    return jsonify({
        'message': 'Квиз завершен',
        'recommended_movies': movies_list,
        'genre_scores': genre_scores
    }), 200
