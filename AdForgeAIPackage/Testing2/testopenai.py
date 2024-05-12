import openai
import requests

# Установите ваш ключ API от OpenAI
api_key = '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'

# Установите языковую модель, которую хотите использовать (для примера используется GPT-3.5)
language_model = "text-davinci-003"

# Укажите настройки прокси
proxy = {
    'http': 'http://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970',
    # 'https': 'https://your-proxy-url:port'
}

def query_gpt(prompt):
    response = openai.Completion.create(
      engine=language_model,
      prompt=prompt,
      max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    while True:
        user_input = input("Введите ваш запрос: ")
        if user_input.lower() == 'выход':
            print("Программа завершена.")
            break
        # Отправляем запрос через прокси
        try:
            response = query_gpt(user_input)
            print("Ответ от модели ChatGPT:", response)
        except requests.exceptions.ProxyError:
            print("Ошибка при отправке запроса через прокси.")

if __name__ == "__main__":
    main()