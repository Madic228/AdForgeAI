import asyncio
from ad_manager import AdManager
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
    model_choice_input = input("Введите номер модели (по умолчанию 1): ")
    model_choice = int(model_choice_input) if model_choice_input else None

    temperature_input = input("Введите значение temperature (например, 0.7) (по умолчанию 0.7): ")
    temperature = float(temperature_input) if temperature_input else None

    stream_input = input("Включить режим stream? (да/нет) (по умолчанию нет): ").strip().lower()
    stream = stream_input == 'да' if stream_input else None

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

    edit_choice = input("\nХотите отредактировать объявление? (да/нет): ").strip().lower()
    if edit_choice == 'да':
        from ad_editor import AdEditor
        ad_editor = AdEditor(ad_text, ad_manager)
        await ad_editor.edit_ad()

# Запуск асинхронной функции main
asyncio.run(main())
