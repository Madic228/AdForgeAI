import g4f

import os

import asyncio
import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Установка прокси-серверов
os.environ["HTTP_PROXY"] = "http://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970"

def generate_ad(headline, model="gpt-3.5-turbo-16k"):
    """
    Генерирует рекламное объявление по заголовку.

    Args:
      headline: Заголовок рекламного объявления.
      model: Название LLM для использования (по умолчанию ChatGPT).

    Returns:
      Сгенерированное рекламное объявление.
    """

    prompt = f"Создай рекламное объявление для продукта [название продукта], используя слевдующий заголовок: {headline}"
    response = g4f.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    # Возвращаем ответ напрямую, без .choices[0].message.content.strip()
    return response.strip()

    # Пример использования


headline = "Лучший продукт для решения ваших проблем!"
ad_text = generate_ad(headline)
print(ad_text)