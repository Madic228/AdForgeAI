from ad_generator import AdGenerator
from config import model_provider_map

class AdManager:
    def __init__(self, proxies=None):
        self.generator = None
        self.headline = ""
        self.audience = ""
        self.key_benefits = ""
        self.call_to_action = ""
        self.style = ""
        self.length_limit = None
        self.model_name = ''
        self.provider = None
        self.temperature = 0.7
        self.stream = False
        self.proxies = proxies

    def set_basic_params(self, headline, audience):
        self.headline = headline
        self.audience = audience

    def set_advanced_params(self, key_benefits=None, call_to_action=None, style=None, length_limit=None, model_choice=1, temperature=0.7, stream=False):
        self.key_benefits = key_benefits
        self.call_to_action = call_to_action
        self.style = style
        self.length_limit = length_limit
        self.model_name, self.provider = model_provider_map[model_choice]
        self.temperature = temperature
        self.stream = stream

    async def generate_ad(self):
        self.generator = AdGenerator(model_name=self.model_name, provider=self.provider, proxies=self.proxies)
        return await self.generator.generate_ad(
            headline=self.headline,
            audience=self.audience,
            key_benefits=self.key_benefits,
            call_to_action=self.call_to_action,
            style=self.style,
            length_limit=self.length_limit,
            temperature=self.temperature,
            stream=self.stream
        )
