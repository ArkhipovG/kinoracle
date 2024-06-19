import keys
import requests
import json
import tmdbsimple as tmdb

tmdb.API_KEY = keys.moviedb_token
tmdb.REQUESTS_TIMEOUT = 5
tmdb.REQUESTS_SESSION = requests.Session()


def list_buttons(chat_id):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': "🍿 Lists of Movies and TV Shows 🍿",
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': 'Watchlist',
                        'callback_data': f'show_watchlist'
                    },
                    {
                        'text': 'Favorites',
                        'callback_data': f'show_favorites'
                    }
                ],
                [
                    {
                        'text': 'Popular',
                        'callback_data': f'popular_list'
                    },
                    {
                        'text': 'Upcoming',
                        'callback_data': f'upcoming_list'
                    }
                ]
            ]
        }
    }
    requests.post(url, json=payload)


def get_popular_tv_list(chat_id):
    movies = tmdb.TV()
    popular_movies = movies.popular()
    results = [
            {
                'id': result['id'],
                'title': result.get('name', 'N/A'),
                'release_date': result.get('first_air_date', 'N/A'),
            }
            for result in popular_movies['results']
        ]
    keyboard = {
        'inline_keyboard': [
            [{'text': f"{movie['title']} ({movie['release_date'][:4] if movie['release_date'] else 'N/A'})",
              'callback_data': f"tv_{movie['id']}"}] for movie in results
        ]
    }
    reply_markup = json.dumps(keyboard)
    message = '🔥 Popular TV shows:'

    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'reply_markup': reply_markup
    }
    requests.post(url, data=payload)

def get_on_the_air_list(chat_id):
    movies = tmdb.TV()
    upcoming_movies = movies.on_the_air()
    results = [
            {
                'id': result['id'],
                'title': result.get('name', 'N/A'),
                'release_date': result.get('first_air_date', 'N/A'),
            }
            for result in upcoming_movies['results']
        ]
    keyboard = {
        'inline_keyboard': [
            [{'text': f"{movie['title']} ({movie['release_date'][:4] if movie['release_date'] else 'N/A'})",
              'callback_data': f"tv_{movie['id']}"}] for movie in results
        ]
    }
    reply_markup = json.dumps(keyboard)
    message = '📺 Currently Airing TV Shows:'

    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'reply_markup': reply_markup
    }
    requests.post(url, data=payload)