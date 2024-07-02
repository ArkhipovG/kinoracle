import keys
import requests
import tmdbsimple as tmdb
import json
from bs4 import BeautifulSoup

tmdb.API_KEY = keys.moviedb_token
tmdb.REQUESTS_TIMEOUT = 5
tmdb.REQUESTS_SESSION = requests.Session()

allowed_list = [7653415, 422308911]
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


def adding_tv_buttons(chat_id, movie_id, movie_summary):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': movie_summary,
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': 'Add to watchlist',
                        'callback_data': f'add_tv_to_watchlist {movie_id}'
                    },
                    {
                        'text': 'Add to favorites',
                        'callback_data': f'add_tv_to_favorites {movie_id}'
                    }
                ],
                [
                    {
                        'text': 'Remove from favorites',
                        'callback_data': f'remove_tv_from_favorites {movie_id}'
                    }
                ],
                [
                    {
                        'text': 'Remove from watchlist',
                        'callback_data': f'remove_tv_from_watchlist {movie_id}'
                    }
                ],
                [
                    {
                        'text': 'Recommendations',
                        'callback_data': f'tv_recommendations {movie_id}'
                    },
                    {
                        'text': 'Release dates',
                        'callback_data': f'release_dates {movie_id}'
                    }
                ]
            ]
        }
    }
    requests.post(url, json=payload)


def adding_tv_buttons_forme(chat_id, movie_id, movie_summary):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': movie_summary,
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': 'Add to watchlist',
                        'callback_data': f'add_tv_to_watchlist {movie_id}'
                    },
                    {
                        'text': 'Add to favorites',
                        'callback_data': f'add_tv_to_favorites {movie_id}'
                    }
                ],
                [
                    {
                        'text': 'Remove from favorites',
                        'callback_data': f'remove_tv_from_favorites {movie_id}'
                    }
                ],
                [
                    {
                        'text': 'Remove from watchlist',
                        'callback_data': f'remove_tv_from_watchlist {movie_id}'
                    }
                ],
                [
                    {
                        'text': 'Recommendations',
                        'callback_data': f'recommendations_tv {movie_id}'
                    },
                    {
                        'text': 'Release dates',
                        'callback_data': f'release_dates {movie_id}'
                    }
                ],
                [
                    {
                        'text': 'Get link',
                        'callback_data': f'link_tv_get_link {movie_id}'
                    }
                ]
            ]
        }
    }
    requests.post(url, json=payload)


# def search_colletion_movies(movie_id):
#     movie = tmdb.Movies(movie_id)
#     movie_info = movie.info()
#     print(movie_info)
#     if movie_info['belongs_to_collection'] == None:
#         return None
#     else:
#         collection_id = movie.belongs_to_collection['id']
#         collection = tmdb.Collections(collection_id)
#         response = collection.info()
#
#         results = [
#             {
#                 'id': result['id'],
#                 'title': result.get('title', 'N/A'),
#                 'release_date': result.get('release_date', 'N/A'),
#                 'overview': result.get('overview', 'N/A')
#             }
#             for result in response['parts']
#         ]
#     return results


# def send_collection_choices(chat_id, movies):
#     keyboard = {
#         'inline_keyboard': [
#             [{'text': f"{movie['title']} ({movie['release_date'][:4] if movie['release_date'] else 'N/A'})",
#               'callback_data': f"movie_{movie['id']}"}] for movie in movies
#         ]
#     }
#     reply_markup = json.dumps(keyboard)
#     message = 'Movies from the collection:'
#
#     url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
#     payload = {
#         'chat_id': chat_id,
#         'text': message,
#         'reply_markup': reply_markup
#     }
#     requests.post(url, data=payload)


def search_tv_poster(movie_id):
    movie = tmdb.TV(movie_id)
    movie_info = movie.info()
    poster_path = movie_info.get('poster_path')
    if poster_path:
        # Construct the full poster URL
        poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
        return poster_url
    return None


def search_tv(query):
    search = tmdb.Search()
    response = search.tv(query=query)

    results = [
        {
            'id': result['id'],
            'title': result.get('name', 'N/A'),
            'release_date': result.get('first_air_date', 'N/A'),
        }
        for result in search.results[:5]  # Limiting to the first 5 results
    ]
    return results


# def search_recommend_movies(movie_id):
#     movie = tmdb.Movies(movie_id)
#     response = movie.recommendations()
#
#     results = [
#         {
#             'id': result['id'],
#             'title': result.get('title', 'N/A'),
#             'release_date': result.get('release_date', 'N/A'),
#
#             'overview': result.get('overview', 'N/A')
#         }
#         for result in response['results'][:5]  # Limiting to the first 5 results
#     ]
#     return results


def send_tv_choices(chat_id, movies):
    keyboard = {
        'inline_keyboard': [
            [{'text': f"{movie['title']} ({movie['release_date'][:4] if movie['release_date'] else 'N/A'})",
              'callback_data': f"tv_{movie['id']}"}] for movie in movies
        ]
    }
    reply_markup = json.dumps(keyboard)
    message = 'Please choose a TV show:'

    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'reply_markup': reply_markup
    }
    requests.post(url, data=payload)


