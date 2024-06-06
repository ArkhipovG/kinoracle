# Configure your environment variables (replace placeholders)
import requests
import boto3
import keys
from datetime import datetime

REGION_NAME = 'us-east-1'  # Change this to your desired region

dynamodb = boto3.client('dynamodb', region_name=REGION_NAME)


def send_message(message, chat_id):
    url = f'https://api.telegram.org/bot{keys.telegram_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    r = requests.post(url, json=payload)


def get_movie_details(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={keys.moviedb_token}'
    response = requests.get(url)
    return response.json()


def add_favorite(chat_id, movie_id):
    """Adds a movie/TV show to a user's favorites list"""
    user_id = chat_id
    movie_details = get_movie_details(movie_id)

    try:
        dynamodb.put_item(
            TableName='UserFavorites',
            Item={
                'userId': {'N': str(user_id)},
                'movieId': {'N': movie_id},
                'movieTitle': {'S': movie_details.get('title')},
                'addedDate': {'S': str(datetime.now().strftime('%d/%m/%Y'))}
            }
        )
        send_message(f"Movie '{movie_details.get('title')}' added to favorites.", chat_id)
    except Exception as e:
        send_message(f"Error adding favorite: {str(e)}", chat_id)


def remove_favorite(chat_id, movie_id):
    """Removes a movie/TV show from a user's favorites list"""
    user_id = chat_id
    movie_details = get_movie_details(movie_id)

    try:
        dynamodb.delete_item(
            TableName='UserFavorites',
            Key={
                'userId': {'N': str(user_id)},
                'movieId': {'N': movie_id}
            }
        )
        send_message(f"Movie '{movie_details.get('title')}' removed from favorites.", chat_id)
    except Exception as e:
        send_message(f"Error removing favorite: {str(e)}", chat_id)


def get_favorites(chat_id):
    response = dynamodb.query(
        TableName='UserFavorites',
        KeyConditionExpression='userId = :uid',
        ExpressionAttributeValues={
            ':uid': {'N': str(chat_id)}
        }
    )
    favorites = response.get('Items', [])
    if favorites:
        favorites_string = "Your favorite movies:\n"
        if 'Items' in response and response['Items']:
            for i, item in enumerate(response['Items'], start=1):
                movie_title = item['movieTitle']['S']
                movie_id = item['movieId']['N']
                favorites_string += f"{i}. '{movie_title}' (ID: {movie_id})\n"
        else:
            favorites_string += "You have no favorite movies yet."
        send_message(favorites_string, chat_id, )
    else:
        send_message("You have no favorite movies.", chat_id, )


def add_favorite_prompt(chat_id):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': "Please reply with the movie ID to add to your favorites:",
        'reply_markup': {
            'force_reply': True
        }
    }
    r = requests.post(url, json=payload)


def remove_favorite_prompt(chat_id):
    url = f"https://api.telegram.org/bot{keys.telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': "Please reply with the movie ID to remove it from your favorites:",
        'reply_markup': {
            'force_reply': True
        }
    }
    r = requests.post(url, json=payload)