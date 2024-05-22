import g4f

model_provider_map = {
    1: ('gpt-3.5-turbo-0125', g4f.Provider.Ecosia),
    2: ('claude-3-haiku-20240307', g4f.Provider.DuckDuckGo),
    3: ('google/gemma-1.1-7b-it', g4f.Provider.HuggingChat),
    4: ('NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO', g4f.Provider.HuggingChat),
    5: ('green', g4f.Provider.Ecosia)
}

# Прокси-сервер
proxies = {
    "all": "http://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970",
    "https": "https://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970"
}
