import json
import requests
import keys
from quiz import quiz_functions
from quiz import picture_quiz_functions
from search import searching_functions, searching_tv_functions
from favorites import favorites_functions
from watchlist import watchlist_functions
from gemini_api import recommend
from lists import lists_functions, lists_tv_functions

search_movie_state = {}
search_tv_state = {}


def send_message(message, chat_id):
    url = f'https://api.telegram.org/bot{keys.telegram_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }

    r = requests.post(url, json=payload)


def send_image(image_url, chat_id):
    url = f'https://api.telegram.org/bot{keys.telegram_token}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': image_url
    }

    r = requests.post(url, json=payload)


def send_message_with_keyboard(message, chat_id):
    keyboard = {
        'keyboard': [
            [{'text': '🗂 Lists'}, {'text': '🤖 Recommendations'}],
            [{'text': '🔍 Search Movies'}, {'text': '🔍 Search TV Shows'}],
            [{'text': '📊 Dashboard'}, {'text': '🧩 Quizzes'}]
        ],
        'resize_keyboard': True
    }
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'reply_markup': json.dumps(keyboard)
    }
    requests.post(url, json=payload)


def disable_keyboard(chat_id):
    keyboard = {'remove_keyboard': True}
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': "Keyboard disabled.",
        'reply_markup': json.dumps(keyboard)
    }
    requests.post(url, json=payload)


