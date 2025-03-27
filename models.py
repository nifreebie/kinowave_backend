from app import db

movie_actor = db.Table('movie_actor',
                       db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
                       db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
                       )

movie_director = db.Table('movie_director',
                          db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
                          db.Column('director_id', db.Integer, db.ForeignKey('directors.id'), primary_key=True)
                          )

movie_genre = db.Table('movie_genre',
                       db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
                       db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
                       )


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_year = db.Column(db.Integer)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    actors = db.relationship('Actor', secondary=movie_actor, backref='movies')
    directors = db.relationship('Director', secondary=movie_director, backref='movies')
    genres = db.relationship('Genre', secondary=movie_genre, backref='movies')


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date)
    bio = db.Column(db.Text)


class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date)
    bio = db.Column(db.Text)


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class User(db.Model):
     __tablename__ = 'users'
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(255), unique=True, nullable=False)
     password = db.Column(db.String(255), nullable=False)
     created_at = db.Column(db.DateTime, default=db.func.now())

class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(512), nullable=False)
    options = db.relationship('QuizOption', backref='question', lazy=True)

class QuizOption(db.Model):
    __tablename__ = 'quiz_options'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'), nullable=False)
    option_text = db.Column(db.String(255), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))  # опционально, если связаны с жанрами
    weight = db.Column(db.Integer, default=1)

class UserQuizAnswer(db.Model):
    __tablename__ = 'user_quiz_answers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('quiz_options.id'), nullable=False)
    answered_at = db.Column(db.DateTime, server_default=db.func.now())