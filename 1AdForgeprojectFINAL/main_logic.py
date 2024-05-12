import g4f
import json
import logging
from g4f_providers_and_models.g4f_utils import save_providers_to_json, save_models_to_json

g4f.debug.logging = True

logging.basicConfig(
    filename='g4f.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)

def load_data_from_json(filename):
    """Загружает данные из JSON файла."""
    try:
        with open(filename, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def choose_provider(providers):
    """Позволяет пользователю выбрать провайдера."""

    print("Доступные провайдеры:")
    for i, provider_name in enumerate(providers):
        print(f"{i+1}. {provider_name}")

    while True:
        try:
            choice = int(input("Введите номер провайдера: "))
            if 1 <= choice <= len(providers):
                return list(providers.keys())[choice - 1]
            else:
                print("Неверный номер провайдера.")
        except ValueError:
            print("Введите число.")

def choose_model(models):
    """Позволяет пользователю выбрать модель."""

    print("Доступные модели:")
    for i, model_name in enumerate(models):
        print(f"{i+1}. {model_name}")

    while True:
        try:
            choice = int(input("Введите номер модели: "))
            if 1 <= choice <= len(models):
                return list(models.keys())[choice - 1]
            else:
                print("Неверный номер модели.")
        except ValueError:
            print("Введите число.")

def main():
    """Главная функция чата."""

    save_providers_to_json()
    save_models_to_json()

    providers = load_data_from_json("providers.json")
    models = load_data_from_json("models.json")

    chosen_provider = choose_provider(providers)
    chosen_model = choose_model(models)

    print(f"Вы выбрали провайдера: {chosen_provider} и модель: {chosen_model}")

    chat_history = []

    while True:
        user_input = input("Вы: ")
        chat_history.append({"role": "user", "content": user_input})

        try:
            response = g4f.ChatCompletion.create(
                model=getattr(g4f.models, chosen_model),
                messages=chat_history,
                provider=getattr(g4f.Provider, chosen_provider)
            )
            print(f"GPT: {response}")
            chat_history.append({"role": "assistant", "content": response})
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()