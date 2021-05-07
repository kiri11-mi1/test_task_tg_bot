import telebot
from flask import Flask, request
from app.bot import bot


app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def get_update():
    bot.process_new_updates([
        telebot.types.Update.de_json(
            request.stream.read().decode("utf-8")
        )
    ])
    return "!", 2000


@app.route('/', methods=['GET'])
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://test-task-tg-bot.herokuapp.com/bot')
    return "Webhook setted", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
