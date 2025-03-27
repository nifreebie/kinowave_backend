from model.models import QuizQuestion, QuizOption, UserQuizAnswer, Movie, Genre, db

class QuizService:
    @staticmethod
    def get_quiz():
        questions = QuizQuestion.query.all()
        quiz_data = []
        for q in questions:
            options = QuizOption.query.filter_by(question_id=q.id).all()
            quiz_data.append({
                'id': q.id,
                'question_text': q.question_text,
                'options': [{'id': o.id, 'option_text': o.option_text} for o in options]
            })
        return quiz_data

    @staticmethod
    def submit_quiz(user_id, answers):
        if not answers:
            return 'Нет ответов', None

        for ans in answers:
            question_id = ans.get('question_id')
            option_id = ans.get('option_id')
            if question_id and option_id:
                answer = UserQuizAnswer(user_id=user_id, question_id=question_id, option_id=option_id)
                db.session.add(answer)
        db.session.commit()

        genre_scores = {}
        for ans in answers:
            option = QuizOption.query.get(ans.get('option_id'))
            if option and option.genre_id:
                genre_scores[option.genre_id] = genre_scores.get(option.genre_id, 0) + option.weight

        best_genre_id = max(genre_scores, key=genre_scores.get) if genre_scores else None
        recommended_movies = Movie.query.join(Movie.genres).filter(Genre.id == best_genre_id).all() if best_genre_id else []

        return None, {
            'recommended_movies': [{
                'id': m.id,
                'title': m.title,
                'release_year': m.release_year,
                'description': m.description
            } for m in recommended_movies],
            'genre_scores': genre_scores
        }
