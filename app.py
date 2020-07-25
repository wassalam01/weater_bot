from flask import Flask
from flask import request
from flask import render_template
import requests
import os, json

# import telebot
# bot = telebot.TeleBot("TOKEN", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
# bot.send_message()

app = Flask(__name__)
app.debug = True

TOKEN = os.getenv('TELEGRAM_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
base_url = f'https://api.telegram.org/bot{TOKEN}/'
weather_url = f'http://api.openweathermap.org/data/2.5/weather?id=468902&appid={WEATHER_TOKEN}&units=metric'
# weather_url = f'http://api.openweathermap.org/data/2.5/weather?id=468902&appid={WEATHER_TOKEN}&units=metric'


def not_support(response):
    chat_id = response['message']['chat']['id']
    template = render_template('start.html', text='Данная функция не поддерживается')
    requests.post(f'{base_url}sendMessage?chat_id={chat_id}&text={template}&parse_mode=html')


def send_start_message(response):
    chat_id = response['message']['chat']['id']
    template = render_template('start.html', text='Start template')
    requests.post(f'{base_url}sendMessage?chat_id={chat_id}&text={template}&parse_mode=html')


def send_weather(response):
    chat_id = response['message']['chat']['id']
    weather_response = json.loads(requests.get(weather_url).text)
    print(type(weather_response))
    print(weather_response['main']['temp'])
    print(weather_response['main']['feels_like'])
    print(weather_response['wind']['speed'])
    template = render_template('current_weather.html',
                               temp=weather_response['main']['temp'],
                               feels_like=weather_response['main']['feels_like'],
                               wind_speed=weather_response['wind']['speed'])

    requests.post(f'{base_url}sendMessage?chat_id={chat_id}&text={template}&parse_mode=html')


def check_response(response):
    print(response)
    text_form_response = response['message']['text']
    if '/' in text_form_response:
        if '/start' == str(text_form_response).lower() \
                or '/help' == str(text_form_response).lower():
            send_start_message(response)
        else:
            not_support(response)
    elif '!' in text_form_response:
        send_weather(response)
    else:
        not_support(response)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        response = request.json
        check_response(response)
        return 'Hello'
    else:
        return 'Hello World!'


if __name__ == '__main__':
    app.run()
