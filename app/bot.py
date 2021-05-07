from config import TOKEN
from telebot import TeleBot
from handler import get_response


bot = TeleBot(TOKEN)


@bot.message_handler()
def answer(message):
    bot.send_message(
        message.chat.id,
        get_response(message.chat.id, message.text.lower())
    )


if __name__ == '__main__':
    bot.polling(none_stop=True)