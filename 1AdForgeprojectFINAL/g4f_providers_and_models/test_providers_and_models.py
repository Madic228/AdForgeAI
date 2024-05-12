import asyncio
import json
import logging

import g4f

g4f.debug.logging = True

logging.basicConfig(
    filename='g4f.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)


async def test_provider_async(provider_name, model_name="gpt-3.5-turbo", timeout=10):
    """Асинхронно тестирует провайдера с заданной моделью."""
    try:
        response = await asyncio.wait_for(
            g4f.ChatCompletion.create_async(
                model=model_name,
                messages=[{"role": "user", "content": "Тестовый запрос"}],
                provider=getattr(g4f.Provider, provider_name)
            ),
            timeout=timeout
        )
        if response:
            print(f"Провайдер {provider_name} РАБОТАЕТ с моделью {model_name}!")
            return True
        else:
            print(f"Провайдер {provider_name} НЕ работает с моделью {model_name}.")
            return False
    except asyncio.TimeoutError:
        print(f"Провайдер {provider_name} - время ожидания истекло.")
        return False
    except Exception as e:
        print(f"Провайдер {provider_name} вызвал ошибку: {e}")
        return False


async def find_working_providers_async():
    """Находит работающие провайдеры для модели gpt-3.5-turbo."""
    working_providers = []
    tasks = []

    excluded_providers = ["AItianhu", "AItianhuSpace"]  # Добавьте проблемные провайдеры

    for provider_name in dir(g4f.Provider):
        if not provider_name.startswith("_") and provider_name not in excluded_providers:
            tasks.append(test_provider_async(provider_name))

    results = await asyncio.gather(*tasks)
    for i, result in enumerate(results):
        if result:
            provider_name = list(dir(g4f.Provider))[i]
            working_providers.append(provider_name)

    return working_providers


def save_working_providers(providers, filename="working_providers.json"):
    """Сохраняет список работающих провайдеров в JSON файл."""
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(providers, f, ensure_ascii=False, indent=4)


async def main():
    working_providers = await find_working_providers_async()
    save_working_providers(working_providers)

    if working_providers:
        print("Рабочие провайдеры для модели gpt-3.5-turbo сохранены в working_providers.json")
    else:
        print("Не найдено рабочих провайдеров.")


if __name__ == "__main__":
    asyncio.run(main())