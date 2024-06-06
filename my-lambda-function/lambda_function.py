import json
import requests
import keys
from quiz import quiz_functions
from quiz import picture_quiz_functions
from search import searching_functions
from favorites import favorites_functions
from watchlist import watchlist_functions
from gemini_api import recommend
search_state = {}


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
                ]
            ]
        }
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

            if data.startswith('add_to_watchlist'):
                movie_id = data.split(' ')[1]
                watchlist_functions.add_to_watchlist(chat_id, movie_id)
            elif data.startswith('add_to_favorites'):
                movie_id = data.split(' ')[1]
                favorites_functions.add_favorite(chat_id, movie_id)
            elif data == 'more_movies':
                recommend.more_recommend_movie(chat_id)

            answer_callback_query(callback_query['id'])
        elif 'message' in body:
            text = body['message']['text']
            message = body.get('message')
            chat_id = message['chat']['id']
            if 'reply_to_message' in body['message']:
                # Handle the reply to the force reply message
                if message['reply_to_message']['text'] == "Please reply with the movie ID to add to your watchlist:":
                    movie_id = text.strip()
                    watchlist_functions.add_to_watchlist(chat_id, movie_id)
                elif message['reply_to_message']['text'] == "Please reply with the movie ID to remove it from your watchlist:":
                    movie_id = text.strip()
                    watchlist_functions.remove_from_watchlist(chat_id, movie_id)
                elif message['reply_to_message']['text'] == "Please reply with the movie ID to add to your favorites:":
                    movie_id = text.strip()
                    favorites_functions.add_favorite(chat_id, movie_id)
                elif message['reply_to_message']['text'] == "Please reply with the movie ID to remove it from your favorites:":
                    movie_id = text.strip()
                    favorites_functions.remove_favorite(chat_id, movie_id)
                elif message['reply_to_message']['text'].startswith("Please tell me more about what you'd like to watch!"):
                    recommend.recommend_movie(text, chat_id)
                # elif message['reply_to_message']['text'].startswith("If you already seen these movies"):
                #     recommend.more_recommend_movie(chat_id)
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
📂 <b>Lists</b>: Create and manage your own lists of favorite movies or those you want to watch in the future.
        
    Use /help for a list of commands.
                        """
                        send_message(welcome_message, chat_id)
                    elif text == '/help':
                        help_message = ("Commands you can use: \n/start - Welcome message "
                                        "\n/help - List of commands "
                                        "\n/search_movie - Find summary about a movie "
                                        "\n/recommend - Get personalized movie suggestions"
                                        "\n/quizzes - Guess the movie by description "
                                        "\n/favorites - List of your favorite movies"
                                        "\n/watchlist - List of movies you want to watch in the future "
                                        "\n/manage_lists - Manage lists commands")
                        send_message(help_message, chat_id)
                    elif text == '/manage_lists':
                        help_message = ("Commands you can use to manage your lists: "
                                        "\n/add_favorite - Add to favorites"
                                        "\n/remove_favorite - Remove from favorites"
                                        "\n/add_to_watchlist - Add to watchlist"
                                        "\n/remove_from_watchlist - Remove from watchlist")
                        send_message(help_message, chat_id)
                    elif text == '/quizzes':
                        quizzes_message = ("Test your movie knowledge: "
                                        "\n/picture_quiz - Guess the movie by picture "
                                        "\n/quiz - Guess the movie by description ")
                        send_message(quizzes_message, chat_id)
                    elif text == '/recommend':
                        recommend.recommend_message(chat_id)
                    elif text == '/quiz':
                        quiz_functions.start_quiz(chat_id)
                    elif text == '/picture_quiz':
                        picture_quiz_functions.start_banner_quiz(chat_id)
                    elif text == '/search_movie':
                        send_message("What movie would you like to find? Please enter the movie name.", chat_id)
                        search_state[chat_id] = True
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
                    elif text == '/favorites':
                        favorites_functions.get_favorites(chat_id)
                    # elif text == '/remove_keyboard':
                    #     remove_custom_keyboard(chat_id)
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
                        elif chat_id in search_state:
                            poster_url = searching_functions.search_movie_poster(text)
                            movie_summary, movie_id = searching_functions.search_movie_info(text)
                            if poster_url:
                                send_image(poster_url, chat_id)
                                adding_buttons(chat_id, movie_id, movie_summary)
                            else:
                                send_message("Sorry, I couldn't find information for that movie.", chat_id)
                            del search_state[chat_id]
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
