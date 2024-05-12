from g4f.client import Client

proxies = {
    "all": "http://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970",
    "https": "https://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970"
}
client = Client(proxies=proxies)

def get_user_input(prompt, options=None):
    """Получает ввод от пользователя с проверкой."""

    while True:
        user_input = input(prompt).strip()
        if options is not None and user_input not in options:
            print("Неверный выбор. Попробуйте снова.")
        else:
            return user_input

def generate_ad(parameters):
    """Генерирует рекламное объявление на основе заданных параметров."""

    messages = [
        {"role": "system", "content": "Ты - опытный копирайтер, который создает рекламные объявления."},
        {"role": "user", "content": f"""
            Напиши рекламное объявление с учетом следующих параметров:
            {parameters}
        """}
    ]

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )

    ad_text = ""
    for completion in chat_completion:
        chunk = completion.choices[0].delta.content or ""
        ad_text += chunk
        print(chunk, end="", flush=True)

    return ad_text

def edit_ad(ad_text):
    """Позволяет пользователю редактировать объявление."""

    print("\nТекущее объявление:\n", ad_text)

    actions = {
        "1": "Сократить объем",
        "2": "Увеличить объем",
        "3": "Сделать текст более строгим",
        "4": "Сделать текст более дружелюбным",
        "5": "Завершить редактирование"
    }

    while True:
        print("\nВыберите действие:")
        for key, value in actions.items():
            print(f"{key}. {value}")

        choice = get_user_input("Введите номер действия: ", options=actions.keys())

        if choice == "5":
            break

        instructions = input("Введите инструкции для GPT (например, 'Сократи текст до 50 слов'): ")

        messages = [
            {"role": "system", "content": "Ты - опытный редактор рекламных объявлений."},
            {"role": "user", "content": f"""
                Отредактируй следующее объявление:
                {ad_text}

                Инструкции: {instructions}
            """}
        ]

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )

        edited_ad_text = ""
        for completion in chat_completion:
            chunk = completion.choices[0].delta.content or ""
            edited_ad_text += chunk
            print(chunk, end="", flush=True)

        ad_text = edited_ad_text

    return ad_text

def main():
    """Главная функция программы."""

    session_data = []

    while True:
        print("\nНовая сессия.")

        parameters = {}
        parameters["Заголовок"] = input("Введите заголовок объявления: ")
        parameters["Целевая аудитория"] = input("Введите целевую аудиторию: ")
        parameters["Ключевые преимущества"] = input("Введите ключевые преимущества: ")
        parameters["Призыв к действию"] = input("Введите призыв к действию: ")

        # Дополнительные параметры
        parameters["Стиль объявления"] = get_user_input("Введите стиль объявления (например, 'формальный', 'неформальный', 'юмористический'): ")
        parameters["Ограничение длины"] = get_user_input("Введите ограничение длины (например, 'до 100 слов'): ")
        # ... добавьте другие параметры ...

        parameters_string = "\n".join(f"- {key}: {value}" for key, value in parameters.items())

        ad_text = generate_ad(parameters_string)
        session_data.append({"parameters": parameters, "ad": ad_text})

        edit_choice = get_user_input("Хотите редактировать объявление? (да/нет): ", options=["да", "нет"])
        if edit_choice == "да":
            ad_text = edit_ad(ad_text)
            session_data[-1]["ad"] = ad_text

        print("\nФинальное объявление:\n", ad_text)

        continue_choice = get_user_input("Хотите начать новую сессию? (да/нет): ", options=["да", "нет"])
        if continue_choice == "нет":
            break

    print("Сессия завершена.")

if __name__ == "__main__":
    main()