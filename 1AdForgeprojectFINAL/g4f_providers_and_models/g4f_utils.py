import g4f
import json
import logging

g4f.debug.logging = True

logging.basicConfig(
    filename='g4f.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)

def save_providers_to_json(filename="providers.json"):
    """Сохраняет список доступных провайдеров в JSON файл."""

    providers = {}
    for provider_name in dir(g4f.Provider):
        if not provider_name.startswith("_"):
            provider = getattr(g4f.Provider, provider_name)
            supports_gpt_35 = hasattr(provider, 'supports_gpt_35_turbo') and provider.supports_gpt_35_turbo
            supports_gpt_4 = hasattr(provider, 'supports_gpt_4') and provider.supports_gpt_4
            providers[provider_name] = {
                "supports_gpt_35": supports_gpt_35,
                "supports_gpt_4": supports_gpt_4
            }

    with open(filename, "w", encoding='utf-8') as f:
        json.dump(providers, f, ensure_ascii=False, indent=4)

def save_models_to_json(filename="models.json"):
    """Сохраняет список доступных моделей в JSON файл."""

    models = {}
    for model_name in g4f.models.__dict__:
        if not model_name.startswith("_") and isinstance(getattr(g4f.models, model_name), g4f.models.Model):
            model = getattr(g4f.models, model_name)
            models[model_name] = str(model)

    with open(filename, "w", encoding='utf-8') as f:
        json.dump(models, f, ensure_ascii=False, indent=4)

# Вызов функций для сохранения данных
save_providers_to_json()
save_models_to_json()


# Пример использования
# from g4f_utils import save_providers_to_json, save_models_to_json
#
# class MyGPTApp:
#
#     def __init__(self):
#         # Обновляем информацию о моделях и провайдерах при запуске
#         self.update_gpt_data()
#
#     def update_gpt_data(self):
#         save_providers_to_json()
#         save_models_to_json()