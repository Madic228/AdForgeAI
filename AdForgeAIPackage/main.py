import g4f



response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Можешь предложить улучшения по коду:"}],
    stream=True,
)


for message in response:
    print(message, flush=True, end='')

