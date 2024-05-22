import asyncio
from ad_manager import AdManager
from ad_editor import AdEditor
from config import proxies

async def main():
    ad_manager = AdManager(proxies=proxies)

    headline = input("Введите заголовок объявления: ")
    audience = input("Введите целевую аудиторию: ")
    ad_manager.set_basic_params(headline, audience)

    key_benefits = input("Введите ключевые преимущества (необязательно): ")
    call_to_action = input("Введите призыв к действию (необязательно): ")
    style = input("Введите стиль объявления (необязательно): ")
    length_limit = input("Введите ограничения на длину слов (необязательно): ")
    length_limit = int(length_limit) if length_limit else None
    print("Выберите модель:")
    print("1: gpt-3.5-turbo-0125")
    print("2: claude-3-haiku-20240307")
    print("3: google/gemma-1.1-7b-it")
    print("4: NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO")
    print("5: green")
    model_choice = input("Введите номер модели (необязательно): ")
    model_choice = int(model_choice) if model_choice else None
    temperature = input("Введите значение temperature (необязательно, например, 0.7): ")
    temperature = float(temperature) if temperature else None
    stream = input("Включить режим stream? (необязательно, да/нет): ").strip().lower()
    stream = stream == 'да' if stream else None

    ad_manager.set_advanced_params(
        key_benefits=key_benefits,
        call_to_action=call_to_action,
        style=style,
        length_limit=length_limit,
        model_choice=model_choice,
        temperature=temperature,
        stream=stream
    )

    ad_text = await ad_manager.generate_ad()
    if not stream:
        print("\nГотовое объявление:\n", ad_text)

    edit = input("Хотите отредактировать объявление? (да/нет): ").strip().lower()
    if edit == 'да':
        editor = AdEditor(ad_text, ad_manager)
        await editor.edit_ad()

# Запуск асинхронной функции main
asyncio.run(main())