import g4f

# Print all available providers
print([
    provider.__name__
    for provider in g4f.Provider.__providers__
    if provider.working
])

# Execute with a specific provider
response = g4f.ChatCompletion.create(
    model="gpt-4",
    provider=g4f.Provider.Chatgpt4Online,
    messages=[{"role": "user", "content": "Привет, что ты за модель?"}],
    stream=True,
)
for message in response:
    print(message)