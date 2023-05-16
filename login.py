from config_bot import API_KEY_TAAS
import requests

url = 'https://api.tdlib.org/client'

data = {
    "api_key": API_KEY_TAAS,
    "@type": "getChatHistory",
    "chat_id": "956074757",
    "limit": "100",
    "offset": "0",
    "from_message_id": "0"
}

rsp = requests.post(url, data=data)
print(rsp, rsp.text)
