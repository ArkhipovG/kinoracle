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


def send_message(message, chat_id):
    url = f'https://api.telegram.org/bot{keys.telegram_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    r = requests.post(url, json=payload)


def send_image(image_url, chat_id):
    url = f'https://api.telegram.org/bot{keys.telegram_token}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': image_url
    }

    r = requests.post(url, json=payload)


def generate_banner_question():
    banner_questions = []
    movies_ids = get_top_rated()
    movie = tmdb.Movies(random.choice(movies_ids))
    response = movie.info()
    path = response['backdrop_path']
    title = response['title']
    banner_questions.append({'question': path, 'answer': title})
    return banner_questions


def generate_popular_banner_question():
    banner_questions = []
    movies_ids = get_top_popular()
    movie = tmdb.Movies(random.choice(movies_ids))
    response = movie.info()
    path = response['backdrop_path']
    title = response['title']
    banner_questions.append({'question': path, 'answer': title})
    return banner_questions


def start_banner_quiz(chat_id):
    banner_questions = generate_banner_question()
    question = choice(banner_questions)
    banner_url = f'https://image.tmdb.org/t/p/w500{question["question"]}'
    user_state[chat_id] = question
    send_message("What movie is it?", chat_id)
    send_image(banner_url, chat_id)


def start_pop_banner_quiz(chat_id):
    banner_questions = generate_popular_banner_question()
    question = choice(banner_questions)
    banner_url = f'https://image.tmdb.org/t/p/w500{question["question"]}'
    user_state[chat_id] = question
    send_message("What movie is it?", chat_id)
    send_image(banner_url, chat_id)


def check_user_state(chat_id, user_answer):
    correct_answer = user_state.get(chat_id, {}).get("answer")
    if correct_answer:
        if correct_answer.lower().startswith(user_answer.lower()):
            response_message = "🎉 Correct! Want to try again?"
        else:
            response_message = f"❌ Wrong. The correct answer was: {correct_answer}. Try again!"
        del user_state[chat_id]
    else:
        response_message = "To start again click here 👇"
    type_quiz_buttons2(response_message, chat_id)


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