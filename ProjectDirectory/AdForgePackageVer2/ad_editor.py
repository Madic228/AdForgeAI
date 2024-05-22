from ad_manager import AdManager

class AdEditor:
    def __init__(self, ad_text, ad_manager):
        self.ad_text = ad_text
        self.ad_manager = ad_manager

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
            print("5: Закончить редактирование")
            choice = int(input("Введите номер параметра: "))

            edit_instructions = ""
            if choice == 1:
                print("Выберите модель:")
                print("1: gpt-3.5-turbo-0125")
                print("2: claude-3-haiku-20240307")
                print("3: google/gemma-1.1-7b-it")
                print("4: NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO")
                print("5: green")
                model_choice = int(input("Введите номер модели: "))
                self.ad_manager.model_name, self.ad_manager.provider = self.ad_manager.get_model_name_and_provider(model_choice)
                edit_instructions = f"Измените модель на: {self.ad_manager.model_name}"
            elif choice == 2:
                stream_choice = input("Выберите режим потоковой обработки (1: Вкл, 2: Выкл): ")
                self.ad_manager.stream = stream_choice == '1'
                edit_instructions = f"Измените потоковую обработку на: {'Вкл' if self.ad_manager.stream else 'Выкл'}"
            elif choice == 3:
                new_temperature = float(input("Введите новое значение температуры (0-1): "))
                self.ad_manager.temperature = new_temperature
                edit_instructions = f"Измените температуру на: {new_temperature}"
            elif choice == 4:
                arbitrary_change = input("Введите произвольное изменение: ")
                edit_instructions = arbitrary_change
            elif choice == 5:
                break

            # Генерация нового объявления с изменениями
            old_ad_text = self.ad_text
            self.ad_text = await self.ad_manager.generate_ad_with_edit(old_ad_text, edit_instructions)
            version = self.ad_manager.load_ad_version_from_json()
            version += 1
            self.ad_manager.save_ad_to_json(self.ad_text, version)

        print("\nОбновленное объявление:\n", self.ad_text)
