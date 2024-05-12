import g4f

g4f.debug.logging = True

from g4f.client import Client

proxies = {
    "all": "http://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970",
    "https": "https://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970"
}
client = Client(proxies=proxies)

response = client.chat.completions.create(
    model="gpt-4-turbo",
    provider=g4f.Provider.You,
   messages=[{"role": "user", "content": "Какая ты версия gpt?"}]
)
print(response.choices[0].message.content)
