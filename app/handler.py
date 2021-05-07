from state_machine import StateMachine


storage = {}


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


def get_response(chat_id, text):
    if get_or_create_state(chat_id) == 'start_state' and text == '/start':
        storage[chat_id]['state'].start_dialog()
        return 'Какую вы хотите пиццу? Большую или маленькую?'

    elif text == '/reset':
        storage[chat_id]['state'].cancel()
        return 'Начните заказ по новой с команды /start.'

    elif get_or_create_state(chat_id) == 'food_size':
        if text in ['большую', 'маленькую']:
            storage[chat_id]['size'] = text
            storage[chat_id]['state'].select_size()
            return 'Как будете оплачивать? Наличкой или безналичкой?'
        else:
            return 'Введите размер: большую или маленькую.'

    elif get_or_create_state(chat_id) == 'payment_form':
        if text in ['наличкой', 'безналичкой']:
            storage[chat_id]['payment'] = text
            storage[chat_id]['state'].select_payment_form()
            return f"Вы хотите {storage[chat_id]['size']} пиццу, оплата {storage[chat_id]['payment']}?",
        else:
            return 'Введите способ оплаты: наличкой или безналичкой.'

    elif get_or_create_state(chat_id) == 'checking':
        if text == 'да':
            storage[chat_id]['state'].fix_order()
            return 'Спасибо за заказ!'
        elif text == 'нет':
            storage[chat_id]['state'].cancel()
            return 'Начните заказ по новой с команды /start.'
        else:
            return 'Ответьте: Да или Нет.'

    return 'Сделайте заказ с помощью команды /start.'
