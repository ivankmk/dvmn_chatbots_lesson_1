import requests
import telegram
from dotenv import load_dotenv
import logging
import os
import time

logger = logging.getLogger(__name__)


class MyLogsHandler(logging.Handler):

    def emit(self, record):
        log_entry = self.format(record)
        bot_logger.send_message(chat_id=tg_chat_id, text=log_entry)


def send_tg_notification(url, chat_id):
    logger.info('Bot is running.')
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
                    bot.send_message(
                        tg_chat_id,
                        f"У вас проверили работу '{task_name}'. \
                        К сожалению нашлись ошибки :-(")
                else:
                    bot.send_message(
                        tg_chat_id,
                        f"У вас проверили работу '{task_name}'. \
                        Все ок - можно приступать к следующему :-)")

        except (requests.exceptions.ReadTimeout, telegram.error.TimedOut) as e:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(90)
            continue
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":

    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())

    load_dotenv()
    tg_token = os.environ.get('TG_TOKEN')
    tg_chat_id = os.environ.get('TG_CHAT_ID')
    bot = telegram.Bot(token=tg_token)
    bot_logger = telegram.Bot(token=tg_token)

    url = 'https://dvmn.org/api/long_polling/'

    send_tg_notification(url, tg_chat_id)
