from config import TOKEN
from state_machine import StateMachine
from telebot import TeleBot
from flask import Flask, request


bot = TeleBot(TOKEN, threaded=False)
storage = dict()
app = Flask(__name__)


def get_or_create_state(chat_id):
    try:
        return storage[chat_id]['state'].state
    except KeyError:
        storage.update({
            chat_id: {
                'state': StateMachine(),
                'size': None,
                'payment': None,
            }
        })
        return storage[chat_id]['state'].state


@bot.message_handler(commands=["start"], func=lambda msg: get_or_create_state(msg.chat.id) == 'start_state')
def cmd_start(message):
    storage[message.chat.id]['state'].start_dialog()
    bot.send_message(
        message.chat.id,
        'Какую вы хотите пиццу? Большую или маленькую?'
    )


@bot.message_handler(commands=["reset"])
def cmd_cancel(message):
    storage[message.chat.id]['state'].cancel()
    bot.send_message(message.chat.id, 'Начните заказ по новой с команды /start.')


@bot.message_handler(func=lambda msg: get_or_create_state(msg.chat.id) == 'food_size')
def food_size(message):
    if message.text.lower() in ['большую', 'маленькую']:
        storage[message.chat.id]['size'] = message.text.lower()
        storage[message.chat.id]['state'].select_size()
        return bot.send_message(
            message.chat.id,
            'Как будете оплачивать? Наличкой или безналичкой?',
        )
    bot.send_message(message.chat.id, 'Введите размер: большую или маленькую.')


@bot.message_handler(func=lambda msg: get_or_create_state(msg.chat.id) == 'payment_form')
def payment_form(message):
    if message.text.lower() in ['наличкой', 'безналичкой']:
        storage[message.chat.id]['payment'] = message.text.lower()
        storage[message.chat.id]['state'].select_payment_form()
        return bot.send_message(
            message.chat.id,
            f"Вы хотите {storage[message.chat.id]['size']} пиццу, оплата {storage[message.chat.id]['payment']}?",
        )
    bot.send_message(message.chat.id, 'Введите способ оплаты: наличкой или безналичкой.')


@bot.message_handler(func=lambda msg: get_or_create_state(msg.chat.id) == 'checking')
def fix_order(message):
    if message.text.lower() == 'да':
        storage[message.chat.id]['state'].fix_order()
        return bot.send_message(message.chat.id, 'Спасибо за заказ!')
    elif message.text.lower() == 'нет':
        return cmd_cancel(message)
    bot.send_message(message.chat.id, 'Ответьте: Да или Нет.')


@bot.message_handler(func=lambda msg: get_or_create_state(msg.chat.id) == 'start_state')
def default_answer(message):
    bot.send_message(message.chat.id, 'Сделайте заказ с помощью команды /start.')


@app.route('/tg_bot', methods=['POST'])
def get_update():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return


@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://test-task-tg-bot.herokuapp.com/tg_bot')
    return


if __name__ == "__main__":
    app.run()
