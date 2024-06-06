import keys
import json
import requests
import re

user_recommendations = {}
user_prompt = {}
def send_message(message, chat_id):
    url = f'https://api.telegram.org/bot{keys.telegram_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }

    r = requests.post(url, json=payload)

def send_reply_message(message, chat_id):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'force_reply': True
        }
    }
    r = requests.post(url, json=payload)


def clean_markdown(text):
    # Remove headers
    # Remove bold asterisks
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Remove italic asterisks
    text = re.sub(r'\*(.*?)\*', r'\1', text)

    return text

def send_message_more_button(text_message, chat_id):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text_message,
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': 'More',
                        'callback_data': 'more_movies'
                    }
                ]
            ]
        }
    }
    requests.post(url, json=payload)


def get_gemini_response(prompt, chat_id):
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    params = {
        "key": keys.google_api_key
    }

    response = requests.post(url, headers=headers, params=params, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            answer = response_json["candidates"][0]["content"]["parts"][0]["text"]
            cleaned_answer = clean_markdown(answer)
            return cleaned_answer
        else:
            send_message("No content generated.", chat_id)
    else:
        send_message('"error": response.status_code, "message": response.text}', chat_id)



def recommend_message(chat_id):
    recommend_message = '''
Please tell me more about what you'd like to watch! To give you the best recommendations, I need some information about your preferences.
For example, tell me:

1. <b>Genre Preferences</b>: What genres do you enjoy? (e.g., action, comedy, drama, horror, science fiction, fantasy, romance, thriller, etc.)
2. <b>Mood or Theme</b>: What kind of mood or theme are you in? (e.g., uplifting, dark, funny, inspirational, intense, etc.)
3. <b>Language Preferences</b>: Do you prefer content in specific languages or are you open to any language?
4. <b>Age Rating</b>: Are there any age rating preferences or restrictions? (e.g., G, PG, PG-13, R, etc.)
5. <b>Favorite Movies/TV Shows</b>: Can you list some of your favorite movies or TV shows? This helps in understanding your taste better.
6. <b>Recent Watches</b>: What have you watched recently and did you enjoy it?
7. <b>Duration Preferences</b>: Do you prefer movies, short TV shows, or longer series?
8. <b>Release Date Preferences</b>: Are you looking for something new or are you open to older content as well?
9. <b>Specific Preferences</b>: Any specific actors, directors, or franchises you prefer?

The more information you give me, the better I can understand your preferences and recommend something you'll truly enjoy.

Reply to this message.    
    '''
    send_reply_message(recommend_message, chat_id)

def recommend_movie(prompt, chat_id):
    user_prompt[chat_id] = prompt
    prompt_message = f"""
You are part of the chatbot which recommends to the user movies or TV shows to watch. 
User will give you some information and you must recommend something he will truly enjoy. 
You must only give recommendations. Dont ask any questions.
Information from the user:
{prompt}
"""
    recommendations = get_gemini_response(prompt_message, chat_id)
    send_message_more_button(recommendations, chat_id)
    user_recommendations[chat_id] = recommendations

def more_recommend_movie(chat_id):
    prompt_message = f"""
    You are part of the chatbot which recommends to the user movies or TV shows to watch. 
    User will give you some information and you must recommend something he will truly enjoy. 
    You must only give recommendations. Dont ask any questions.
    Information from the user:
    {user_prompt[chat_id]}
    I already saw these movies:
    {user_recommendations[chat_id]}
    """

    user_prompt[chat_id] = prompt_message

    recommendations = get_gemini_response(prompt_message, chat_id)
    send_message_more_button(recommendations, chat_id)
    user_recommendations[chat_id] = recommendations



