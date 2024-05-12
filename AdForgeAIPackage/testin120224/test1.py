import g4f
import logging

g4f.debug.logging = True

logging.basicConfig(
    filename='g4f.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)

def list_providers_and_models():
    """Выводит список доступных провайдеров и поддерживаемых моделей."""

    print("Доступные провайдеры:")
    for provider_name in dir(g4f.Provider):
        if not provider_name.startswith("_"):
            provider = getattr(g4f.Provider, provider_name)
            # Проверка наличия атрибутов
            supports_gpt_35 = hasattr(provider, 'supports_gpt_35_turbo') and provider.supports_gpt_35_turbo
            supports_gpt_4 = hasattr(provider, 'supports_gpt_4') and provider.supports_gpt_4
            print(f"- {provider_name} (поддерживает GPT-3.5: {supports_gpt_35}, GPT-4: {supports_gpt_4})")

    print("\nДоступные модели:")
    for model_name in g4f.models.__dict__:
        if not model_name.startswith("_") and isinstance(getattr(g4f.models, model_name), g4f.models.Model): # Проверка типа
            model = getattr(g4f.models, model_name)
            print(f"- {model_name}: {model}")

list_providers_and_models()

# Пример использования:
messages = [{"role": "user", "content": "Тестовый запрос"}]

# Выберите модель из списка
available_models = [getattr(g4f.models, model_name) for model_name in g4f.models.__dict__
                      if not model_name.startswith("_") and isinstance(getattr(g4f.models, model_name), g4f.models.Model)]

if available_models:
    chosen_model = available_models[0]  # Выбираем первую доступную модель
    response = g4f.ChatCompletion.create(
        model=chosen_model,
        messages=messages
    )

    if response:
        print("\nОтвет GPT:")
        print(response)
    else:
        print("\nНе удалось получить ответ от GPT.")
else:
    print("\nНет доступных моделей.")