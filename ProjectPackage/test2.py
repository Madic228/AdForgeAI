import requests
import os

# Установка прокси-серверов
os.environ["HTTP_PROXY"] = "http://136.243.89.93:8888"
os.environ["HTTPS_PROXY"] = "http://128.140.51.69:18"

# Указание страны и авторизационного заголовка
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer sk-proj-X0WWGavi2Y9f9HqfPdpeT3BlbkFJ4yYdV9K8IC2bcCiVab12',
    'X-Geo-Country': 'De'
}

data = {
    "model": "text-davinci-002",  # Заменено на актуальную версию
    "messages": [{"role": "user", "content": "Say this is a test!"}],
    "temperature": 0.7
}

# Отправка запроса через прокси
response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

# Обработка ответа
if response.status_code == 200:
    print("Available ChatGPT versions:")
    versions = response.json().get("model_versions")
    for version in versions:
        print(version)
else:
    print("Failed to retrieve ChatGPT versions. Status code:", response.status_code)
