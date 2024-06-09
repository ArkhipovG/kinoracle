from random import choice
import keys
import requests
import tmdbsimple as tmdb
import random
tmdb.API_KEY = keys.moviedb_token
tmdb.REQUESTS_TIMEOUT = 5
tmdb.REQUESTS_SESSION = requests.Session()

movies_ids = [278,
 238,
 240,
 424,
 389,
 19404,
 129,
 155,
 496243,
 497,
 372058,
 680,
 122,
 13,
 429,
 769,
 12477,
 346,
 11216,
 637,
 550,
 1058694,
 667257,
 372754,
 157336,
 539,
 598,
 255709,
 696374,
 311,
 510,
 120,
 704264,
 4935,
 324857,
 724089,
 40096,
 121,
 620249,
 1891,
 568332,
 14537,
 761053,
 423,
 1160164,
 378064,
 244786,
 807,
 27205,
 569094,
 567,
 274,
 73,
 820067,
 128,
 1139087,
 92321,
 914,
 644479,
 105,
 12493,
 207,
 18491,
 599,
 101,
 10494,
 3782,
 3082,
 335,
 28,
 901,
 29259,
 77338,
 995133,
 447362,
 1585,
 975,
 652837,
 527641,
 637920,
 632632,
 10376,
 8587,
 670,
 25237,
 533514,
 299534,
 283566,
 630566,
 508965,
 299536,
 490132,
 618344,
 315162,
 265177,
 42269,
 572154,
 635302,
 110420,
 504253]

def generate_questions():
    questions = []
    for i in range(5):
        movie = tmdb.Movies(random.choice(movies_ids))
        response = movie.info()
        question = response['overview']
        title = response['title']
        questions.append({'question': question, 'answer': title})
    return questions

user_state = {}

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
    quiz_buttons2(response_message, chat_id)


def quiz_buttons(chat_id):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': "🧠 Test your movie knowledge! 🧠",
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': 'Picture quiz',
                        'callback_data': f'picture_quiz'
                    }
                ],
                [
                    {
                        'text': 'Description quiz',
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
                        'text': 'Picture quiz',
                        'callback_data': f'picture_quiz'
                    }
                ],
                [
                    {
                        'text': 'Description quiz',
                        'callback_data': f'description_quiz'
                    }
                ]
            ]
        }
    }
    requests.post(url, json=payload)