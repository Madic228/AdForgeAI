import requests

# Укажите ваш прокси-сервер и порт
proxy = 'http://128.140.51.69:8118'

# Укажите страну, из которой хотите отправлять запросы (если прокси-сервер поддерживает)
# Замените 'country_code' на код страны, например, 'US' для США
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer sk-proj-X0WWGavi2Y9f9HqfPdpeT3BlbkFJ4yYdV9K8IC2bcCiVab12',
    'X-Geo-Country': 'De'
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Say this is a test!"}],
    "temperature": 0.7
}

# Подключение через прокси
response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data, proxies={'http': proxy, 'https': proxy})

# Вывод результата
print(response.json())
