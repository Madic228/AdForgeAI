import asyncio
from ProjectDirectory.AdForgePackageVer3.ad_manager import AdManager
from ProjectDirectory.AdForgePackageVer3.ad_editor import AdEditor
from ProjectDirectory.AdForgePackageVer3.config import proxies

async def main():
    ad_manager = AdManager(proxies=proxies)

    while True:
        print("\nВыберите действие:")
        print("1: Создать новое объявление")
        print("2: Загрузить существующее объявление")
        print("3: Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
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

                # Взаимодействие с AdEditor через функции
                while True:
                    # Вывод текущих параметров
                    print("\nТекущее объявление:\n", editor.ad_text)
                    print("\nТекущие параметры:")
                    print(f"Модель: {editor.ad_manager.model_name}")
                    print(f"Потоковая обработка: {'Вкл' if editor.ad_manager.stream else 'Выкл'}")
                    print(f"Температура: {editor.ad_manager.temperature}")

                    print("\nЧто вы хотите изменить?")
                    print("1: Модель")
                    print("2: Потоковая обработка")
                    print("3: Температура")
                    print("4: Произвольные изменения")
                    print("5: Применить изменения")
                    print("6: Завершить редактирование")
                    choice = int(input("Введите номер параметра: "))

                    if choice == 1:
                        print("Выберите модель:")
                        print("1: gpt-3.5-turbo-0125")
                        print("2: claude-3-haiku-20240307")
                        print("3: google/gemma-1.1-7b-it")
                        print("4: NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO")
                        print("5: green")
                        model_choice = int(input("Введите номер модели: "))
                        ad_text = await editor.change_model(model_choice)
                        print("\nОбновленное объявление:\n", ad_text)
                    elif choice == 2:
                        stream_choice = int(input("Выберите режим потоковой обработки (1: Вкл, 2: Выкл): "))
                        await editor.toggle_stream(stream_choice == 1)
                    elif choice == 3:
                        new_temperature = float(input("Введите новое значение температуры (0-1): "))
                        await editor.change_temperature(new_temperature)
                    elif choice == 4:
                        arbitrary_change = input("Введите произвольное изменение: ")
                        await editor.add_arbitrary_change(arbitrary_change)
                    elif choice == 5:
                        ad_text = await editor.apply_changes()
                        print("\nОбновленное объявление:\n", ad_text)
                    elif choice == 6:
                        break
        elif choice == '2':
            ads = ad_manager.load_ad_version_from_json()

            if ads:
                for i, ad in enumerate(ads):
                    print(f"{i + 1}: {ad['headline']} - {ad['audience']} - Версия: {ad['version']}")

                try:
                    ad_index = int(input("Введите номер объявления: ")) - 1
                    if 0 <= ad_index < len(ads):
                        ad_manager.ad_text = ads[ad_index]['ad_text']
                        ad_manager.headline = ads[ad_index]['headline']
                        ad_manager.audience = ads[ad_index]['audience']
                        ad_manager.key_benefits = ads[ad_index]['key_benefits']
                        ad_manager.call_to_action = ads[ad_index]['call_to_action']
                        ad_manager.style = ads[ad_index]['style']
                        ad_manager.length_limit = ads[ad_index]['length_limit']
                        ad_manager.model_name = ads[ad_index]['model_name']
                        ad_manager.temperature = ads[ad_index]['temperature']
                        ad_manager.stream = ads[ad_index]['stream']

                        ad_manager.initialize_generator()

                        # Взаимодействие с AdEditor через функции
                        editor = AdEditor(ad_manager.ad_text, ad_manager)
                        while True:
                            # Вывод текущих параметров
                            print("\nТекущее объявление:\n", editor.ad_text)
                            print("\nТекущие параметры:")
                            print(f"Модель: {editor.ad_manager.model_name}")
                            print(f"Потоковая обработка: {'Вкл' if editor.ad_manager.stream else 'Выкл'}")
                            print(f"Температура: {editor.ad_manager.temperature}")

                            print("\nЧто вы хотите изменить?")
                            print("1: Модель")
                            print("2: Потоковая обработка")
                            print("3: Температура")
                            print("4: Произвольные изменения")
                            print("5: Применить изменения")
                            print("6: Завершить редактирование")
                            choice = int(input("Введите номер параметра: "))

                            if choice == 1:
                                print("Выберите модель:")
                                print("1: gpt-3.5-turbo-0125")
                                print("2: claude-3-haiku-20240307")
                                print("3: google/gemma-1.1-7b-it")
                                print("4: NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO")
                                print("5: green")
                                model_choice = int(input("Введите номер модели: "))
                                ad_text = await editor.change_model(model_choice)
                                print("\nОбновленное объявление:\n", ad_text)
                            elif choice == 2:
                                stream_choice = int(input("Выберите режим потоковой обработки (1: Вкл, 2: Выкл): "))
                                await editor.toggle_stream(stream_choice == 1)
                            elif choice == 3:
                                new_temperature = float(input("Введите новое значение температуры (0-1): "))
                                await editor.change_temperature(new_temperature)
                            elif choice == 4:
                                arbitrary_change = input("Введите произвольное изменение: ")
                                await editor.add_arbitrary_change(arbitrary_change)
                            elif choice == 5:
                                ad_text = await editor.apply_changes()
                                print("\nОбновленное объявление:\n", ad_text)
                            elif choice == 6:
                                break
                    else:
                        print("Некорректный номер объявления.")
                except ValueError:
                    print("Некорректный ввод. Введите число.")
                except IndexError:
                    print("Некорректный номер объявления.")

            else:
                print("Нет сохраненных объявлений.")
        elif choice == '3':
            break




# Запуск асинхронной функции main
asyncio.run(main())
