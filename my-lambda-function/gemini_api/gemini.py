import requests
import json
import re
import keys


def send_message(message, chat_id):
    url = f'https://api.telegram.org/bot{keys.telegram_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    r = requests.post(url, json=payload)


def get_gemini_response(prompt, chat_id):
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f'{prompt}'}
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
            send_message(cleaned_answer, chat_id)
        else:
            send_message("No content generated.", chat_id)
    else:
        send_message('"error": response.status_code, "message": response.text}', chat_id)


def clean_markdown(text):
    # Remove headers
    # Remove bold asterisks
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Remove italic asterisks
    text = re.sub(r'\*(.*?)\*', r'\1', text)

    return text


get_gemini_response("What would you recommend me to watch?", chat_id=7653415)