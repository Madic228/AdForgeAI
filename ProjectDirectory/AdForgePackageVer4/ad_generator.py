import g4f

class AdGenerator:
    def __init__(self, model_name, provider, proxies=None):
        self.model_name = model_name
        self.provider = provider
        self.proxies = proxies

    async def generate_ad(self, headline, audience, key_benefits=None, call_to_action=None, style=None, length_limit=None, temperature=0.7, stream=False):
        system_message = {
            "role": "system",
            "content": "Вы профессионал в создании рекламных объявлений. Ваша задача - создавать высококачественные рекламные объявления, соответствующие заданным параметрам."
        }
        prompt = f"Заголовок объявления: {headline}\nЦелевая аудитория: {audience}\n"
        if key_benefits:
            prompt += f"Ключевые преимущества: {key_benefits}\n"
        if call_to_action:
            prompt += f"Призыв к действию: {call_to_action}\n"
        if style:
            prompt += f"Стиль объявления: {style}\n"
        if length_limit:
            prompt += f"Размер объявления: {length_limit}\n"

        setting = "Я хочу видеть в результате красивое объявление с введенными параметрами, пожалуйста не нужно больше никакой информации помимо неё, также объем должен быть в пару абзацев, оформленный по стандартам объявлений с указанием ссылок на авторов, адрес продукта, если это уместно"

        user_message = {"role": "user", "content": prompt + setting}
        messages = [system_message, user_message]

        response_gen = self.provider.create_async_generator(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            stream=stream,
            proxy=self.proxies.get("all") if self.proxies else None
        )

        result = []
        if stream:
            async for message in response_gen:
                try:
                    print(message.encode('utf-8', 'ignore').decode('utf-8'), end='', flush=True)
                except UnicodeEncodeError:
                    message = message.encode('utf-8', 'ignore').decode('utf-8')
                    print(message, end='', flush=True)
                result.append(message)
        else:
            result = [message async for message in response_gen]

        return "".join(result)
