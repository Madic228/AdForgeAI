import openai
import json
import os
import requests

# Получение API-ключа
def get_api_key():
    # Реализуйте эту функцию в соответствии с вашими актуальными данными
    openai_key_file = 'Bearer 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'
    with open(openai_key_file, 'r', encoding='utf-8') as f:
        openai_key = json.loads(f.read())
    return openai_key['api']

openai.api_key = 'Bearer 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'

class ChatGPT:
    def __init__(self, proxy=None):
        self.chat_history = []
        self.proxy = proxy

    def ask_gpt(self, question):
        # Добавляем в историю чатов текущий вопрос пользователя
        self.chat_history.append({"role": "user", "content": question})

        # Настройка параметров прокси для запроса
        proxies = self.proxy if self.proxy else {}

        # Вызываем API для получения ответа
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=self.format_chat_history(),
            max_tokens=150,
            proxies=proxies  # Передача параметров прокси
        )

        # Добавляем ответ в историю чатов
        self.chat_history.append({"role": "assistant", "content": response.choices[0].text.strip()})

        return response

    def format_chat_history(self):
        # Форматируем историю чатов для передачи модели
        chat_history = []
        for msg in self.chat_history:
            chat_history.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(chat_history)


def main():
    # Укажите свой прокси-сервер
    proxy = {
        "http": "http://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970",
        # Добавьте аналогичные настройки для HTTPS, если это необходимо
    }
    chat = ChatGPT(proxy=proxy)

    while True:
        user_input = input("You: ")

        # Выход из программы при вводе "0"
        if user_input.strip() == "0":
            print("Exiting...")
            break

        # Запрос на получение ответа от модели
        response = chat.ask_gpt(user_input)

        # Вывод ответа ассистента
        print(f"ChatGPT: {response.choices[0].text.strip()}")

if __name__ == '__main__':
    main()
