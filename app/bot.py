from config import TOKEN
from state_machine import StateMachine
from telebot import TeleBot


bot = TeleBot(TOKEN)
sm = StateMachine()


selected = {
    'size': None,
    'payment': None
}


@bot.message_handler(commands=["start"], func=lambda m: sm.state == 'start_state')
def cmd_start(message):
    bot.send_message(
        message.chat.id,
        'Какую вы хотите пиццу? Большую или маленькую?'
    )
    sm.start_dialog()


@bot.message_handler(commands=["reset"])
def cmd_cancel(message): 
    sm.cancel()
    bot.send_message(message.chat.id, 'Начните заказ по новой с команды /start.')


@bot.message_handler(func=lambda m: sm.state=='food_size')
def food_size(message):
    if message.text.lower() in ['большую', 'маленькую']:
        selected['size'] = message.text.lower()
        sm.select_size()
        return bot.send_message(
            message.chat.id,
            'Как будете оплачивать? Наличкой или безналичкой?',
        )
    bot.send_message(message.chat.id, 'Введите размер: большую или маленькую.')


@bot.message_handler(func=lambda m: sm.state=='payment_form')
def payment_form(message):
    if message.text.lower() in ['наличкой', 'безналичкой']:
        selected['payment'] = message.text.lower()
        sm.select_payment_form()
        return bot.send_message(
            message.chat.id,
            f"Вы хотите {selected['size']} пиццу, оплата {selected['payment']}?",
        )
    bot.send_message(message.chat.id, 'Введите способ оплаты: наличкой или безналичкой.')


@bot.message_handler(func=lambda m: sm.state=='checking')
def fix_order(message):
    if message.text.lower() == 'да':
        sm.fix_order()
        return bot.send_message(message.chat.id, 'Спасибо за заказ!')
    elif message.text.lower() == 'нет':
        return cmd_cancel(message)
    bot.send_message(message.chat.id, 'Ответьте: Да или Нет.')


@bot.message_handler(func=lambda m: sm.state == 'start_state')
def default_answer(message):
    bot.send_message(message.chat.id, 'Сделайте заказ с помощью команды /start.')


if __name__ == "__main__":
    bot.infinity_polling()