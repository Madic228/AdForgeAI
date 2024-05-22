from ad_manager import AdManager

class AdEditor:
    def __init__(self, ad_text, ad_manager):
        self.ad_text = ad_text
        self.ad_manager = ad_manager
        self.edit_instructions = []

    async def edit_ad(self):
        while True:
            print("\nТекущее объявление:\n", self.ad_text)
            print("\nТекущие параметры:")
            print(f"Модель: {self.ad_manager.model_name}")
            print(f"Потоковая обработка: {'Вкл' if self.ad_manager.stream else 'Выкл'}")
            print(f"Температура: {self.ad_manager.temperature}")
            print("\nЧто вы хотите изменить?")
            print("1: Модель")
            print("2: Потоковая обработка")
            print("3: Температура")
            print("4: Произвольные изменения")
            print("5: Применить изменения и сгенерировать новое объявление")
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
                self.ad_manager.model_name, self.ad_manager.provider = self.ad_manager.get_model_name_and_provider(model_choice)
                # self.edit_instructions.append(f"Измените модель на: {self.ad_manager.model_name}")
            elif choice == 2:
                stream_choice = input("Выберите режим потоковой обработки (1: Вкл, 2: Выкл): ")
                self.ad_manager.stream = stream_choice == '1'
                # self.edit_instructions.append(f"Измените потоковую обработку на: {'Вкл' if self.ad_manager.stream else 'Выкл'}")
            elif choice == 3:
                new_temperature = float(input("Введите новое значение температуры (0-1): "))
                self.ad_manager.temperature = new_temperature
                # self.edit_instructions.append(f"Измените температуру на: {new_temperature}")
            elif choice == 4:
                arbitrary_change = input("Введите произвольное изменение: ")
                self.edit_instructions.append(arbitrary_change)
            elif choice == 5:
                if self.edit_instructions:  # Проверка на произвольные изменения
                    # Генерация нового объявления с изменениями
                    old_ad_text = self.ad_text
                    edit_instructions_str = "\n".join(self.edit_instructions)
                    self.ad_text = await self.ad_manager.generate_ad_with_edit(old_ad_text, edit_instructions_str)
                    version = self.ad_manager.load_ad_version_from_json()
                    version += 1
                    self.ad_manager.save_ad_to_json(self.ad_text, version)
                    print("\nОбновленное объявление:\n", self.ad_text)
                    self.edit_instructions = []  # Очистка списка инструкций
                else:  # Генерация нового объявления с новыми параметрами
                    self.ad_text = await self.ad_manager.generate_ad()
                    version = self.ad_manager.load_ad_version_from_json()
                    version += 1
                    self.ad_manager.save_ad_to_json(self.ad_text, version)
                    print("\nОбновленное объявление:\n", self.ad_text)
            elif choice == 6:  # Завершение редактирования
                break