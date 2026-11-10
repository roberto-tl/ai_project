from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)
user_input = input('Insert a text to create a checklist: ')

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "system", "content": "change the user input into a checklist. Use emojis and squares at the beginning to make easier for read"},
        {"role": "user", "content": user_input},], 
    stream=False,
    reasoning_effort="low"
    )

print(response.choices[0].message.content)