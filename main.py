import telebot
import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()  

telegram_token = os.getenv('TELEGRAM_TOKEN')
api_key = os.getenv('WEATHER_API_KEY')
  
bot = telebot.TeleBot(telegram_token) 
WEATHER_API_KEY = api_key 


@bot.message_handler(commands=['start'])
def start(message): 
  bot.send_message(message.chat.id, 'Hello! Please enter a city name.')
  
  
  
@bot.message_handler(content_types=['text'])
def get_weather(message): 
    city = message.text.strip()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        bot.reply_to(message, f'Weather: {data["main"]["temp"]}°C')

        icon = data["weather"][0]["icon"]
        image = f'http://openweathermap.org/img/wn/{icon}@2x.png'
        bot.send_photo(message.chat.id, image)
    else: 
        bot.reply_to(message, 'Sorry, I couldn`t find that city. Please check the spelling and try again.')

  
bot.polling(none_stop=True)