from g4f import GPT4

# Создаем экземпляр модели
model = GPT4()

prompt = "Привет, я GPT-4. Давай поговорим о Python!"
generated_text = model.generate_text(prompt, max_length=100)
print(generated_text)