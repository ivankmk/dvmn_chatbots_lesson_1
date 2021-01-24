## Telegram chat-bot for checking the readyness of the tasks from [devman.org](https://dvmn.org/)


### What do you need to use the bot: 

- Account on [devman.org](https://dvmn.org/) and [api](https://dvmn.org/api/docs/)
- To register the bot [here](https://telegram.me/BotFather) and take his ID

### Installation:

```
git clone https://github.com/ivankmk/dvmn_chatbots_lesson_1
```
- Use environment variables to store sensetive data
```
DEVMAN_TOKEN='devman_example_token'
TELEGRAM_TOKEN='tg_example_token'
TELEGRAM_CHAT_ID='chat_id'
```
*To get the TELEGRAM_CHAT_ID, please message to @userinfobot.*

- Install dependencies (preferably using virtual environment)
```
pip install -r requirements.txt
```
- Run the script by:
```
python3 main.py
```

Done!