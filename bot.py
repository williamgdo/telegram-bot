### TODO: make this a virtual environment instead of a commentary:
# pip install openai python-telegram-bot python-dotenv --upgrade

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from openai import OpenAI


load_dotenv()

OPEN_AI_TOKEN = os.environ.get['OPEN_AI_TOKEN']
TELEGRAM_TOKEN = os.environ.get['TELEGRAM_TOKEN']

chatgpt = OpenAI(api_key=OPEN_AI_TOKEN)

def prompt(text):
    answer = chatgpt.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um tradutor de textos. Para cada texto enviado a você, você responderá somente uma tradução do texto corrigido de acordo com a ortografia português brasileiro. Responda SOMENTE o texto da tradução."},
            {"role": "user", "content": text},
        ],
        temperature=0.7,
    )
    return answer.choices[0].message.content

# this function is used to translate messages into brazilian portuguese
# to use it, you need to answer /translate as a reply to a message in telegram
# the bot will check if there is a reply to its message and answer the translation accordingly
# ATTENTION: this only works with privacy mode DISABLED. The bot needs to be able to read all messages from the group.
async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = update.message.reply_to_message

    if reply is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode="html",
            text="Escreva /translate como resposta para uma mensagem."
        )
        return

    answer = prompt(reply.text)

    message = f"Tradução: \n<blockquote>{answer}</blockquote>"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode="html",
        text=message
    )

# this function reposts message with a starting link from www.x.com or www.twitter.com for a version of the link which serves video embeds to desktop
# the server responsible is a open source project called vxTwitter: https://github.com/dylanpdx/BetterTwitFix
async def link_fix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.chat is None:
      return

    if update.message.text is not None and update.api_kwargs is not None:
      message = update.message.text
      prefixes = ["https://x.com/", "x.com/", "https://www.x.com/", "www.x.com/", "https://twitter.com/", "twitter.com/", "https://www.twitter.com/","www.twitter.com/",]

      for prefix in prefixes:
        if message.startswith(prefix):
          
          remaining_text = message[len(prefix):]
          if not remaining_text:
            return

          modified_url = message.replace(prefix, "https://fixvx.com/")
        
          ####### CAUTION: This delets the message with original link
          # await context.bot.delete_message(message_id = update.message.message_id,
          #                  chat_id = update.message.chat_id)
          # username = update.message.from_user.username

          await context.bot.send_message(
              chat_id=update.effective_chat.id,
              parse_mode="html",
              text=f"{modified_url}"
              # you can also use the username in a message
              # text=f"{modified_url}\n\n Reposted link from @{username}."
          )
          break
    else:
        return


if __name__ == '__main__':
    print("Bot is starting.")
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    translate_handler = CommandHandler('translate', translate)
    link_fix_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), link_fix)

    application.add_handler(translate_handler)
    application.add_handler(link_fix_handler)

    print("Bot is polling messages...")
    application.run_polling(poll_interval=5)
