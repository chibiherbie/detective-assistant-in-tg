from config_bot import API_KEY_TAAS
import requests
import json

url = 'https://api.tdlib.org/client'

data = {
    "api_key": API_KEY_TAAS,
    "@type": "getChatHistory",
    "chat_id": "-956074757",
    "limit": "200",
    "offset": "0",
    "from_message_id": "0"
}

get_chat_id = {
  "api_key": API_KEY_TAAS,
  "@type": "searchPublicChat",
  "username": "@testbadword"
}


def get_message(chat):
    data['chat_id'] = chat
    rsp = requests.post(url, data=data)
    return rsp.json()['messages']


def get_id_chat(username):
    get_chat_id['username'] = username
    rsp = requests.post(url, data=get_chat_id)
    return rsp.json()['id']


if __name__ == '__main__':
    id_chat = get_id_chat('@testbadword')
    print(id_chat)
    a = get_message(id_chat)
    print(a)
    for i in a:
        print(i['content']['text']['text'])
