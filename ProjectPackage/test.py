import openai
import json
import os

os.environ["HTTP_PROXY"] = "http://134.122.73.206:7890"
os.environ["HTTPS_PROXY"] = "http://128.140.51.69:18"


# Получение API-ключа
def get_api_key():
    # Реализуйте эту функцию в соответствии с вашими актуальными данными
    openai_key_file = 'envs/openai_key.json'
    with open(openai_key_file, 'r', encoding='utf-8') as f:
        openai_key = json.loads(f.read())
    return openai_key['api']


openai.api_key = get_api_key()


class ChatGPT:
    def __init__(self):
        self.chat_history = []

    def ask_gpt(self, question):
        # Добавляем в историю чатов текущий вопрос пользователя
        self.chat_history.append({"role": "user", "content": question})

        # Вызываем API для получения ответа
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=self.format_chat_history(),
            max_tokens=150
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
    chat = ChatGPT()

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
