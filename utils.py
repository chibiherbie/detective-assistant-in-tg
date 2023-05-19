

def clear_url_chat_id(chat_tg):
    if '@' in chat_tg:
        return chat_tg.strip()
    if 'https://t.me/' in chat_tg:
        return '@' + chat_tg.replace('https://t.me/', '')
    if 't.me/' in chat_tg:
        return '@' + chat_tg.replace('t.me/', '').strip()


if __name__ == '__main__':
    print(clear_url_chat_id('https://t.me/testbadword'))