# def send_recommendation_movie_choices(chat_id, movies):
#     keyboard = {
#         'inline_keyboard': [
#             [{'text': f"{movie['title']} ({movie['release_date'][:4] if movie['release_date'] else 'N/A'})",
#               'callback_data': f"movie_{movie['id']}"}] for movie in movies
#         ]
#     }
#     reply_markup = json.dumps(keyboard)
#     message = 'Recommended movies:'
#
#     url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
#     payload = {
#         'chat_id': chat_id,
#         'text': message,
#         'reply_markup': reply_markup
#     }
#     requests.post(url, data=payload)


def handle_tv_callback(query):
    chat_id = query['message']['chat']['id']
    movie_id = int(query['data'].split('_')[1])
    movie_summary = get_tv_details(movie_id)
    poster_url = search_tv_poster(movie_id)
    send_image(poster_url, chat_id)
    if chat_id in allowed_list:
        adding_tv_buttons_forme(chat_id, movie_id, movie_summary)
    else:
        adding_tv_buttons(chat_id, movie_id, movie_summary)


def get_tv_details(movie_id):
    movie = tmdb.TV(movie_id)
    movie_info = movie.info()
    credits = movie.credits()
    cast = credits['cast']
    crew = credits['crew']
    movie_title = movie_info.get('name', 'N/A')
    movie_year = movie_info.get('first_air_date', 'N/A')
    movie_rating = movie_info.get('vote_average', 'N/A')
    movie_genres = [genre['name'] for genre in movie_info.get('genres', [])]
    movie_overview = movie_info.get('overview', 'N/A')
    movie_cast = [actor['name'] for actor in cast]
    movie_directors = [member['name'] for member in crew if member['job'] == 'Director']

    movie_summary = f'''
🎥 🍿 {movie_title} ({movie_year[:4]}) 
🎬 Director: {', '.join(movie_directors)}
⭐ Rating: {movie_rating}\n
🎭 Genres: {", ".join(movie_genres)}\n
💬 Overview: {movie_overview}\n
👥 Cast: {", ".join(movie_cast[:10])}\n
    '''
    return movie_summary


# def send_movie_details(chat_id, movie_summary):
#     url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
#     payload = {
#         'chat_id': chat_id,
#         'text': movie_summary
#     }
#     requests.post(url, data=payload)


def get_kinopoisk_url(movie_id):
    movie = tmdb.TV(movie_id)
    movie_info = movie.info()
    movie_title = movie_info.get('name', 'N/A')
    kinopoisk_search_url = f'https://www.kinopoisk.ru/index.php?kp_query={movie_title}'
    kinopoisk_search_page = requests.get(kinopoisk_search_url)
    print(kinopoisk_search_page.url)
    kinopoisk_soup = BeautifulSoup(kinopoisk_search_page.content, 'html.parser')

    # Проверяем, не является ли текущий URL страницей фильма или перенаправлением
    if 'film' in kinopoisk_search_page.url:
        original_url = kinopoisk_search_page.url
        # Находим начало параметра 'retpath=' и его значение
        start = original_url.find("retpath=") + len("retpath=")
        end = original_url.find("&", start)
        if end == -1:  # Если '&' не найден, это значит, что retpath идет до конца строки
            end = len(original_url)

        # Извлекаем и декодируем значение параметра 'retpath'
        encoded_retpath = original_url[start:end]
        decoded_retpath = encoded_retpath.replace('%3A', ':').replace('%2F', '/')
        modified_url = decoded_retpath.replace('kino', 'ss')
        return modified_url

    # Находим первый результат поиска
    result_div = kinopoisk_soup.find('div', class_='element most_wanted')
    if result_div:
        # Получаем ссылку на страницу фильма на Кинопоиске
        kinopoisk_link = result_div.find('div', class_='info').find('a')['href']
        kinopoisk_full_url = f'https://www.kinopoisk.ru{kinopoisk_link}'
        # Заменяем 'kino' на 'ss' в URL
        modified_url = kinopoisk_full_url.replace('kino', 'ss').replace('/sr/1/', '')
        return modified_url
    else:
        return None

def get_last_season_episode_dates(tv_show_id, chat_id):
    API_KEY = keys.moviedb_token
    BASE_URL = 'https://api.themoviedb.org/3'
    # Получение информации о сезонах
    tv_url = f'{BASE_URL}/tv/{tv_show_id}?api_key={API_KEY}'
    response = requests.get(tv_url).json()
    seasons = response['seasons']

    # Найти последний сезон
    last_season = max(seasons, key=lambda x: x['season_number'])
    if last_season['air_date']:
        last_season_number = last_season['season_number']
    else:
        last_season_number = last_season['season_number'] - 1

    # Получение информации о последнем сезоне
    season_url = f'{BASE_URL}/tv/{tv_show_id}/season/{last_season_number}?api_key={API_KEY}'
    season_details = requests.get(season_url).json()
    episodes = season_details['episodes']

    # Создание словаря для хранения дат выхода серий последнего сезона
    episode_dates = {}

    for episode in episodes:
        episode_number = episode['episode_number']
        air_date = episode['air_date']
        episode_dates[f'Season {last_season_number} Episode {episode_number}'] = air_date

    release_dates = ""

    for episode, date in episode_dates.items():
        release_dates += f"{episode}: {date}\n"

    send_message(release_dates, chat_id)
