import telebot
import openai
import random
import requests

import keys
from open_ai import ai_functions

bot = telebot.TeleBot(keys.telegram_token)

openai.api_key = keys.openai_api_key

