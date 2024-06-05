from random import choice
import keys
import requests
import tmdbsimple as tmdb
import random
tmdb.API_KEY = keys.moviedb_token
tmdb.REQUESTS_TIMEOUT = 5
tmdb.REQUESTS_SESSION = requests.Session()
import urllib.parse
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


def search_movie_poster(query):
    # Replace 'YOUR_TMDB_API_KEY' with your actual TMDb API key
    tmdb.API_KEY = keys.moviedb_token
    search = tmdb.Search()
    response = search.movie(query=query)
    if search.results:
        # Get the first result
        movie_id = search.results[0]['id']
        movie = tmdb.Movies(movie_id)
        movie_info = movie.info()
        poster_path = movie_info.get('poster_path')
        if poster_path:
            # Construct the full poster URL
            poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
            return poster_url
    return None

def search_movie_info(query):
    tmdb.API_KEY = keys.moviedb_token
    search = tmdb.Search()
    response = search.movie(query=query)
    if search.results:
        # Get the first result
        movie_id = search.results[0]['id']
        movie = tmdb.Movies(movie_id)
        movie_info = movie.info()
        movie_overview = movie_info.get('overview')
        movie_title = movie_info.get('title')
        movie_year = movie_info.get('release_date')
        movie_rating = movie_info.get('vote_average')
        movie_genres = [genre['name'] for genre in movie_info['genres']]
    movie_summary = f'''
Title: {movie_title}     ID: {movie_id}\n
Year: {movie_year}\n
Rating: {movie_rating}\n
Genres: {", ".join(movie_genres)}\n
Overview: {movie_overview}\n
    '''
    return movie_summary, movie_id

