import telebot
import requests

bot_token = 'TOKEN'
api_url = 'http://api.geonames.org/searchJSON?country=RU&name='
username = 'GeoNames'

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для получения численности населения городов России. Просто отправь мне название города.")

@bot.message_handler(func=lambda message: True)
def get_population(message):
    city = message.text
    population = get_city_population(city)
    if population is None:
        bot.reply_to(message, "Не удалось получить информацию о численности населения для этого города.")
    else:
        bot.reply_to(message, f"Численность населения города {city}: {population}")

def get_city_population(city):
    try:
        response = requests.get(f"{api_url}{city}&username={username}")
        data = response.json()
        population = data['geonames'][0]['population']
        return population
    except:
        return None

bot.polling()