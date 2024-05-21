class AdEditor:
    def __init__(self, ad_text):
        self.ad_text = ad_text

    def edit_ad(self):
        while True:
            print("\nТекущее объявление:\n", self.ad_text)
            print("\nЧто вы хотите изменить?")
            print("1: Заголовок объявления")
            print("2: Целевую аудиторию")
            print("3: Ключевые преимущества")
            print("4: Призыв к действию")
            print("5: Стиль объявления")
            print("6: Ограничения на длину слов")
            print("7: Произвольные изменения")
            print("8: Закончить редактирование")
            choice = int(input("Введите номер параметра: "))

            if choice == 1:
                new_headline = input("Введите новый заголовок объявления: ")
                self.ad_text = self._replace_param("Заголовок объявления", new_headline)
            elif choice == 2:
                new_audience = input("Введите новую целевую аудиторию: ")
                self.ad_text = self._replace_param("Целевая аудитория", new_audience)
            elif choice == 3:
                new_key_benefits = input("Введите новые ключевые преимущества: ")
                self.ad_text = self._replace_param("Ключевые преимущества", new_key_benefits)
            elif choice == 4:
                new_call_to_action = input("Введите новый призыв к действию: ")
                self.ad_text = self._replace_param("Призыв к действию", new_call_to_action)
            elif choice == 5:
                new_style = input("Введите новый стиль объявления: ")
                self.ad_text = self._replace_param("Стиль объявления", new_style)
            elif choice == 6:
                new_length_limit = input("Введите новые ограничения на длину слов: ")
                self.ad_text = self._replace_param("Желаемый размер объявления в символах", new_length_limit)
            elif choice == 7:
                arbitrary_change = input("Введите произвольное изменение (например, 'добавить текст в конец'): ")
                self.ad_text += f"\n{arbitrary_change}"
            elif choice == 8:
                break

        print("\nОбновленное объявление:\n", self.ad_text)

    def _replace_param(self, param_name, new_value):
        start_idx = self.ad_text.find(param_name)
        if start_idx == -1:
            return self.ad_text
        end_idx = self.ad_text.find("\n", start_idx)
        if end_idx == -1:
            return self.ad_text[:start_idx] + f"{param_name}: {new_value}"
        return self.ad_text[:start_idx] + f"{param_name}: {new_value}" + self.ad_text[end_idx:]
