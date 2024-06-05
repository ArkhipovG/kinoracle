import requests
import json

import keys
my_id = 7653415
api_key = keys.google_api_key
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
             send_message(answer, chat_id)
        else:
            send_message("No content generated.", chat_id)
    else:
        send_message('"error": response.status_code, "message": response.text}', chat_id)



#get_gemini_response('hi there', my_id)

