import keys
import requests
import tmdbsimple as tmdb
import json

tmdb.API_KEY = keys.moviedb_token
tmdb.REQUESTS_TIMEOUT = 5
tmdb.REQUESTS_SESSION = requests.Session()


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


def adding_buttons(chat_id, movie_id, movie_summary):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': movie_summary,
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': 'Add to watchlist',
                        'callback_data': f'add_to_watchlist {movie_id}'
                    },
                    {
                        'text': 'Add to favorites',
                        'callback_data': f'add_to_favorites {movie_id}'
                    }
                ],
                [
                    {
                        'text': 'Remove from favorites',
                        'callback_data': f'remove_from_favorites {movie_id}'
                    }
                ],
                [
                    {
                        'text': 'Remove from watchlist',
                        'callback_data': f'remove_from_watchlist {movie_id}'
                    }
                ],
                [
                    {
                        'text': 'Recommendations',
                        'callback_data': f'recommendations {movie_id}'
                    },
                    {
                        'text': 'Collection',
                        'callback_data': f'collection {movie_id}'
                    }
                ]
            ]
        }
    }
    requests.post(url, json=payload)


def search_colletion_movies(movie_id):
    movie = tmdb.Movies(movie_id)
    movie_info = movie.info()
    print(movie_info)
    if movie_info['belongs_to_collection'] == None:
        return None
    else:
        collection_id = movie.belongs_to_collection['id']
        collection = tmdb.Collections(collection_id)
        response = collection.info()

        results = [
            {
                'id': result['id'],
                'title': result.get('title', 'N/A'),
                'release_date': result.get('release_date', 'N/A'),
                'overview': result.get('overview', 'N/A')
            }
            for result in response['parts']
        ]
    return results


def send_collection_choices(chat_id, movies):
    keyboard = {
        'inline_keyboard': [
            [{'text': f"{movie['title']} ({movie['release_date'][:4] if movie['release_date'] else 'N/A'})",
              'callback_data': f"movie_{movie['id']}"}] for movie in movies
        ]
    }
    reply_markup = json.dumps(keyboard)
    message = 'Movies from the collection:'

    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'reply_markup': reply_markup
    }
    requests.post(url, data=payload)


def search_movie_poster(movie_id):
    movie = tmdb.Movies(movie_id)
    movie_info = movie.info()
    poster_path = movie_info.get('poster_path')
    if poster_path:
        # Construct the full poster URL
        poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
        return poster_url
    return None


def search_movies(query):
    search = tmdb.Search()
    response = search.movie(query=query)

    results = [
        {
            'id': result['id'],
            'title': result.get('title', 'N/A'),
            'release_date': result.get('release_date', 'N/A'),
            'overview': result.get('overview', 'N/A')
        }
        for result in search.results[:5]  # Limiting to the first 5 results
    ]
    return results


def search_recommend_movies(movie_id):
    movie = tmdb.Movies(movie_id)
    response = movie.recommendations()

    results = [
        {
            'id': result['id'],
            'title': result.get('title', 'N/A'),
            'release_date': result.get('release_date', 'N/A'),

            'overview': result.get('overview', 'N/A')
        }
        for result in response['results'][:5]  # Limiting to the first 5 results
    ]
    return results


def send_movie_choices(chat_id, movies):
    keyboard = {
        'inline_keyboard': [
            [{'text': f"{movie['title']} ({movie['release_date'][:4] if movie['release_date'] else 'N/A'})",
              'callback_data': f"movie_{movie['id']}"}] for movie in movies
        ]
    }
    reply_markup = json.dumps(keyboard)
    message = 'Please choose a movie:'

    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'reply_markup': reply_markup
    }
    requests.post(url, data=payload)


def send_recommendation_movie_choices(chat_id, movies):
    keyboard = {
        'inline_keyboard': [
            [{'text': f"{movie['title']} ({movie['release_date'][:4] if movie['release_date'] else 'N/A'})",
              'callback_data': f"movie_{movie['id']}"}] for movie in movies
        ]
    }
    reply_markup = json.dumps(keyboard)
    message = 'Recommended movies:'

    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'reply_markup': reply_markup
    }
    requests.post(url, data=payload)


def handle_movie_callback(query):
    chat_id = query['message']['chat']['id']
    movie_id = int(query['data'].split('_')[1])
    movie_summary = get_movie_details(movie_id)
    poster_url = search_movie_poster(movie_id)
    send_image(poster_url, chat_id)
    adding_buttons(chat_id, movie_id, movie_summary)
    if chat_id == 7653415:
        send_message(f'Here will be link :)', chat_id)


def get_movie_details(movie_id):
    movie = tmdb.Movies(movie_id)
    movie_info = movie.info()

    movie_title = movie_info.get('title', 'N/A')
    movie_year = movie_info.get('release_date', 'N/A')
    movie_rating = movie_info.get('vote_average', 'N/A')
    movie_genres = [genre['name'] for genre in movie_info.get('genres', [])]
    movie_overview = movie_info.get('overview', 'N/A')
    movie_collection = movie_info['belongs_to_collection']['name'] if 'belongs_to_collection' in movie_info and \
                                                                      movie_info['belongs_to_collection'] else "N/A"

    movie_summary = f'''
🎥 🍿 {movie_title} ({movie_year[:4]}) 

⭐ Rating: {movie_rating}\n
🎭 Genres: {", ".join(movie_genres)}\n
🎞 Collection: {movie_collection}\n
💬 Overview: {movie_overview}
    '''
    return movie_summary


def send_movie_details(chat_id, movie_summary):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': movie_summary
    }
    requests.post(url, data=payload)

