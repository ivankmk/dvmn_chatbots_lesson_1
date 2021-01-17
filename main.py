import requests
import telegram
import json
from dotenv import load_dotenv
import os

load_dotenv()

def send_message(token, chat_id, text):

    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=text)

def bot_watcher(url):
    tg_token = os.environ.get('TG_TOKEN')
    tg_chat_id = os.environ.get('TG_CHAT_ID')
    token = {
    'Authorization': os.environ.get('DVMN_TOKEN')
    }    
    while True:
        try:
            response = requests.get(url, headers=token, timeout=5)
            response_json = json.loads(response.text)
            task_name = response_json['new_attempts'][0]['lesson_title']
            is_negative = response_json['new_attempts'][0]['is_negative']
            if is_negative:
                send_message(tg_token,
                            tg_chat_id,
                            f"У вас проверили работу '{task_name}'. К сожалению нашлись ошибки :-(")
            else:
                send_message(tg_token,
                            tg_chat_id,
                            f"У вас проверили работу '{task_name}'. Все ок - можно приступать к следующему :-)")
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            continue

if __name__ == "__main__":
    url = 'https://dvmn.org/api/long_polling/'
    bot_watcher(url)