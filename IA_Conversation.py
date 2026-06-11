import os
import requests
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError
from IPython.display import Markdown, display

load_dotenv(override=True)

google_api_key = os.getenv('GOOGLE_API_KEY')

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")

gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)


'''
tell_a_joke = [
    {"role": "system", "content": "You are a helpful assistant that tells jokes in spanish to students learning about LLM Engineering."},
    {"role": "user", "content": "Tell a joke for a student on the journey to becoming an expert in LLM Engineering"},
]

response = completion(model="gemini/gemini-2.5-flash-lite", messages=tell_a_joke)
print(response.choices[0].message.content)

'''

gemini1_model = "gemini-2.5-flash"
gemini2_model = "gemini-2.5-flash-lite"

gemini1_system = "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way. All in spanish"

gemini2_system = "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting. All in spanish"

gemini1_messages = ["Holaa, ¿cómo estás?"]
gemini2_messages = ["Hola"]

def call_gemini_1():
    messages = [{"role": "system", "content": gemini1_system}]
    for model1, model2 in zip(gemini1_messages, gemini2_messages):
        messages.append({"role": "assistant", "content": model1})
        messages.append({"role": "user", "content": model2})
    try:
        response = gemini.chat.completions.create(model=gemini1_model, messages=messages)
        return response.choices[0].message.content
    except RateLimitError as exc:
        print(f"Gemini 1 hit a quota limit: {exc}")
        return None


def call_gemini_2():
    messages = [{"role": "system", "content": gemini2_system}]
    for model1, model2 in zip(gemini1_messages, gemini2_messages):
        messages.append({"role": "user", "content": model1})
        messages.append({"role": "assistant", "content": model2})
    messages.append({"role": "user", "content": gemini1_messages[-1]})
    try:
        response = gemini.chat.completions.create(model=gemini2_model, messages=messages)
        return response.choices[0].message.content
    except RateLimitError as exc:
        print(f"Gemini 2 hit a quota limit: {exc}")
        return None


gemini1_messages = ["Holaa, ¿cómo estás?"]
gemini2_messages = ["Hola"]

print(f"### Gemini 1:\n{gemini1_messages[0]}\n")
print(f"### Gemini 2:\n{gemini2_messages[0]}\n")

for i in range(5):
    gemini1_next = call_gemini_1()
    if gemini1_next is None:
        break
    print(f"### Gemini 1:\n{gemini1_next}\n")
    gemini1_messages.append(gemini1_next)

    gemini2_next = call_gemini_2()
    if gemini2_next is None:
        break
    print(f"### Gemini 2:\n{gemini2_next}\n")
    gemini2_messages.append(gemini2_next)
    time.sleep(3)