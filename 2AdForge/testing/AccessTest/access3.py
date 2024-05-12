import g4f

g4f.debug.logging = True

from g4f.client import Client

proxies = {
    "all": "http://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970",
    "https": "https://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970"
}
client = Client(proxies=proxies)

response = client.chat.completions.create(
   model="gpt-3.5-turbo",
    provider=g4f.Provider.Chatgpt4Online,
   messages=[{"role": "user", "content": "Привет, какая ты версия gpt?"}]
)
print(response.choices[0].message.content)
