import requests
import telegram
from dotenv import load_dotenv
import logging
import os
import time


def send_message(token, chat_id, text):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=text)


def send_tg_notification(url):
    logging.info('Bot is running.')
    tg_token = os.environ.get('TG_TOKEN')
    tg_chat_id = os.environ.get('TG_CHAT_ID')
    token = {'Authorization': os.environ.get('DVMN_TOKEN')}
    params = ''
    while True:
        try:
            response = requests.get(
                url,
                headers=token,
                params=params,
                timeout=90
            )
            response.raise_for_status()
            task_check_result = response.json()

            if task_check_result['status'] == 'timeout':
                timestamp = task_check_result['timestamp_to_request']
                params = {'timestamp': timestamp}
            else:
                lesson_details = task_check_result['new_attempts'][0]
                task_name = lesson_details['lesson_title']
                is_negative = lesson_details['is_negative']
                if is_negative:
                    send_message(tg_token,
                                 tg_chat_id,
                                 f"У вас проверили работу '{task_name}'. \
                                  К сожалению нашлись ошибки :-(")
                else:
                    send_message(tg_token,
                                 tg_chat_id,
                                 f"У вас проверили работу '{task_name}'. \
                                Все ок - можно приступать к следующему :-)")

        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(90)
            continue


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    load_dotenv()
    url = 'https://dvmn.org/api/long_polling/'
    send_tg_notification(url)
