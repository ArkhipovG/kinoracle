from random import choice
import keys
import requests
import tmdbsimple as tmdb
import random

tmdb.API_KEY = keys.moviedb_token
tmdb.REQUESTS_TIMEOUT = 5
tmdb.REQUESTS_SESSION = requests.Session()

user_state = {}


def get_top_rated():
    movies = tmdb.Movies()

    total_pages = 5

    top_100 = []

    for page in range(1, total_pages + 1):
        response = movies.top_rated(page=page)
        top_100.extend(response['results'])

    movies_ids = []

    for movie in top_100:
        movies_ids.append(movie['id'])
    return movies_ids


def get_top_popular():
    movies = tmdb.Discover()

    total_pages = 5

    top_100 = []

    for page in range(1, total_pages + 1):
        params = {
            'sort_by': 'vote_count.desc',
        }
        movies = tmdb.Discover()
        popular_movies = movies.movie(**params, page=page)
        top_100.extend(popular_movies['results'])

    movies_ids = []

    for movie in top_100:
        movies_ids.append(movie['id'])
    return movies_ids


def generate_questions():
    movies_ids = get_top_rated()
    questions = []
    for i in range(5):
        movie = tmdb.Movies(random.choice(movies_ids))
        response = movie.info()
        question = response['overview']
        title = response['title']
        questions.append({'question': question, 'answer': title})
    return questions


def generate_popular_questions():
    movies_ids = get_top_popular()
    questions = []
    for i in range(5):
        movie = tmdb.Movies(random.choice(movies_ids))
        response = movie.info()
        question = response['overview']
        title = response['title']
        questions.append({'question': question, 'answer': title})
    return questions


def send_message(message, chat_id):
    url = f'https://api.telegram.org/bot{keys.telegram_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    r = requests.post(url, json=payload)


def start_quiz(chat_id):
    questions = generate_questions()
    question = choice(questions)
    user_state[chat_id] = question
    send_message(question["question"], chat_id)


def start_pop_quiz(chat_id):
    questions = generate_popular_questions()
    question = choice(questions)
    user_state[chat_id] = question
    send_message(question["question"], chat_id)


def check_answer(chat_id, user_answer):
    correct_answer = user_state.get(chat_id, {}).get("answer")
    if correct_answer:
        if correct_answer.lower().startswith(user_answer.lower()):
            response_message = "🎉 Correct! Want to try again?"
        else:
            response_message = f"❌ Wrong. The correct answer was: {correct_answer}"
        del user_state[chat_id]
    else:
        response_message = "To start again click here 👇"
    type_quiz_buttons2(response_message, chat_id)


def quiz_buttons(chat_id):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': "Choose one of the following 👇",
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '🖼️ Picture quiz',
                        'callback_data': f'picture_quiz'
                    }
                ],
                [
                    {
                        'text': '📝 Description quiz',
                        'callback_data': f'description_quiz'
                    }
                ]
            ]
        }
    }
    requests.post(url, json=payload)


def quiz_buttons2(message, chat_id):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '🖼️ Picture quiz',
                        'callback_data': f'picture_quiz'
                    }
                ],
                [
                    {
                        'text': '📝 Description quiz',
                        'callback_data': f'description_quiz'
                    }
                ]
            ]
        }
    }
    requests.post(url, json=payload)


def type_quiz_buttons(chat_id):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': "🧠 Test your movie knowledge! 🧠",
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': 'Top rated movies quizzes',
                        'callback_data': f'top_rated_quiz'
                    }
                ],
                [
                    {
                        'text': 'Top popular movies quizzes',
                        'callback_data': f'top_popular_quiz'
                    }
                ]
            ]
        }
    }
    requests.post(url, json=payload)


def quiz_pop_buttons(chat_id):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': "Choose one of the following 👇",
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '🖼️ Picture quiz',
                        'callback_data': f'pop_picture_quiz'
                    }
                ],
                [
                    {
                        'text': '📝 Description quiz',
                        'callback_data': f'pop_description_quiz'
                    }
                ]
            ]
        }
    }
    requests.post(url, json=payload)


def type_quiz_buttons2(message, chat_id):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': 'Top rated movies quizzes',
                        'callback_data': f'top_rated_quiz'
                    }
                ],
                [
                    {
                        'text': 'Top popular movies quizzes',
                        'callback_data': f'top_popular_quiz'
                    }
                ]
            ]
        }
    }
    requests.post(url, json=payload)