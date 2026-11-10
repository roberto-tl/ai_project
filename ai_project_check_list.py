from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)
user_input = input('Insert your prompt!: ')

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "system", "content": "Explain it as a teacher for your students"},
        {"role": "user", "content": user_input},], 
    stream=False,
    reasoning_effort="low"
    )

print(response.choices[0].message.content)