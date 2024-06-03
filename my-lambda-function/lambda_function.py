import json
import requests
import keys
from random import choice
from quiz import quiz_functions
from search import searching_functions

search_state = {}
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


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        message = body.get('message')

        if message and 'text' in message:
            chat_id = message['chat']['id']
            text = message['text']

            if text == '/start':
                welcome_message = """
                👋 Hi there! Welcome to Kinoracle 🎬

I'm here to help you find the perfect movie or series to watch. Here's what I can do for you:

🎥 Recommendations: Suggest what to watch tonight.
⭐ Ratings: Show you the top movies and series across various categories.
🧩 Quizzes: Test your movie knowledge by guessing movies from stills or descriptions.
📂 Lists: Create and manage your own lists of favorite movies or those you want to watch in the future.

Use /help for a list of commands.
                """
                send_message(welcome_message, chat_id)
            elif text == '/help':
                help_message = "Commands you can use: \n/start - Welcome message \n/help - List of commands \n/quiz - Start a quiz"
                send_message(help_message, chat_id)
            elif text == '/quiz':
                quiz_functions.start_quiz(chat_id)
            elif text == '/search_movie':
                send_message("What movie would you like to find? Please enter the movie name.", chat_id)
                search_state[chat_id] = True
            else:
                if chat_id in quiz_functions.user_state:
                    quiz_functions.check_answer(chat_id, text)
                elif chat_id in search_state:
                    poster_url = searching_functions.search_movie_poster(text)
                    movie_summary = searching_functions.search_movie_info(text)
                    if poster_url:
                        send_image(poster_url, chat_id)
                        send_message(movie_summary, chat_id)
                    else:
                        send_message("Sorry, I couldn't find information for that movie.", chat_id)
                    del search_state[chat_id]  # Clear the state after processing
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
