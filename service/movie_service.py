from model.models import Movie, Genre, Actor, Director

class MovieService:
    @staticmethod
    def search_movies(title='', release_year='', genre_name='', actor_name='', director_name=''):
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

        return query.all()

    @staticmethod
    def serialize_movie(movie):
        return {
            'id': movie.id,
            'title': movie.title,
            'release_year': movie.release_year,
            'description': movie.description,
            'genres': [genre.name for genre in movie.genres],
            'actors': [actor.name for actor in movie.actors],
            'directors': [director.name for director in movie.directors]
        }