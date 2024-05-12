import g4f
import logging

from g4f.client import Client

g4f.debug.logging = True

logging.basicConfig(
    filename='g4f.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)

proxies = {
    "all": "http://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970",
    "https": "https://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970"
}

from g4f.cookies import set_cookies

set_cookies(".bing.com", {
  "MUID": "270E617F4C5467D3281172824D7C6684"
})
set_cookies(".google.com", {
  "__Secure-1PSID": "g.a000jgiMy_IrxUh1eFvbBlXwEnTApWpSjiCeVEzdUH2uNohZlhqeU1bnite6_qimio8b2cM6qAACgYKAVgSAQASFQHGX2MirT372zxp0XWOViVwKerfdxoVAUF8yKoatkDGDxnT1iKdcr-TKBhR0076	"
})

client = Client(proxies=proxies)

def main():
    """Главная функция чата."""

    chat_history = []

    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "exit":
            break

        chat_history.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create( # Используем client для запросов
                model="gpt-4-turbo",
                provider=g4f.Provider.Bing,
                messages=chat_history
            )

            print(f"GPT: {response.choices[0].message.content}") # Извлекаем текст из ответа
            chat_history.append({"role": "assistant", "content": response.choices[0].message.content})

        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()