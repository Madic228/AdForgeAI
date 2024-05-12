import g4f
import time

import os



import asyncio
import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#
# os.environ["G4F_PROXY"] = "http://gkodmrwtb:fOqettKDvWrA@193.233.164.83:62970"

# Define the query for generating a response from the AI
query = "Создай рекламное объявление для продукта [название продукта], используя следующий заголовок: 'Вашей кошке понравится наш кошачий корм MyLittleCat'"

# Record the start time to measure the duration of the process
start = time.time()

# Use the g4f.ChatCompletion.create() chat completion with specified parameters
response = g4f.ChatCompletion.create(
    # Choose the GPT-4 model for better stability and performance (unlimited access, slower but stable)
    # model='gpt-4',

    # Alternatively, you can use the GPT-3.5 Turbo model for faster response (unlimited access, very fast but less stable)
    # model="gpt-3.5-turbo",
    model="gpt-4-turbo",

    # Best model for GPT4 access with realtime data. slow but very accurate
    provider=g4f.Provider.Bing,
    # GPTGo is the fastest but less stable
    # provider=g4f.Provider.Aura,
    # GPTalk is slow but quite stable
    # provider=g4f.Provider.GPTalk,
    # provider=g4f.Provider.Ecosia,
    # provider=g4f.Provider.Cnote,
    # provider=g4f.Provider.Liaobots,
    # Provide the user query as a "message" for chat completion
    messages=[{'role': 'user', 'content': query}],

    # Enable stream mode for real-time output
    stream=False,
)

# Iterate through the response messages and print them
for message in response:
    print(message, flush=True, end="")

# Record the end time and calculate the duration
end = time.time()
print(f"\nTIME TAKEN : {end - start} seconds")