def answer_callback_query(callback_query_id):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/answerCallbackQuery"
    payload = {
        'callback_query_id': callback_query_id
    }
    requests.post(url, json=payload)


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        if 'callback_query' in body:
            callback_query = body['callback_query']
            chat_id = callback_query['message']['chat']['id']
            data = callback_query['data']
            #send_message(body, chat_id)

            if data.startswith('add_to_watchlist'):
                movie_id = data.split(' ')[1]
                watchlist_functions.add_to_watchlist(chat_id, movie_id)
            elif data.startswith('add_to_favorites'):
                movie_id = data.split(' ')[1]
                favorites_functions.add_favorite(chat_id, movie_id)
            elif data.startswith('remove_from_favorites'):
                movie_id = data.split(' ')[1]
                favorites_functions.remove_favorite(chat_id, movie_id)
            elif data.startswith('remove_from_watchlist'):
                movie_id = data.split(' ')[1]
                watchlist_functions.remove_from_watchlist(chat_id, movie_id)
            elif data.startswith('collection '):
                movie_id = int(data.split(' ')[1])
                collection_movies = searching_functions.search_colletion_movies(movie_id)
                if collection_movies:
                    searching_functions.send_collection_choices(chat_id, collection_movies)
                else:
                    send_message("This movie has no collection", chat_id)
            elif data.startswith('recommendations '):
                movie_id = int(data.split(' ')[1])
                movies = searching_functions.search_recommend_movies(movie_id)
                if movies:
                    searching_functions.send_recommendation_movie_choices(chat_id, movies)
                else:
                    send_message("Sorry, I couldn't find recommendations", chat_id)
            elif data.startswith('get_link'):
                movie_id = int(data.split(' ')[1])
                watch_link = searching_functions.get_kinopoisk_url(movie_id)
                if watch_link:
                    send_message(watch_link, chat_id)
                else:
                    send_message("Sorry, I cant find the link", chat_id)
            elif data == 'more_movies':
                recommend.more_recommend_movie(chat_id)
            elif data.startswith('movie_'):
                searching_functions.handle_movie_callback(callback_query)
            elif data.startswith('tv_'):
                searching_tv_functions.handle_tv_callback(callback_query)
            elif data == "show_favorites":
                favorites_functions.get_favorites2(chat_id)
            elif data == "show_watchlist":
                watchlist_functions.get_watchlist2(chat_id)
            elif data == "popular_list":
                lists_functions.get_popular_list(chat_id)
            elif data == "upcoming_list":
                lists_functions.get_upcoming_list(chat_id)
            elif data == "popular_tv_list":
                lists_tv_functions.get_popular_tv_list(chat_id)
            elif data == "airing_list":
                lists_tv_functions.get_on_the_air_list(chat_id)
            elif data == "picture_quiz":
                picture_quiz_functions.start_banner_quiz(chat_id)
            elif data == "description_quiz":
                quiz_functions.start_quiz(chat_id)
            elif data == "pop_picture_quiz":
                picture_quiz_functions.start_pop_banner_quiz(chat_id)
            elif data == "pop_description_quiz":
                quiz_functions.start_pop_quiz(chat_id)
            elif data == "top_rated_quiz":
                quiz_functions.quiz_buttons(chat_id)
            elif data == "top_popular_quiz":
                quiz_functions.quiz_pop_buttons(chat_id)
            elif data.startswith("release_dates"):
                movie_id = int(data.split(' ')[1])
                searching_tv_functions.get_last_season_episode_dates(movie_id, chat_id)
            elif data.startswith('link_tv_get_link'):
                movie_id = int(data.split(' ')[1])
                watch_link = searching_tv_functions.get_kinopoisk_url(movie_id)
                if watch_link:
                    send_message(watch_link, chat_id)
                else:
                    send_message("Sorry, I cant find the link", chat_id)

            answer_callback_query(callback_query['id'])
        elif 'message' in body:
            text = body['message']['text']
            message = body.get('message')
            chat_id = message['chat']['id']
            #send_message(body, chat_id)
            if 'reply_to_message' in body['message']:
                # Handle the reply to the force reply message
                if message['reply_to_message']['text'] == "Please reply with the movie ID to add to your watchlist:":
                    movie_id = text.strip()
                    watchlist_functions.add_to_watchlist(chat_id, movie_id)
                elif message['reply_to_message'][
                    'text'] == "Please reply with the movie ID to remove it from your watchlist:":
                    movie_id = text.strip()
                    watchlist_functions.remove_from_watchlist(chat_id, movie_id)
                elif message['reply_to_message']['text'] == "Please reply with the movie ID to add to your favorites:":
                    movie_id = text.strip()
                    favorites_functions.add_favorite(chat_id, movie_id)
                elif message['reply_to_message'][
                    'text'] == "Please reply with the movie ID to remove it from your favorites:":
                    movie_id = text.strip()
                    favorites_functions.remove_favorite(chat_id, movie_id)
                elif message['reply_to_message']['text'].startswith(
                        "Please tell me more about what you'd like to watch!"):
                    recommend.recommend_movie(text, chat_id)
            else:
                if message and 'text' in message:
                    chat_id = message['chat']['id']
                    text = message['text']

                    if text == '/start':
                        welcome_message = """
                        👋 Hi there! Welcome to <b>KinOracle</b> 🎬

I'm here to help you find the perfect movie or series to watch. Here's what I can do for you:

🎥 <b>Recommendations</b>: Suggest what to watch tonight.
⭐ <b>Ratings</b>: Show you the top movies and series across various categories.
🧩 <b>Quizzes</b>: Test your movie knowledge by guessing movies from banners or descriptions.
🗂 <b>Lists</b>: Create and manage your own lists of favorite movies or those you want to watch in the future.
📊 <b>Dashboard</b>: <a href="https://public.tableau.com/app/profile/gregory.arkhipov/viz/MoviesDashboardPublic/MoviesDashboard">Interactive Dashboard</a> for searching movies.

Use /help for a list of commands.
                        """

                        send_message(welcome_message, chat_id)
                    elif text == '/help':
                        help_message = ("Commands you can use: \n/start - Welcome message\n"
                                        "\n🗂 Lists \nDifferent Lists of movies and TV shows\n"
                                        "\n🤖 Recommendations \nGet personalized movie suggestions\n"
                                        "\n🔍 Search Movies/TV Shows \nFind summary about a movie or TV show\n"
                                        "\n📊 Dashboard \nInteractive dashboard\n"
                                        "\n🧩 Quizzes \nGuess the movie by description\n"
                                        )
                        send_message_with_keyboard(help_message, chat_id)
                    elif text == '/manage_lists':
                        help_message = ("Commands you can use to manage your lists: "
                                        "\n/add_favorite - Add to favorites"
                                        "\n/remove_favorite - Remove from favorites"
                                        "\n/add_to_watchlist - Add to watchlist"
                                        "\n/remove_from_watchlist - Remove from watchlist")
                        send_message(help_message, chat_id)
                    elif text == '🧩 Quizzes':
                        quiz_functions.type_quiz_buttons(chat_id)
                    elif text == '🤖 Recommendations':
                        recommend.recommend_message(chat_id)
                    elif text == '🗂 Lists':
                        lists_functions.list_buttons(chat_id)
                    elif text == '📊 Dashboard':
                        dashboard_message = '<a href="https://public.tableau.com/app/profile/gregory.arkhipov/viz/MoviesDashboardPublic/MoviesDashboard">Interactive Dashboard</a>'
                        send_message(dashboard_message, chat_id)
                    elif text == '/keyboard':
                        disable_keyboard(chat_id)
                    elif text == '🔍 Search Movies':
                        send_message("What movie would you like to find? Please enter the name.", chat_id)
                        search_movie_state[chat_id] = True
                    elif text == '🔍 Search TV Shows':
                        send_message("What TV show would you like to find? Please enter the name.", chat_id)
                        search_tv_state[chat_id] = True
                    elif text.startswith('/add_favorite'):
                        if text == '/add_favorite':
                            favorites_functions.add_favorite_prompt(chat_id)
                        else:
                            movie_id = text.split(' ')[1]
                            favorites_functions.add_favorite(chat_id, movie_id)
                    elif text.startswith("/remove_favorite"):
                        if text == '/remove_favorite':
                            favorites_functions.remove_favorite_prompt(chat_id)
                        else:
                            movie_id = text.split(' ')[1]
                            favorites_functions.remove_favorite(chat_id, movie_id)
                    elif text.startswith('/add_to_watchlist'):
                        if text == '/add_to_watchlist':
                            watchlist_functions.add_to_watchlist_prompt(chat_id)
                        else:
                            movie_id = text.split(' ')[1]
                            watchlist_functions.add_to_watchlist(chat_id, movie_id)
                    elif text.startswith("/remove_from_watchlist"):
                        if text == '/remove_from_watchlist':
                            watchlist_functions.remove_from_watchlist_prompt(chat_id)
                        else:
                            movie_id = text.split(' ')[1]
                            watchlist_functions.remove_from_watchlist(chat_id, movie_id)
                    elif text == '/watchlist':
                        watchlist_functions.get_watchlist(chat_id)
                    else:
                        if chat_id in quiz_functions.user_state:
                            quiz_functions.check_answer(chat_id, text)
                        elif chat_id in picture_quiz_functions.user_state:
                            picture_quiz_functions.check_user_state(chat_id, text)
                        elif chat_id in search_movie_state:
                            movies = searching_functions.search_movies(text)
                            if movies:
                                searching_functions.send_movie_choices(chat_id, movies)
                            else:
                                send_message("Sorry, I couldn't find information.", chat_id)
                            del search_movie_state[chat_id]
                        elif chat_id in search_tv_state:
                            movies = searching_tv_functions.search_tv(text)
                            if movies:
                                searching_tv_functions.send_tv_choices(chat_id, movies)
                            else:
                                send_message("Sorry, I couldn't find information.", chat_id)
                            del search_tv_state[chat_id]
                        else:
                            unknown_command_message = "Sorry, I don't understand this command. Use /help for a list of commands."
                            send_message(unknown_command_message, chat_id)
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'ok'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
