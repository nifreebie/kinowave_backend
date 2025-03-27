from flask import request, jsonify

from app import app
from model.models import Movie
from service.movie_service import MovieService


@app.route('/search', methods=['GET'])
def search():
    """
        Поиск фильмов.
        ---
        tags:
          - Movies
        parameters:
          - name: title
            in: query
            type: string
            description: Название фильма
          - name: release_year
            in: query
            type: string
            description: Год выпуска фильма
          - name: genre
            in: query
            type: string
            description: Жанр фильма
          - name: actor
            in: query
            type: string
            description: Имя актёра
          - name: director
            in: query
            type: string
            description: Имя режиссёра
        responses:
          200:
            description: Список найденных фильмов
            schema:
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
                  genres:
                    type: array
                    items:
                      type: string
                  actors:
                    type: array
                    items:
                      type: string
                  directors:
                    type: array
                    items:
                      type: string
        """
    movies = MovieService.search_movies(
        title=request.args.get('title', ''),
        release_year=request.args.get('release_year', ''),
        genre_name=request.args.get('genre', ''),
        actor_name=request.args.get('actor', ''),
        director_name=request.args.get('director', '')
    )

    return jsonify([MovieService.serialize_movie(m) for m in movies])

@app.route('/movies', methods=['GET'])
def get_all_movies():
    """
        Получение списка всех фильмов.
        ---
        tags:
          - Movies
        responses:
          200:
            description: Список фильмов
            schema:
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
                  genres:
                    type: array
                    items:
                      type: string
                  actors:
                    type: array
                    items:
                      type: string
                  directors:
                    type: array
                    items:
                      type: string
        """
    movies = Movie.query.all()
    return jsonify([MovieService.serialize_movie(m) for m in movies])