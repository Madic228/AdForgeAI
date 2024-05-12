
from g4f.client import Client

# Установка переменной окружения (необязательно, если она уже установлена)
import os



import asyncio
import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

os.environ["G4F_PROXY"] = "http://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970"

client = Client()
response = client.chat.completions.create(
    model="claude-v1",
    messages=[{"role": "user", "content": "Создай рекламное объявление для продукта [название продукта], используя следующий заголовок: 'Вашей кошке понравится наш кошачий корм Kislove'"}]
)
print(response.choices[0].message.content)