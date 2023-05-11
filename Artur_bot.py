import telebot as telebot

from config_bot import TOKEN_BOT
import re

bot = telebot.TeleBot(TOKEN_BOT)
GROUP_ID = '-956074757'
ORD_LIST_SYMBOL = [21328, 1161]
ORD_RUSSIA = [1040, 1103]
ORD_ENGLISH = [1, 122]
BORDER_STRANGE_MIDDLE = 2
BORDER_STRANGE = 5


def analyze_text(text):

    strange_elem = []
    count = 0

    clean_text = re.sub("[^\w\s, ]", "", text)
    print(clean_text)

    # Проверка на специльные символы
    for i in text:
        if ord(i) in ORD_LIST_SYMBOL:
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
    bot.send_message(message.chat.id, "Привет. Моя задач находить плохие слова. Пока я в тестовом режиме, поэтому "
                                      "добавь меня в группу, и я попробую там найти что-то нехорошое")


@bot.message_handler(commands=['search'])
def button_message(message):
    bot.send_message(message.chat.id, 'Выполняю поиск... (в будущем)')


@bot.message_handler(content_types=['text'])
def echo(message):
    print("Сообщение", message.text)

    status = analyze_text(message.text)
    
    text_clear = re.sub("[^\w\s, ]", "", message.text)
    msg_clear = f'\n\nОбработанное сообщение:\n"{text_clear}"'
    
    if not status:
        bot.reply_to(message, f'сообщение выглядит нормально{msg_clear}')
    elif status == 1:
        bot.reply_to(message, f'сообщение подозрительное{msg_clear}')
    else:
        bot.reply_to(message, f'сообщение точно что-то скрывает{msg_clear}')


bot.polling(none_stop=True)
