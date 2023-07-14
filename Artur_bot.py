import time

import telebot as telebot

from config_bot import TOKEN_BOT
import re
from utils import clear_url_chat_id
import telegram_api
import json
from text_model.text_analysis import analysis_text

bot = telebot.TeleBot(TOKEN_BOT)
ORD_LIST_SYMBOL = [21328, 1161]
ORD_RUSSIA = [1040, 1103]
ORD_ENGLISH = [1, 122]
BORDER_STRANGE_MIDDLE = 4
BORDER_STRANGE = 8


def analyze_special_symbol(text):
    """Анализ на специальный символы"""
    for i in text:
        if ord(i) in ORD_LIST_SYMBOL:
            return True
    return False


def analyze_text(text):
    """Определение степени подозрительности текста"""
    strange_elem = []
    count = 0

    clean_text = re.sub("[^\w\s, ]", "", text)
    print(clean_text)

    # Проверка на специльные символы
    if analyze_special_symbol(text):
        return 1

    # Проврека чистого текста
    for i in clean_text:
        print(i, "-", ord(i))
        ord_elem = ord(i)

        if not (ORD_ENGLISH[0] <= ord_elem <= ORD_ENGLISH[1] or
                ORD_RUSSIA[0] <= ord_elem <= ORD_RUSSIA[1]):
            count += 1
            strange_elem.append(i)

        if count == BORDER_STRANGE:
            return 2

    if count > BORDER_STRANGE_MIDDLE:
        return 1

    return 0


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет. Моя задач находить плохие слова. Пока я в тестовом режиме, поэтому '
                                      'отправь мне группу или пришли сообщение, и я попробую там найти что-то нехорошое')


@bot.message_handler(commands=['search'])
def analyze_group_message(message):
    bot.send_message(message.chat.id, 'Отправь мне ссылку на группу или ник этой группы'
                                      '\n\nНапример:\nhttps://t.me/somegroup\nt.me/somegroup\n@somegroup'
                                      '\n\nЕсли твоя ссылка не похожа на ссылки из примеров, то перешли сообщение из группы')
    bot.register_next_step_handler(message, get_group_url)


def get_group_url(message):
    """Сканирование сообщений в группе по ссылке"""

    bot.send_message(message.chat.id, 'Обработка началась, ожидайте')

    msg_finished = []

    try:
        if message.forward_from_chat:
            id_chat = message.forward_from_chat.id
        else:
            username_chat = clear_url_chat_id(message.text)
            id_chat = telegram_api.get_id_chat(username_chat)
        messages = telegram_api.get_message(id_chat)
        print(id_chat)

        all_text = ''
        for message_chat in messages:
            if message_chat['content']['@type'] == 'messageText':
                msg = message_chat['content']['text']['text']
                chat_info = bot.get_chat(message_chat['chat_id'])
                print(chat_info)
                msg_link = f"https://t.me/{chat_info.username}/{message_chat['id']}"
                print(msg)

                if analyze_special_symbol(msg):
                    msg_finished.append(f'Сообщение подозрительное, найден символ из списка\n{msg}')
                else:
                    all_text += f'{msg} \n '

            if len(msg_finished) >= 10:
                bot.send_message(message.chat.id, f'\n{"-" * 10}\n'.join(msg_finished))
                msg_finished = []

        # result = analysis_text(all_text)
        # for i in result.itertuples():
        #     print(i.text, i.labels)
        #     if not i.labels:
        #         msg_finished.append(f'Сообщение подозрительное \n{i.text}')
        #     if len(msg_finished) >= 10:
        #         bot.send_message(message.chat.id, f'\n{"-" * 10}\n'.join(msg_finished))
        #         msg_finished = []
        #         time.sleep(1)

        if msg_finished:
            bot.send_message(message.chat.id, f'\n{"-" * 10}\n'.join(msg_finished))

        bot.send_message(message.chat.id, f'Анализ закончен')

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, f'Так... что-то не то\nДля повторной попытки введи /search')


@bot.message_handler(commands=['list_symbol'])
def list_symbol(message):
    msg = ''
    for s in ORD_LIST_SYMBOL:
        msg += f'{chr(s)}\n'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['add_symbol'])
def add_symbol(message):
    bot.send_message(message.chat.id, 'Отправь символ, чтобы каждый раз реагировать на него')
    bot.register_next_step_handler(message, add_symbol_to_list)


def add_symbol_to_list(message):
    global ORD_LIST_SYMBOL

    symbol = ord(message.text)
    ORD_LIST_SYMBOL.append(symbol)
    danger_symbol['danger_symbol'] = ORD_LIST_SYMBOL
    with open('danger_symbol.json', 'w') as f:
        json.dump(danger_symbol, f)
    bot.send_message(message.chat.id, f'Символ {message.text} добавлен')


@bot.message_handler(content_types=['text'])
def some_text(message):
    try:
        print("Сообщение", message.text)
        bot.send_message(message.chat.id, 'Обработка началась, ожидайте')
        analyze_message_model(message)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, f'Так... что-то не то\nПопробуй ещё раз')


def analyze_message_model(message):
    if analyze_special_symbol(message.text):
        bot.reply_to(message, f'сообщение подозрительное, найден символ из списка \n {message.text}')

    result = analysis_text(message.text)
    for i in result.itertuples():
        print(i.text, i.labels)
        if i.labels:
            bot.reply_to(message, f'Сообщение не подозрительное')
        else:
            bot.reply_to(message, f'Сообщение подозрительное')


def analyze_message(message):
    status = analyze_text(message.text)

    text_clear = re.sub("[^\w\s, ]", "", message.text)
    msg_clear = f'\n\nОбработанное чистое сообщение:\n"{text_clear}"'

    if not status:
        bot.reply_to(message, f'сообщение выглядит нормально{msg_clear}')
    elif status == 1:
        bot.reply_to(message, f'сообщение подозрительное{msg_clear}')
    else:
        bot.reply_to(message, f'сообщение точно что-то скрывает{msg_clear}')


with open('danger_symbol.json') as f:
    danger_symbol = json.load(f)

ORD_LIST_SYMBOL = danger_symbol['danger_symbol']
bot.polling(none_stop=True)
