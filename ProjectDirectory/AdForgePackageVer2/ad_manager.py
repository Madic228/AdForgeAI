import json
import datetime
import g4f
import sys
from config import model_provider_map
import re

from ad_generator import AdGenerator

# class AdGenerator:
#     def __init__(self, model_name, provider, proxies=None):
#         self.model_name = model_name
#         self.provider = provider
#         self.proxies = proxies
#
#
#     async def generate_ad(self, headline, audience, key_benefits=None, call_to_action=None, style=None, length_limit=None, temperature=0.7, stream=False):
#         system_message = {
#             "role": "system",
#             "content": "Вы профессионал в создании рекламных объявлений. Ваша задача - создавать высококачественные рекламные объявления, соответствующие заданным параметрам."
#                        " Вы пишите объявления без использования эмодзи, делаете их структурированными, с красивым форматированием. По всем стандартам. Абзацев должно быть несколько, текст должен быть со всеми возможными переносами."
#         }
#         prompt = f"Заголовок объявления: {headline}\nЦелевая аудитория: {audience}\n"
#         if key_benefits:
#             prompt += f"Ключевые преимущества: {key_benefits}\n"
#         if call_to_action:
#             prompt += f"Призыв к действию: {call_to_action}\n"
#         if style:
#             prompt += f"Стиль объявления: {style}\n"
#         if length_limit:
#             prompt += f"Желаемый размер объявления в символах: {length_limit}\n"
#
#         setting = "Вывод должен содержать только текст объявления и ничего больше Не используй эмодзи и юникод. При упоминании личных данных всегда добавляй [] и в них пиши, что пользователю нужно вписать."
#
#         user_message = {"role": "user", "content": prompt + setting}
#         messages = [system_message, user_message]
#
#         response_gen = self.provider.create_async_generator(
#             model=self.model_name,
#             messages=messages,
#             temperature=temperature,
#             stream=stream,
#             proxy=self.proxies.get("all") if self.proxies else None
#         )
#
#         result = []
#         if stream:
#             async for message in response_gen:
#                 sys.stdout.buffer.write(message.encode('utf-8', 'surrogateescape'))
#                 sys.stdout.buffer.flush()
#                 result.append(message)
#         else:
#             result = [message async for message in response_gen]
#
#         return "".join(result)

class AdManager:
    def __init__(self, proxies=None):
        self.proxies = proxies
        self.generator = None
        self.headline = ""
        self.audience = ""
        self.key_benefits = ""
        self.call_to_action = ""
        self.style = ""
        self.length_limit = None
        self.model_name = 'gpt-3.5-turbo-0125'
        self.provider = g4f.Provider.Ecosia
        self.temperature = 0.7
        self.stream = False

    def set_basic_params(self, headline, audience):
        self.headline = headline
        self.audience = audience

    def set_advanced_params(self, key_benefits=None, call_to_action=None, style=None, length_limit=None, model_choice=None, temperature=None, stream=None):
        self.key_benefits = key_benefits
        self.call_to_action = call_to_action
        self.style = style
        self.length_limit = length_limit
        if model_choice is not None:
            self.model_name, self.provider = self.get_model_name_and_provider(model_choice)
        if temperature is not None:
            self.temperature = temperature
        if stream is not None:
            self.stream = stream
        self.generator = AdGenerator(model_name=self.model_name, provider=self.provider, proxies=self.proxies)
        self.initialize_generator()
    def get_model_name_and_provider(self, choice):
        return model_provider_map.get(choice, ('gpt-3.5-turbo-0125', g4f.Provider.Ecosia))

    async def generate_ad(self):
        ad_text = await self.generator.generate_ad(
            headline=self.headline,
            audience=self.audience,
            key_benefits=self.key_benefits,
            call_to_action=self.call_to_action,
            style=self.style,
            length_limit=self.length_limit,
            temperature=self.temperature,
            stream=self.stream
        )

        ad_text = remove_surrogates(ad_text)  # Удаление суррогатных пар
        self.save_ad_to_json(ad_text, 1)
        return ad_text

    async def generate_ad_with_edit(self, old_ad_text, edit_instructions):
        system_message = {
            "role": "system",
            "content": "Вы профессионал в создании рекламных объявлений. Ваша задача - редактировать предоставленные объявления в соответствии с новыми критериями. В ответе вы должны дать только текст объявления. Ты не используешь эмодзи и юникод при генерации объявления."
        }
        user_message = {"role": "user", "content": f"Старое объявление: {old_ad_text}\n\nКритерии редактирования: {edit_instructions}"}
        messages = [system_message, user_message]

        response_gen = self.provider.create_async_generator(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            stream=self.stream,
            proxy=self.proxies.get("all") if self.proxies else None
        )

        result = []
        if self.stream:
            async for message in response_gen:
                sys.stdout.buffer.write(message.encode('utf-8', 'surrogateescape'))
                sys.stdout.buffer.flush()
                result.append(message)
        else:
            result = [message async for message in response_gen]

        ad_text = "".join(result)
        ad_text = remove_surrogates(ad_text)  # Удаление суррогатных пар
        return ad_text

    def save_ad_to_json(self, ad_text, version, ad_index=None):
        ad_text = remove_surrogates(ad_text)  # Удаление суррогатных пар
        ad_data = {
            "creation_date": datetime.datetime.now().isoformat(),
            "version": version,
            "headline": self.headline,
            "audience": self.audience,
            "key_benefits": self.key_benefits,
            "call_to_action": self.call_to_action,
            "style": self.style,
            "length_limit": self.length_limit,
            "model_name": self.model_name,
            "provider": self.provider.__name__,  # Сохранение провайдера
            "temperature": self.temperature,
            "stream": self.stream,
            "ad_text": ad_text
        }

        try:
            with open('ad_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        # Найти объявление с таким же заголовком и аудиторией
        ad_exists = False
        for ad in data:
            if ad["headline"] == self.headline and ad["audience"] == self.audience:
                ad["version"] = version
                ad["creation_date"] = ad_data["creation_date"]
                ad["key_benefits"] = ad_data["key_benefits"]
                ad["call_to_action"] = ad_data["call_to_action"]
                ad["style"] = ad_data["style"]
                ad["length_limit"] = ad_data["length_limit"]
                ad["model_name"] = ad_data["model_name"]
                ad["provider"] = ad_data["provider"]
                ad["temperature"] = ad_data["temperature"]
                ad["stream"] = ad_data["stream"]
                ad["ad_text"] = ad_data["ad_text"]
                ad_exists = True
                break

        if not ad_exists:
            data.append(ad_data)

        with open('ad_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_ad_version_from_json(self):
        try:
            with open('ad_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Инициализация AdGenerator с правильными значениями из JSON
            for ad in data:
                self.model_name = ad['model_name']
                self.provider = getattr(g4f.Provider, ad['provider'])
                self.generator = AdGenerator(model_name=self.model_name, provider=self.provider, proxies=self.proxies)
                self.initialize_generator()
            return data
        except FileNotFoundError:
            return []

    def initialize_generator(self):
        self.generator = AdGenerator(model_name=self.model_name, provider=self.provider, proxies=self.proxies)

def remove_surrogates(text):
    # Удаление суррогатных пар
    return re.sub(r'[\ud800-\udfff]', '', text)


