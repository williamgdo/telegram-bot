# A simple Telegram bot (telegram-bot)
A simple telegram bot, made for learning purposes. The bot currently has only two functions:
1. Fixing links from https://x.com for its embed versions;
2. Translating messages from english and other languages to brazilian portuguese, using GPT-3.5, a language model trained to produce text, from OpenAI.

The bot's performance is subpar, as it was primarily developed to explore and experiment with the Telegram and OpenAI's APIs.

## Setup

In order to execute the application, you need a OpenAI token to use the translating capabilities and a Telegram bot token in order to scan messages in a group or private conversation. Both can me obtained on their own official websites. You also need to run install some python requirements:

```bash
pip install openai python-telegram-bot python-dotenv --upgrade
```

After setting up the keys into a .env file (follow the .env-example as a guide), the bot.py can be executed.

```bash
python3 bot.py
```
