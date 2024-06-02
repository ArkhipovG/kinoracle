import telebot
import openai
import random
import requests
import keys

bot = telebot.TeleBot(keys.telegram_token)

openai.api_key = keys.openai_api_key

