import g4f

g4f.debug.logging = True

from g4f.client import Client

proxies = {
    "all": "http://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970",
    "https": "https://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970"
}
client = Client(proxies=proxies)

response = client.chat.completions.create(
    model="google/gemma-1.1-7b-it",
    provider=g4f.Provider.HuggingChat,
   messages=[{"role": "user", "content": "Что ты за модель? Справишься ли ты с таким заданием, генерация рекламного объявления по заголовку"}]
)
print(response.choices[0].message.content)
